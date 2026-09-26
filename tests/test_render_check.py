import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".agents" / "skills" / "bc-design" / "scripts" / "render_check.py"
SPEC = importlib.util.spec_from_file_location("render_check", SCRIPT)
render_check = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(render_check)

CLEAN_PROBE = {"scrollWidth": 375, "clientWidth": 375, "unnamedControls": [], "imagesWithoutAlt": []}


class RenderCheckTests(unittest.TestCase):
    def test_parses_viewport_lists(self):
        self.assertEqual(render_check.parse_viewports("375x812, 1440x900"), [(375, 812), (1440, 900)])
        with self.assertRaises(ValueError):
            render_check.parse_viewports("wide")
        with self.assertRaises(ValueError):
            render_check.parse_viewports("100x100")

    def test_reduced_motion_runs_cover_the_narrowest_and_widest_views(self):
        runs = render_check.plan_runs([(375, 812), (768, 1024), (1440, 900)])
        reduced = [(width, height) for width, height, motion in runs if motion == "reduce"]
        self.assertEqual(reduced, [(375, 812), (1440, 900)])
        self.assertEqual(sum(1 for *_, motion in runs if motion == "no-preference"), 3)

    def test_clean_render_has_no_findings(self):
        self.assertEqual(render_check.findings_for((375, 812, "no-preference"), CLEAN_PROBE, [], [], []), [])

    def test_reports_overflow_errors_and_unnamed_controls(self):
        probe = {
            "scrollWidth": 420,
            "clientWidth": 375,
            "unnamedControls": ["<button></button>"],
            "imagesWithoutAlt": ["hero.jpg"],
        }
        findings = render_check.findings_for((375, 812, "reduce"), probe, ["boom"], ["TypeError"], ["https://cdn/x.js"])
        rules = {finding["rule_id"] for finding in findings}
        self.assertEqual(
            rules,
            {
                "render-horizontal-overflow",
                "render-console-error",
                "render-page-error",
                "render-failed-request",
                "render-image-alt",
                "render-unnamed-control",
            },
        )
        self.assertTrue(all(finding["view"] == "375px reduced-motion" for finding in findings))

    def test_merges_the_same_problem_across_views(self):
        first = render_check.findings_for((375, 812, "no-preference"), CLEAN_PROBE, ["boom"], [], [])
        second = render_check.findings_for((1440, 900, "no-preference"), CLEAN_PROBE, ["boom"], [], [])
        merged = render_check.dedupe(first + second)
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["views"], ["375px", "1440px"])

    def test_explains_how_to_install_playwright_when_missing(self):
        with tempfile.TemporaryDirectory() as tempdir:
            page = Path(tempdir) / "page.html"
            page.write_text("<h1>Hello</h1>", encoding="utf-8")
            code = (
                "import sys, runpy\n"
                "sys.modules['playwright'] = None\n"
                f"sys.argv = ['render_check.py', {str(page)!r}]\n"
                f"runpy.run_path({str(SCRIPT)!r}, run_name='__main__')\n"
            )
            completed = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
        self.assertEqual(completed.returncode, 2)
        self.assertIn("pip install playwright", completed.stderr)

    def test_rejects_a_missing_target(self):
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), str(ROOT / "does-not-exist.html")],
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 2)
        self.assertIn("does-not-exist.html", completed.stderr)


FIXTURES = ROOT / "tests" / "fixtures" / "render"


def _serve_signed_in_app():
    """A tiny app: /dashboard needs a session cookie, and its /api/tasks backend is down."""
    import http.server
    import threading

    page = (FIXTURES / "signed-in-app.html").read_bytes()

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path.startswith("/dashboard"):
                if "session=signed-in" not in (self.headers.get("Cookie") or ""):
                    self.send_response(302)
                    self.send_header("Location", "/login")
                    self.end_headers()
                    return
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(page)
            elif self.path.startswith("/login"):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"<!doctype html><title>Sign in</title><h1>Sign in</h1>")
            else:
                self.send_response(503)
                self.end_headers()

        def log_message(self, *args):
            pass

    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


class SignedInRenderTests(unittest.TestCase):
    def test_parses_cookies_and_mocks(self):
        self.assertEqual(
            render_check.parse_cookies(["session=abc=1"], "http://localhost:3000/dashboard"),
            [{"name": "session", "value": "abc=1", "url": "http://localhost:3000"}],
        )
        with self.assertRaises(ValueError):
            render_check.parse_cookies(["session=abc"], "file:///tmp/page.html")
        mocks = render_check.parse_mocks(["**/api/tasks*=tasks.json"], base=FIXTURES)
        self.assertEqual(mocks[0][0], "**/api/tasks*")
        self.assertIn("Review the weekly plan", mocks[0][1])
        self.assertTrue(render_check.redirected_to_sign_in("http://x/dashboard", "http://x/login?next=/dashboard"))
        self.assertFalse(render_check.redirected_to_sign_in("http://x/login", "http://x/login"))

    def test_renders_a_signed_in_page_with_mocked_data(self):
        try:
            import playwright  # noqa: F401
        except ImportError:
            self.skipTest("Playwright is not installed")
        server = _serve_signed_in_app()
        url = f"http://127.0.0.1:{server.server_address[1]}/dashboard"
        try:
            with tempfile.TemporaryDirectory() as tempdir:
                out = Path(tempdir)
                viewports = [(375, 812)]
                _, signed_out = render_check.run_checks(url, viewports, out / "a")
                _, with_cookie = render_check.run_checks(
                    url, viewports, out / "b",
                    cookies=render_check.parse_cookies(["session=signed-in"], url),
                    mocks=render_check.parse_mocks(["**/api/tasks=tasks.json"], base=FIXTURES),
                )
                _, with_state = render_check.run_checks(
                    url, viewports, out / "c",
                    storage_state=render_check.check_storage_state(str(FIXTURES / "storage-state.json")),
                    mocks=render_check.parse_mocks(["**/api/tasks=tasks.json"], base=FIXTURES),
                )
                _, unmocked = render_check.run_checks(
                    url, viewports, out / "d", cookies=render_check.parse_cookies(["session=signed-in"], url)
                )
        finally:
            server.shutdown()
        self.assertIn("render-signed-out", {finding["rule_id"] for finding in signed_out})
        self.assertEqual(with_cookie, [])
        self.assertEqual(with_state, [])
        self.assertIn("render-console-error", {finding["rule_id"] for finding in unmocked})


if __name__ == "__main__":
    unittest.main()

(() => {
  const root = document.documentElement;
  const themeToggle = document.querySelector("[data-theme-toggle]");
  const themeLabel = document.querySelector("[data-theme-label]");
  const menuToggle = document.querySelector("[data-menu-toggle]");
  const nav = document.querySelector("#primary-nav");
  const visitForm = document.querySelector("[data-visit-form]");
  const formStatus = document.querySelector("[data-form-status]");

  let savedTheme = null;
  try {
    savedTheme = window.localStorage.getItem("bc-school-theme");
  } catch {
    // Private browsing can disable storage; the page still works per session.
  }
  if (savedTheme === "dark" || savedTheme === "light") {
    root.dataset.theme = savedTheme;
  }

  const updateThemeControl = () => {
    const isDark = root.dataset.theme === "dark";
    themeToggle.setAttribute("aria-pressed", String(isDark));
    themeLabel.textContent = isDark ? "Gunakan mode terang" : "Gunakan mode gelap";
  };

  updateThemeControl();

  themeToggle.addEventListener("click", () => {
    root.dataset.theme = root.dataset.theme === "dark" ? "light" : "dark";
    try {
      window.localStorage.setItem("bc-school-theme", root.dataset.theme);
    } catch {
      // Theme switching remains useful even when persistence is unavailable.
    }
    updateThemeControl();
  });

  const closeMenu = () => {
    nav.classList.remove("is-open");
    menuToggle.setAttribute("aria-expanded", "false");
  };

  menuToggle.addEventListener("click", () => {
    const isOpen = menuToggle.getAttribute("aria-expanded") === "true";
    menuToggle.setAttribute("aria-expanded", String(!isOpen));
    nav.classList.toggle("is-open", !isOpen);
    menuToggle.querySelector(".sr-only").textContent = isOpen ? "Buka navigasi" : "Tutup navigasi";
  });

  nav.querySelectorAll("a").forEach((link) => link.addEventListener("click", closeMenu));

  document.querySelector("[data-focus-visit]").addEventListener("click", () => {
    window.setTimeout(() => document.querySelector("#visitor-name").focus(), 350);
  });

  visitForm.addEventListener("submit", (event) => {
    event.preventDefault();
    if (!visitForm.reportValidity()) return;
    formStatus.textContent = "Terima kasih. Tim kami akan menghubungi Anda dalam satu hari sekolah.";
    visitForm.reset();
  });
})();

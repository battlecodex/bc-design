/**
 * Regression guard — every audit case in one file.
 */
import gsap from "gsap";

const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

export function Everything() {
  // Comment with an em dash — never copy.
  if (!reduce) gsap.to(".row", { duration: 2.5, ease: "bounce.out" });
  return (
    <main>
      {/* Header — still a comment */}
      <p>Plan ahead — then ship</p>
      <div className="transition-opacity duration-1000 ease-[var(--bc-ease)]">Slow fade</div>
      <div className="transition-transform duration-150 ease-[cubic-bezier(0.68,-0.6,0.32,1.6)]">Springy</div>
      <div className="transition-transform duration-150 ease-[cubic-bezier(0.16,1,0.3,1)]">Calm</div>
      <div className="fixed inset-0 bg-[#000]/50" />
      <div className="fixed inset-0 bg-[rgb(0_0_0/0.5)]" />
      <p>Done ✓ → next ★</p>
      <span aria-hidden="true" className="sr-hint">Decorative mark ✓</span>
      <button className="rounded-md px-4 py-2 focus-visible:ring-2">Save plan</button>
    </main>
  );
}

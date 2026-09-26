const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
if (!reduce) {
  gsap.to(".row", { y: 0, opacity: 1, duration: 0.25, ease: "expo.out" });
}

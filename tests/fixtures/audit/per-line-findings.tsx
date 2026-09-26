import gsap from "gsap";
export function B() {
  gsap.to(".x", { duration: 2.5, ease: "bounce.out" });          // line 3: reported
  return <button className="outline-none duration-1000">Go</button>; // line 4: duration-1000 NOT reported
}

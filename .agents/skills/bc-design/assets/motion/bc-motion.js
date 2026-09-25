/*
 * BC Motion: GSAP orchestration helpers on BC Design motion tokens.
 *
 * Load GSAP (and ScrollTrigger for reveals or scroll stories) before this
 * file, then call BCMotion.orchestrate(). Every helper runs inside
 * gsap.matchMedia(), so reduced-motion users get the final state with no
 * tweens, and inside gsap.context(), so revert() cleans everything up.
 */
(function (root) {
  "use strict";

  var ease = {
    out: "expo.out", // cubic-bezier(0.16, 1, 0.3, 1), the --bc-ease token
    inOut: "power2.inOut", // --bc-ease-in-out
    scrub: "none",
  };

  var duration = {
    fast: 0.15, // --bc-duration-fast
    normal: 0.25, // --bc-duration-normal
    slow: 0.4, // --bc-duration-slow, the longest UI tween
    reveal: 0.6, // --bc-duration-reveal, once-only hero and section reveals (max 0.75)
  };

  var REDUCED = "(prefers-reduced-motion: reduce)";
  var FULL = "(prefers-reduced-motion: no-preference)";

  function requireGsap() {
    if (!root.gsap) {
      throw new Error("BCMotion needs GSAP loaded first.");
    }
    return root.gsap;
  }

  /**
   * Build choreography that respects reduced motion and can be reverted.
   *
   * build(tools) receives { gsap, ease, duration, timeline }. It runs only
   * when the user allows motion. showFinal(gsap) runs instead under reduced
   * motion and should gsap.set() every element to its final state.
   * Returns an object with revert().
   */
  function orchestrate(scope, build, showFinal) {
    var gsap = requireGsap();
    var mm = gsap.matchMedia(scope || undefined);
    mm.add({ full: FULL, reduced: REDUCED }, function (context) {
      if (context.conditions.reduced) {
        if (showFinal) showFinal(gsap);
        return;
      }
      // A returned function runs when the media query stops matching or on revert().
      return build({
        gsap: gsap,
        ease: ease,
        duration: duration,
        timeline: function (vars) {
          return gsap.timeline(
            Object.assign({ defaults: { ease: ease.out, duration: duration.slow } }, vars || {})
          );
        },
      });
    });
    return { revert: function () { mm.revert(); } };
  }

  /**
   * Hero entrance in reading order. steps is a list of selectors; each step
   * overlaps the previous one so the whole sequence stays near 1.4s.
   */
  function heroSequence(steps, options) {
    options = options || {};
    return orchestrate(
      options.scope,
      function (tools) {
        var tl = tools.timeline({ defaults: { ease: ease.out, duration: duration.reveal } });
        steps.forEach(function (selector, index) {
          var distance = index === 0 ? 12 : 20;
          tl.from(selector, { autoAlpha: 0, y: distance }, index === 0 ? 0 : "-=0.45");
        });
      },
      function (gsap) {
        gsap.set(steps.join(","), { autoAlpha: 1, y: 0 });
      }
    );
  }

  /** Reveal each matching section once as it enters the viewport. */
  function revealOnce(selector, options) {
    options = options || {};
    return orchestrate(
      options.scope,
      function (tools) {
        if (root.ScrollTrigger) tools.gsap.registerPlugin(root.ScrollTrigger);
        tools.gsap.utils.toArray(selector).forEach(function (element) {
          tools.gsap.from(element, {
            autoAlpha: 0,
            y: 24,
            duration: duration.reveal,
            ease: ease.out,
            scrollTrigger: { trigger: element, start: options.start || "top 82%", once: true },
          });
        });
      },
      function (gsap) {
        gsap.set(selector, { autoAlpha: 1, y: 0 });
      }
    );
  }

  /** Stagger a list, capping the total stagger at 0.3s. */
  function staggerList(selector, options) {
    options = options || {};
    return orchestrate(
      options.scope,
      function (tools) {
        var items = tools.gsap.utils.toArray(selector);
        var each = Math.min(0.06, items.length ? 0.3 / items.length : 0.06);
        tools.gsap.from(items, {
          autoAlpha: 0,
          y: 12,
          duration: duration.normal,
          ease: ease.out,
          stagger: each,
          scrollTrigger: options.trigger
            ? { trigger: options.trigger, start: "top 82%", once: true }
            : undefined,
        });
      },
      function (gsap) {
        gsap.set(selector, { autoAlpha: 1, y: 0 });
      }
    );
  }

  root.BCMotion = {
    ease: ease,
    duration: duration,
    orchestrate: orchestrate,
    heroSequence: heroSequence,
    revealOnce: revealOnce,
    staggerList: staggerList,
  };
})(typeof window !== "undefined" ? window : globalThis);

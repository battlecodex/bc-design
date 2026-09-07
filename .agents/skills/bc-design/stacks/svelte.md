# BC Design System for Svelte 5 & SvelteKi

Architecture using **Svelte 5 Runes (`$state`, `$derived`, `$props`)** and SvelteKit.

---

## 1. Svelte 5 Runes Theme State (`theme.svelte.ts`)

```ts
// src/lib/theme.svelte.ts
export class BCDesignThemeManager {
  current = $state<'light' | 'dark' | 'system'>('dark');
  resolved = $derived(
    this.current === 'dark' || (this.current === 'system' && typeof window !== 'undefined' && window.matchMedia('(prefers-color-scheme: dark)').matches)
      ? 'dark'
      : 'light'
  );

  constructor() {
    if (typeof window !== 'undefined') {
      const saved = (localStorage.getItem('bc-theme') as any) || 'dark';
      this.set(saved);
    }
  }

  set(mode: 'light' | 'dark' | 'system') {
    this.current = mode;
    if (typeof document !== 'undefined') {
      const isDark = mode === 'dark' || (mode === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches);
      const res = isDark ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', res);
      if (isDark) document.documentElement.classList.add('dark');
      else document.documentElement.classList.remove('dark');
      localStorage.setItem('bc-theme', mode);
    }
  }

  toggle() {
    this.set(this.resolved === 'dark' ? 'light' : 'dark');
  }
}

export const themeManager = new BCDesignThemeManager();
```

---

## 2. Svelte 5 Component (`BCDesignButton.svelte`)

```svelte
<script lang="ts">
  import type { Snippet } from 'svelte';

  interface Props {
    variant?: 'contrast' | 'glass' | 'terracotta';
    children: Snippet;
    onclick?: (e: MouseEvent) => void;
  }

  let { variant = 'contrast', children, onclick }: Props = $props();
</script>

<button
  class="bc-btn-{variant} bc-interactive"
  {onclick}
>
  {@render children()}
</button>
```

---

## 3. Svelte Custom Transition with BC Design Curve

```ts
// src/lib/motion.ts
import { cubicOut } from 'svelte/easing';

export function bcFadeUp(node: HTMLElement, { duration = 250, y = 8 } = {}) {
  return {
    duration,
    css: (t: number) => {
      // Approximation of cubic-bezier(0.16, 1, 0.3, 1)
      const eased = Math.pow(t - 1, 3) + 1;
      return `
        opacity: ${t};
        transform: translateY(${(1 - eased) * y}px);
      `;
    }
  };
}
```

---

## 4. 3D Spatial & WebGL in Svelte 5 / SvelteKit (Runes & Lifecycle Safety)

> **SVELTEKIT SSR & RUNES SAFETY**:
> 1. **SSR Guard**: SvelteKit routes render on the server by default. Guard all Three.js imports or instantiations inside `onMount` or `$effect` where `browser` is true.
> 2. **Never wrap Three.js in `$state()`**: Like Vue's reactivity, Svelte 5's reactive proxy wraps object fields. Keep Three.js instances in ordinary `let` variables.

### Reusable Svelte 5 Spatial Component (`BCSpatialHero.svelte`)

```svelte
<script lang="ts">
  import { onMount, type Snippet } from 'svelte';
  import * as THREE from 'three';
  import { themeManager } from '$lib/theme.svelte';

  interface Props {
    children: Snippet;
  }

  let { children }: Props = $props();
  let canvas: HTMLCanvasElement;

  onMount(() => {
    if (!canvas) return;

    const width = canvas.clientWidth || window.innerWidth;
    const height = canvas.clientHeight || 520;

    // 1. Scene & Camera
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
    camera.position.set(0, 0, 8);

    // 2. Renderer with Mobile GPU DPR Capping
    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));

    // 3. Subject-Grounded 3D Objec
    const group = new THREE.Group();
    const geo = new THREE.TorusGeometry(1.6, 0.4, 24, 64);
    const isDark = themeManager.resolved === 'dark';
    const mat = new THREE.MeshStandardMaterial({
      color: isDark ? 0xe28466 : 0xd97757,
      roughness: 0.35,
      metalness: 0.2,
    });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.position.set(2.4, 0, 0); // Positioned in right hemisphere (Zero text overlap)
    group.add(mesh);
    scene.add(group);

    const ambient = new THREE.AmbientLight(0xffffff, isDark ? 0.9 : 1.2);
    const dir = new THREE.DirectionalLight(0xffe8dc, isDark ? 2.0 : 1.5);
    dir.position.set(4, 6, 5);
    scene.add(ambient, dir);

    // 4. Animation Loop with Reduced-Motion Check
    let animId = 0;
    const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    function animate() {
      animId = requestAnimationFrame(animate);
      if (!prefersReduced) {
        group.rotation.y += 0.005;
        group.rotation.x += 0.003;
      }
      renderer.render(scene, camera);
    }
    animate();

    // 5. Responsive Resize
    function handleResize() {
      const w = canvas.parentElement?.clientWidth || window.innerWidth;
      const h = canvas.parentElement?.clientHeight || 520;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    }
    window.addEventListener('resize', handleResize);

    // 6. Complete Lifecycle Cleanup on Destroy
    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener('resize', handleResize);

      scene.traverse((obj) => {
        if (obj instanceof THREE.Mesh) {
          obj.geometry?.dispose();
          if (Array.isArray(obj.material)) obj.material.forEach((m) => m.dispose());
          else if (obj.material) obj.material.dispose();
        }
      });

      renderer.dispose();
      renderer.forceContextLoss();
    };
  });
</script>

<div class="relative w-full h-[520px] overflow-hidden bg-[var(--bc-bg)]">
  <!-- Spatial Canvas Layer: pointer-events-none prevents blocking text & buttons -->
  <canvas
    bind:this={canvas}
    class="absolute inset-0 pointer-events-none z-1"
    aria-hidden="true"
  />

  <!-- Scannable Content Layer -->
  <div class="relative z-10 max-w-xl p-8 md:p-12 flex flex-col justify-center h-full">
    {@render children()}
  </div>
</div>
```

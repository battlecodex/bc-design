# BC Design System for Svelte 5 & SvelteKit

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

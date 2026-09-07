# BC Design System for Vue 3

Implementation guide for **Vue 3, Composition API, Pinia, and Vue Router**.

---

## 1. Pinia Theme Store (`stores/bcTheme.ts`)

```ts
import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useBCDesignThemeStore = defineStore('bcTheme', () => {
  const theme = ref<'light' | 'dark' | 'system'>('dark');
  const resolvedTheme = ref<'light' | 'dark'>('dark');

  function apply(mode: 'light' | 'dark' | 'system') {
    theme.value = mode;
    const isDark = mode === 'dark' || (mode === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches);
    resolvedTheme.value = isDark ? 'dark' : 'light';

    document.documentElement.setAttribute('data-theme', resolvedTheme.value);
    if (isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }

  function toggle() {
    apply(resolvedTheme.value === 'dark' ? 'light' : 'dark');
  }

  return { theme, resolvedTheme, apply, toggle };
});
```

---

## 2. Reusable Component (`components/BCDesignCard.vue`)

```vue
<template>
  <div
    class="bc-card"
    :class="[
      'bg-[var(--bc-surface)] border border-[var(--bc-border)] rounded-2xl p-6 shadow-sm transition-all duration-200',
      interactive && 'hover:border-[var(--bc-border-strong)] hover:-translate-y-0.5 cursor-pointer'
    ]"
  >
    <div v-if="$slots.header" class="mb-4">
      <slot name="header" />
    </div>
    <div class="text-[var(--bc-text-primary)]">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  interactive?: boolean;
}>();
</script>
```

---

## 3. Vue Router Transition

In `App.vue`:

```vue
<template>
  <router-view v-slot="{ Component }">
    <transition name="bc-page" mode="out-in">
      <component :is="Component" />
    </transition>
  </router-view>
</template>

<style>
.bc-page-enter-active {
  animation: bcFadeUp 250ms cubic-bezier(0.16, 1, 0.3, 1);
}
.bc-page-leave-active {
  transition: opacity 150ms ease;
  opacity: 0;
}
</style>
```

---

## 4. 3D Spatial & WebGL in Vue 3 (Composition API & Performance Safety)

> **CRITICAL VUE 3 PERFORMANCE PITFALL**:
> Never put Three.js objects (`scene`, `camera`, `renderer`, `mesh`) inside Vue's `ref()` or `reactive()`. Vue 3's deep reactive Proxy wraps every internal matrix and transform calculation, causing frame rates to collapse from 60 FPS to 5 FPS. Always use `shallowRef()` or plain local variables inside `onMounted()`.

### Reusable 3D Spatial Component (`components/BCSpatialHero.vue`)

```vue
<template>
  <div class="relative w-full h-[520px] overflow-hidden bg-[var(--bc-bg)]">
    <!-- Non-blocking background canvas -->
    <canvas
      ref="canvasRef"
      class="absolute inset-0 pointer-events-none z-1"
      aria-hidden="true"
    />

    <!-- Hero Content Layer (Always above canvas) -->
    <div class="relative z-10 max-w-xl p-8 md:p-12 flex flex-col justify-center h-full">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import { shallowRef, onMounted, onUnmounted, watch } from 'vue';
import * as THREE from 'three';
import { useBCDesignThemeStore } from '../stores/bcTheme';

const canvasRef = shallowRef<HTMLCanvasElement | null>(null);
const themeStore = useBCDesignThemeStore();

let renderer: THREE.WebGLRenderer | null = null;
let animId: number = 0;
let resizeObserver: ResizeObserver | null = null;

onMounted(() => {
  const canvas = canvasRef.value;
  if (!canvas) return;

  const width = canvas.clientWidth || window.innerWidth;
  const height = canvas.clientHeight || 520;

  // 1. Scene & Camera
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
  camera.position.set(0, 0, 8);

  // 2. Renderer with Mobile GPU DPR Capping
  renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));

  // 3. Domain Geometry (Subject-grounded)
  const group = new THREE.Group();
  const geo = new THREE.IcosahedronGeometry(1.8, 1);
  const isDark = themeStore.resolvedTheme === 'dark';
  const mat = new THREE.MeshStandardMaterial({
    color: isDark ? 0xe28466 : 0xd97757,
    roughness: 0.35,
    metalness: 0.15,
  });
  const mesh = new THREE.Mesh(geo, mat);
  mesh.position.set(2.4, 0, 0); // Positioned in right hemisphere, zero text overlap
  group.add(mesh);
  scene.add(group);

  // Lights
  const ambient = new THREE.AmbientLight(0xffffff, isDark ? 0.9 : 1.2);
  const point = new THREE.PointLight(0xffe8dc, isDark ? 2.2 : 1.6, 20);
  point.position.set(4, 5, 6);
  scene.add(ambient, point);

  // 4. Reduced Motion Safe Animation Loop
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function animate() {
    animId = requestAnimationFrame(animate);
    if (!prefersReduced) {
      group.rotation.y += 0.004;
      group.rotation.x += 0.002;
    }
    renderer?.render(scene, camera);
  }
  animate();

  // 5. Responsive Resize Observer
  resizeObserver = new ResizeObserver((entries) => {
    for (const entry of entries) {
      const w = entry.contentRect.width;
      const h = entry.contentRect.height;
      if (w > 0 && h > 0 && renderer) {
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
        renderer.setSize(w, h);
      }
    }
  });
  if (canvas.parentElement) {
    resizeObserver.observe(canvas.parentElement);
  }

  // 6. Dual-Theme Watcher
  watch(() => themeStore.resolvedTheme, (newTheme) => {
    const dark = newTheme === 'dark';
    mat.color.setHex(dark ? 0xe28466 : 0xd97757);
    ambient.intensity = dark ? 0.9 : 1.2;
  });

  // 7. Complete GPU Memory Teardown
  onUnmounted(() => {
    cancelAnimationFrame(animId);
    resizeObserver?.disconnect();

    scene.traverse((obj) => {
      if (obj instanceof THREE.Mesh) {
        obj.geometry?.dispose();
        if (Array.isArray(obj.material)) {
          obj.material.forEach((m) => m.dispose());
        } else if (obj.material) {
          obj.material.dispose();
        }
      }
    });

    renderer?.dispose();
    renderer?.forceContextLoss();
    renderer = null;
  });
});
</script>
```

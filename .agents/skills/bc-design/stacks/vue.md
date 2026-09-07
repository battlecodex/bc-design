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

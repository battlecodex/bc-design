# BC Design System for React

Production architecture, hooks, compound components, and performance patterns for React (Vite / CRA / Remix / Next.js).

---

## 1. Theme Management Hook (`useBCDesignTheme`)

Zero-dependency theme manager that supports `system`, `light`, and `dark` modes without hydration mismatch:

```tsx
// hooks/useBCDesignTheme.ts
import { useEffect, useState, useCallback } from 'react';

type Theme = 'light' | 'dark' | 'system';

export function useBCDesignTheme() {
  const [theme, setThemeState] = useState<Theme>('system');
  const [resolvedTheme, setResolvedTheme] = useState<'light' | 'dark'>('light');

  const applyTheme = useCallback((t: Theme) => {
    const root = document.documentElement;
    const isDark = t === 'dark' || (t === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches);
    const resolved = isDark ? 'dark' : 'light';
    
    root.setAttribute('data-theme', resolved);
    if (isDark) {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
    setResolvedTheme(resolved);
  }, []);

  useEffect(() => {
    const saved = (localStorage.getItem('bc-theme') as Theme) || 'system';
    setThemeState(saved);
    applyTheme(saved);

    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handler = () => {
      if (theme === 'system') applyTheme('system');
    };
    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, [applyTheme, theme]);

  const setTheme = (newTheme: Theme) => {
    localStorage.setItem('bc-theme', newTheme);
    setThemeState(newTheme);
    applyTheme(newTheme);
  };

  return { theme, resolvedTheme, setTheme, toggle: () => setTheme(resolvedTheme === 'dark' ? 'light' : 'dark') };
}
```

---

## 2. Core Components (Compound Pattern)

### Button Component (`BCDesignButton.tsx`)
```tsx
import React from 'react';
import { clsx } from 'clsx';

interface BCDesignButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'contrast' | 'glass' | 'terracotta';
  size?: 'sm' | 'md' | 'lg';
}

export const BCDesignButton: React.FC<BCDesignButtonProps> = ({
  children,
  variant = 'contrast',
  size = 'md',
  className,
  ...props
}) => {
  const variantStyles = {
    contrast: 'bg-[var(--bc-btn-contrast-bg)] text-[var(--bc-btn-contrast-text)] hover:bg-[var(--bc-btn-contrast-hover)] shadow-sm',
    glass: 'bg-[var(--bc-btn-glass-bg)] text-[var(--bc-btn-glass-text)] border border-[var(--bc-border)] hover:bg-[var(--bc-btn-glass-hover)]',
    terracotta: 'bg-[var(--bc-accent)] text-white hover:bg-[var(--bc-accent-hover)] shadow-sm',
    primary: 'bg-[var(--bc-accent)] text-white hover:bg-[var(--bc-accent-hover)]',
  };

  const sizeStyles = {
    sm: 'px-3 py-1.5 text-xs rounded-md',
    md: 'px-4 py-2 text-sm rounded-lg',
    lg: 'px-6 py-3 text-base rounded-xl font-medium',
  };

  return (
    <button
      className={clsx(
        'inline-flex items-center justify-center font-medium transition-all duration-150 active:scale-[0.985] outline-none focus-visible:ring-2 focus-visible:ring-[var(--bc-accent)]',
        variantStyles[variant],
        sizeStyles[size],
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
};
```

---

## 3. High-Performance Chat Streaming Pattern

When streaming AI text token-by-token, avoid re-rendering prompt boxes or unrelated parent components:

```tsx
// Isolate text streaming into a memoized leaf component
import React, { memo } from 'react';

export const StreamingMessage = memo(function StreamingMessage({ 
  content, 
  isThinking 
}: { 
  content: string; 
  isThinking?: boolean; 
}) {
  return (
    <div className="flex gap-4 py-4 leading-relaxed text-[15px]">
      <div className="w-8 h-8 rounded-lg bg-[var(--bc-accent-subtle)] border border-[var(--bc-accent-border)] flex items-center justify-center shrink-0">
        <svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
          <circle cx="12" cy="12" r="8" />
        </svg>
      </div>
      <div className="flex-1 min-w-0">
        {isThinking && (
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[var(--bc-accent-subtle)] text-[var(--bc-accent)] text-xs mb-3 animate-bc-thinking">
            <span className="w-2 h-2 rounded-full bg-[var(--bc-accent)]" />
            Thinking...
          </div>
        )}
        <div className="text-[var(--bc-text-primary)] whitespace-pre-wrap">
          {content}
        </div>
      </div>
    </div>
  );
});
```

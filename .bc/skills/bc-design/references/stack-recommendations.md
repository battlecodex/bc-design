# BC Design System - Recommended Tech Stack & Libraries

Recommended production stack for building web applications with the **BC Design language**.

---

## 1. Core Stack Summary

| Layer | Recommended Library | Version / Configuration |
| :--- | :--- | :--- |
| **Framework** | **React / Next.js** (or Vue / Svelte / Vanilla) | Next.js 14 / 15 App Router |
| **Styling** | **Tailwind CSS** + **CSS Variables** | Use `tailwind.config.snippet.js` |
| **Headless UI Primitives** | **Radix UI** (`@radix-ui/react-*`) | Completely unstyled, 100% accessible |
| **Icon Library** | **Lucide Icons** (`lucide-react`) | Required: `strokeWidth={1.5}` |
| **Motion & Animation** | **Framer Motion** (`framer-motion`) | Easing: `[0.16, 1, 0.3, 1]` |
| **Typography** | Google Fonts / `@fontsource` | `Newsreader` + `Inter` (Body) |

---

## 2. Quick Package Installation

```bash
npm install lucide-react @radix-ui/react-dialog @radix-ui/react-switch @radix-ui/react-popover framer-motion clsx tailwind-merge
```

---

## 3. How to Combine the Stack (Production Example)

### BC Design Dialog with Radix UI + Lucide + Framer Motion

```tsx
import * as Dialog from '@radix-ui/react-dialog';
import * as Switch from '@radix-ui/react-switch';
import { motion } from 'framer-motion';
import { Sparkles, X } from 'lucide-react';

export function BCDesignMemoryModal({ open, onOpenChange }: { open: boolean; onOpenChange: (open: boolean) => void }) {
  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50" />
        <Dialog.Content className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-full max-w-2xl">
          <motion.div 
            initial={{ opacity: 0, scale: 0.96 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
            className="bg-[#1F1E1D] border border-white/10 rounded-2xl overflow-hidden shadow-2xl flex"
          >
            {/* Settings Left */}
            <div className="flex-1 p-8">
              <h2 className="font-serif text-2xl text-[#FAF9F5] font-medium mb-6">
                Review updates to BC Design's memory
              </h2>
              
              <div className="flex items-center justify-between py-4">
                <div>
                  <h4 className="text-sm font-medium text-white">Include sensitive topics</h4>
                  <p className="text-xs text-stone-400">You can change this anytime in settings.</p>
                </div>
                <Switch.Root className="w-11 h-6 bg-stone-700 data-[state=checked]:bg-[#D97757] rounded-full relative">
                  <Switch.Thumb className="block w-4 h-4 bg-white rounded-full transition-transform duration-200 translate-x-1 data-[state=checked]:translate-x-6" />
                </Switch.Root>
              </div>

              <button className="w-full mt-6 bg-white hover:bg-stone-200 text-stone-900 font-medium py-3 rounded-lg transition-colors">
                Save preferences
              </button>
            </div>

            {/* Organic Crayon Illustration Right */}
            <div className="w-72 bg-[#181816] flex items-center justify-center p-6 border-l border-white/5">
              {/* Organic thought bubble */}
              <svg width="180" height="180" viewBox="0 0 200 200">
                <path d="M40,100 C30,70 60,35 110,35 C160,35 185,70 175,105 C165,140 130,155 85,150 C55,145 45,120 40,100 Z" fill="#D97757" />
                <path d="M60,95 Q75,70 90,95 T120,95 T150,95" stroke="#FFFFFF" strokeWidth="6" strokeLinecap="round" />
              </svg>
            </div>
          </motion.div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

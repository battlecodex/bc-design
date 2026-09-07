# BC Design System - Icons & Illustration Guide

Guidelines for icon libraries, stroke weights, icon wells, and organic illustrations in the **BC Design Language**.

---

## 1. Recommended Icon Library: Lucide Icons

BC Design uses **monoline hairline icons with rounded terminals**. The industry standard library that matches BC Design with 99% visual fidelity is **Lucide Icons**.

### Installation

For React / Next.js:
```bash
npm install lucide-react
```

For Vue:
```bash
npm install lucide-vue-next
```

---

## 2. Icon Styling Rules (Hairline Geometry)

All icons in BC Design-style interfaces must follow these mechanical constraints:

* **Stroke Width**: `1.5px` (Crucial! Default 2px icons look too bulky and unrefined).
* **Line Caps & Joins**: Always `round`.
* **Color**: Inherit from text (`currentColor`), `--bc-text-primary`, or `--bc-text-secondary`.

### React Example

```tsx
import { Sliders, Database, Megaphone, Funnel, Compass, Code, PenTool, CircleDollarSign, Scale, Cog } from 'lucide-react';

export function RoleCard({ title, icon: Icon, isRecommended }: { title: string; icon: any; isRecommended?: boolean }) {
  return (
    <div className="bc-role-card">
      <div className="bc-role-icon">
        <Icon size={20} strokeWidth={1.5} className="text-bc-text" />
      </div>
      <div>
        <span className="font-medium text-sm">{title}</span>
        {isRecommended && <span className="bc-badge-blue ml-2">For you</span>}
      </div>
    </div>
  );
}
```

---

## 3. The Icon Well Container (`.bc-role-icon`)

Icons in cards (like the "Browse by role" grid) are housed inside a soft, elevated well:

* **Dimensions**: `40px × 40px` or `42px × 42px`.
* **Border Radius**: `8px` to `10px` (`rounded-md` / `rounded-lg`).
* **Background**:
  * Light Mode: `#F3F2EE` or `#F0EFEB`.
  * Dark Mode: `rgba(255, 255, 255, 0.06)` or `#2A2826`.
* **Border**: Delicate 1px hairline `rgba(31, 30, 27, 0.08)` (light) / `rgba(255, 255, 255, 0.08)` (dark).

---

## 4. Organic Hand-Drawn & Crayon Illustration Style

In addition to crisp monoline icons, BC Design features **tactile, organic, hand-drawn vector elements** for brand moments and feature dialogs:

### A. The BC Design Starburst (Logo)
```html
<svg width="24" height="24" viewBox="0 0 24 24" fill="none">
  <path d="M12 2L14.4 9.6L22 12L14.4 14.4L12 22L9.6 14.4L2 12L9.6 9.6L12 2Z" fill="#D97757"/>
</svg>
```

### B. The Memory Thought Bubble with Crayon Chalk Squiggle
```html
<svg width="240" height="240" viewBox="0 0 240 240" fill="none">
  <!-- Asymmetrical organic clay bubble -->
  <path d="M50 110 C35 70 75 30 135 30 C195 30 220 70 210 115 C200 160 160 180 105 175 C65 170 55 135 50 110 Z" fill="#D97757"/>
  <circle cx="45" cy="188" r="14" fill="#D97757"/>
  <circle cx="28" cy="208" r="8" fill="#D97757"/>
  
  <!-- Hand-drawn white chalk / crayon squiggle -->
  <path d="M75 118 Q90 85 108 118 T140 118 T175 118 T208 85" 
        stroke="#FFFFFF" 
        stroke-width="7" 
        stroke-linecap="round" 
        stroke-linejoin="round"
        style="filter: drop-shadow(0 1px 2px rgba(0,0,0,0.15));"/>
</svg>
```

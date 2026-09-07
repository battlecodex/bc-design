# BC Design System - Charts & Data Visualization

Comprehensive specifications, categorical color spectra, and copy-paste code snippets for **Recharts (React/Next.js), Chart.js, and D3.js** styled in the **BC Design / BC Design Aesthetic**.

---

## 1. The BC Design Categorical Color Spectrum

Never use neon RGB or generic high-contrast rainbow charts. BC Design's charts use an **earth-toned, humanist categorical spectrum** that remains legible in both light parchment and dark espresso modes:

```ts
export const BCDesignChartPalette = {
  // Primary Categorical Series
  series1: '#D97757', // Signature Terracotta (Hero metric, active run)
  series2: '#E09F3E', // Warm Amber (Secondary metric, volume)
  series3: '#7D8A68', // Eucalyptus Sage (Positive growth, retention)
  series4: '#34526F', // Scholarly Navy (Benchmarks, historical averages)
  series5: '#AA4F32', // Burnt Sienna (High-priority events)
  series6: '#8C7A6B', // Muted Taupe (Baseline, reference data)

  // Gradients & Fills
  fillTerracotta: 'rgba(217, 119, 87, 0.12)',
  fillAmber: 'rgba(224, 159, 62, 0.12)',
  fillSage: 'rgba(125, 138, 104, 0.12)',

  // Grid & Axis
  gridLight: 'rgba(31, 30, 27, 0.06)',
  gridDark: 'rgba(250, 249, 245, 0.06)',
  axisTextLight: '#6B6760',
  axisTextDark: '#A39E93',
};
```

---

## 2. Chart Types Directory

| Chart Type | Primary Use Case | Recommended Palette | Library Options |
| :--- | :--- | :--- | :--- |
| **1. Area / Line Chart** | Token generation over time, streaming velocity, latency | Terracotta stroke + translucent gradient fill | Recharts / Chart.js |
| **2. Bar / Column Chart**| Cost per model, capability benchmarks, role distribution | Grouped: Terracotta, Amber, Sage, Navy | Recharts / Chart.js |
| **3. Donut / Pie Chart** | Context window memory utilization, prompt vs completion | Multi-segment Earth spectrum with center label | Recharts / Chart.js |
| **4. Heatmap Matrix** | API traffic density (hour vs day), code change hotspots | 5-stop Parchment-to-Terracotta ramp | D3.js / SVG |
| **5. Sparklines & Tickers**| Compact table metric, model uptime ticker | Monoline 1.5px with pulsing live dot | SVG / Recharts |
| **6. Scatter / Bubble** | Model evaluation: Quality score vs inference speed | Clustered translucent bubbles | Recharts / D3.js |

---

## 3. Copy-Paste Code Implementations

### A. Recharts Smooth Area Chart (React / Next.js)

```tsx
import React from 'react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

const data = [
  { time: '09:00', tokens: 3200 },
  { time: '10:00', tokens: 6800 },
  { time: '11:00', tokens: 5400 },
  { time: '12:00', tokens: 11200 },
  { time: '13:00', tokens: 9400 },
  { time: '14:00', tokens: 14800 },
];

export function BCDesignVelocityChart() {
  return (
    <div className="bg-[var(--bc-surface)] border border-[var(--bc-border)] rounded-2xl p-6 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="font-serif text-lg font-medium text-[var(--bc-text-primary)]">Token Generation Velocity</h3>
          <p className="text-xs text-[var(--bc-text-secondary)]">Output tokens per minute across active agents</p>
        </div>
        <span className="text-xs font-mono bg-[var(--bc-bg-subtle)] text-[var(--bc-accent)] px-2.5 py-1 rounded-full">
          Live: 14.8k tok/m
        </span>
      </div>

      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="bcGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#D97757" stopOpacity={0.25} />
                <stop offset="95%" stopColor="#D97757" stopOpacity={0.0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--bc-border)" />
            <XAxis dataKey="time" tickLine={false} axisLine={false} tick={{ fill: 'var(--bc-text-secondary)', fontSize: 12 }} />
            <YAxis tickLine={false} axisLine={false} tick={{ fill: 'var(--bc-text-secondary)', fontSize: 12 }} />
            <Tooltip
              contentStyle={{
                backgroundColor: 'var(--bc-surface)',
                border: '1px solid var(--bc-border-strong)',
                borderRadius: '8px',
                boxShadow: 'var(--bc-shadow-md)',
                color: 'var(--bc-text-primary)',
                fontFamily: 'Inter, sans-serif',
                fontSize: '13px',
              }}
            />
            <Area
              type="monotone"
              dataKey="tokens"
              stroke="#D97757"
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#bcGradient)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
```

---

### B. Chart.js Categorical Bar & Donut Configuration

```javascript
// Reusable BC Design Chart.js Preset
export const bcChartJsPreset = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
      align: 'end',
      labels: {
        color: '#6B6760',
        font: { family: 'Inter', size: 12, weight: '500' },
        usePointStyle: true,
        pointStyle: 'circle',
        boxWidth: 8,
      },
    },
    tooltip: {
      backgroundColor: '#1F1E1B',
      titleFont: { family: 'Newsreader', size: 14, weight: '500' },
      bodyFont: { family: 'Inter', size: 12 },
      padding: 12,
      cornerRadius: 8,
      borderColor: 'rgba(255, 255, 255, 0.1)',
      borderWidth: 1,
    },
  },
  scales: {
    x: {
      grid: { display: false },
      ticks: { color: '#99948B', font: { family: 'Inter', size: 12 } },
      border: { display: false },
    },
    y: {
      grid: { color: 'rgba(31, 30, 27, 0.06)' },
      ticks: { color: '#99948B', font: { family: 'Inter', size: 12 } },
      border: { display: false },
    },
  },
};
```

---

### C. Heatmap Intensity Scale (5-Stop Parchment Ramp)

For API traffic or token heatmaps:

| Intensity Step | Light Mode Hex | Dark Mode Hex | Purpose |
| :--- | :--- | :--- | :--- |
| **0 (Empty)** | `#FAF9F5` (Base) | `#20201D` | Zero calls / inactive cell |
| **1 (Low)** | `#F5E8E1` | `#2D211C` | Low volume (< 10 requests) |
| **2 (Medium)** | `#EBC8B8` | `#4B2F24` | Moderate traffic |
| **3 (High)** | `#DF9F86` | `#7D4431` | High load |
| **4 (Peak)** | `#D97757` (Solid Terra) | `#E28466` | Maximum throughput |

---

## 4. Accessibility & A11y Best Practices

1. **Never Rely on Color Alone**: Always pair color fills with data tooltips, visible value labels, or distinct hatch/stroke patterns for colorblind users.
2. **Accessible Contrast**: Ensure all axis labels and legends meet WCAG AA (minimum 4.5:1 on their corresponding background).
3. **Screen Reader Tables**: Provide a visually-hidden `<table className="sr-only">` counterpart alongside SVG charts so screen readers can consume the raw tabular numbers.
4. **Interactive Focus Rings**: Interactive chart points or bars must have a visible `:focus-visible` outline (`box-shadow: 0 0 0 2px var(--bc-accent)`).

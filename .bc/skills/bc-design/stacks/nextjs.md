# BC Design System for Next.js

Implementation guide for **Next.js 14 / 15 App Router**, Server Components, SSR hydration, and font optimization.

---

## 1. Zero-CLS Font Optimization (`app/layout.tsx`)

Load `Newsreader` and `Inter` using `next/font/google` to achieve **zero layout shift** and self-hosted privacy:

```tsx
// app/layout.tsx
import type { Metadata } from 'next';
import { Inter, Newsreader, JetBrains_Mono } from 'next/font/google';
import '@/styles/globals.css';
import '@/.agents/skills/bc-design/references/tokens.css';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-sans',
  display: 'swap',
});

const newsreader = Newsreader({
  subsets: ['latin'],
  style: ['normal', 'italic'],
  variable: '--font-serif',
  display: 'swap',
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-mono',
  display: 'swap',
});

export const metadata: Metadata = {
  title: 'BC Design Workspace',
  description: 'Powered by BC Design BC Design Language',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${inter.variable} ${newsreader.variable} ${jetbrainsMono.variable}`}>
      <head>
        {/* Prevent flash of light/dark theme on first load */}
        <script
          dangerouslySetInnerHTML={{
            __html: `
              (function() {
                try {
                  var saved = localStorage.getItem('bc-theme');
                  var isDark = saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches);
                  if (isDark) {
                    document.documentElement.setAttribute('data-theme', 'dark');
                    document.documentElement.classList.add('dark');
                  } else {
                    document.documentElement.setAttribute('data-theme', 'light');
                  }
                } catch (e) {}
              })();
            `,
          }}
        />
      </head>
      <body className="bg-[var(--bc-bg)] text-[var(--bc-text-primary)] font-sans antialiased min-h-screen">
        {children}
      </body>
    </html>
  );
}
```

---

## 2. Server-Sent Events (SSE) AI Streaming with Thinking State

Example Route Handler streaming tokens to a BC Design frontend:

```ts
// app/api/chat/route.ts
import { NextResponse } from 'next/server';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const encoder = new TextEncoder();
  const stream = new ReadableStream({
    async start(controller) {
      // 1. Emit thinking state
      controller.enqueue(encoder.encode(`event: status\ndata: {"isThinking": true}\n\n`));

      // Simulate synthesis delay
      await new Promise((r) => setTimeout(r, 800));

      // 2. Stream synthesized text
      controller.enqueue(encoder.encode(`event: status\ndata: {"isThinking": false}\n\n`));
      const tokens = ["Certainly! ", "Here ", "is ", "the ", "BC Design ", "architecture."];
      for (const token of tokens) {
        controller.enqueue(encoder.encode(`event: token\ndata: ${JSON.stringify({ text: token })}\n\n`));
        await new Promise((r) => setTimeout(r, 60));
      }
      controller.close();
    },
  });

  return new NextResponse(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      Connection: 'keep-alive',
    },
  });
}

---

## 3. 3D Spatial & WebGL in Next.js App Router (SSR Safety)

Three.js, WebGL shaders, and Canvas 2D contexts depend on browser globals (`window`, `document`, `navigator`) that do not exist during Next.js Server-Side Rendering.

### Pattern: Dynamic Client Boundary (`ssr: false`)

Isolate the spatial component into a dedicated client module and import it dynamically to prevent SSR hydration crashes:

```tsx
// components/SpatialStage.tsx
'use client';

import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

export default function SpatialStage() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (!canvasRef.current) return;
    const canvas = canvasRef.current;

    // 1. Scene & Renderer with DPR Capping
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 100);
    camera.position.set(0, 0.5, 7.5);

    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // 2. Add lighting and subject-grounded 3D artifact
    const ambient = new THREE.AmbientLight(0xfaf9f5, 1.2);
    scene.add(ambient);

    let animationFrameId: number;
    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      renderer.render(scene, camera);
    };
    animate();

    const handleResize = () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    };
    window.addEventListener('resize', handleResize);

    // 3. Mandatory Cleanup on Unmount (GPU Memory Safety)
    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener('resize', handleResize);
      renderer.dispose();
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 w-full h-full pointer-events-none z-[1]"
      aria-hidden="true"
    />
  );
}
```

Then in your page:

```tsx
// app/page.tsx
import dynamic from 'next/dynamic';

const SpatialStage = dynamic(() => import('@/components/SpatialStage'), {
  ssr: false,
  loading: () => <div className="fixed inset-0 bg-[var(--bc-bg)] z-[1]" />,
});

export default function HomePage() {
  return (
    <main className="relative min-h-screen">
      <SpatialStage />
      <div className="relative z-10 p-8">
        {/* Editorial content */}
      </div>
    </main>
  );
}
```
```

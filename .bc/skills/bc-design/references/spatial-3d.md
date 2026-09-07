# BC Design System - Spatial 3D & Interactive Scrollytelling

> Architecture, ergonomics, and engineering standards for integrating scroll-driven 3D product visualization, exploded views, and tactile spatial artifacts into the BC Design editorial language.

---

## 1. Aesthetic Philosophy: Subject Grounding vs. Generic Novelty

Typical AI-generated 3D websites rely on repetitive cyberpunk tropes: saturated neon glows (`#7C3AED`), floating geometric spheres, and glossy gadget renders disconnected from the product's actual purpose.

BC Design rejects ungrounded novelty. 3D interaction must be treated as an **interactive scientific codex, an architectural monograph, or an archival physical instrument**:

| Dimension | Generic 3D Web (Avoid) | BC Design Subject-Grounded Standard |
| :--- | :--- | :--- |
| **Canvas** | Pitch black with purple/cyan neon halos | Warm neutral parchment, espresso soot, slate, or ivory matched to the product palette |
| **Materials** | Highly specular plastic, chrome, laser emissives | Matte ceramic, brushed bronze, paper grain, titanium, slate, linen, or glass |
| **Lighting** | Multi-point colored lasers with harsh specular hotspots | Soft directional daylight (45° azimuth) with rich ambient occlusion |
| **Callouts** | Floating glow cards with rounded-full neon badges | 1px hairline measurement brackets with monoline 1.5px pins |
| **Typography** | Loud geometric sans-serif screaming features | Editorial display serif or technical sans paired with tabular monospace telemetry |
| **Motion Physics** | Disorienting continuous spin or spring bounces | Intentional damped friction (`cubic-bezier(0.16, 1, 0.3, 1)`), user-anchored scrub |
| **Subject Grounding** | Floating gadgets disconnected from user purpose | Domain-authentic artifacts: codices, supply-chain hubs, yield curves, architectural volumes |

---

## 1.1 Sector-Grounded Spatial Metaphors

In BC Design, **3D is never an arbitrary decorative wallpaper**. An interface representing an educational academy must not show an astronomical galaxy or spinning spaceship; an enterprise ERP must not show a floating cyberpunk sphere.

Every sector has an authentic, literal or mechanical 3D physical object:

| Sector / Industry | Authentic 3D Spatial Artifact | Physical Metaphor & Geometry | Avoid (Generic clichés without subject ground) |
| :--- | :--- | :--- | :--- |
| **Education / School** | **3D Open Codex / Book of Knowledge** | Curved turning vellum leaves, hardbound linen cover, gold leaf ribbon, academic folios | *Astronomy planets, space rockets, floating cartoon graduation caps* |
| **Enterprise ERP** | **Modular Supply-Chain Pipeline Hub** | 3D interlocking modular stoneware cubes (Procurement, Inventory, Logistics, Ledger) with data pulse conduits | *Spinning globe wireframes, floating pie charts, generic particle clouds* |
| **HRM (People Ops)** | **Dynamic Talent Topology Tree** | Hierarchical human capital constellation with role clusters, team orbits, and career progression vectors | *Cartoon avatar heads, stock photo circles, bouncy balloon trees* |
| **Fintech / Crypto** | **Volumetric Yield Curve & Settlement Lattice** | 3D order-book depth terrain, precision bullion ingot geometry, cryptographic ledger blocks | *Cartoon spinning gold coins, neon dollar signs, arcade slot machine effects* |
| **Healthcare / Medical** | **Vitality Pulse Waveform & Cellular Osmosis Mesh** | Procedural biocompatible heartbeat ribbon, organic cellular membrane lattice, clinical matte ceramic | *Flying cartoon stethoscopes, spinning pills, neon red cross symbols* |
| **Pet Services / Vet** | **Fauna Biometric Collar & Pulse Arc** | Organic companion pulse ring, paw-track biomechanical curvature, warm amber fur-toned lighting | *Cartoon bouncing dog bones, spinning paw stamps, barking emoji cutouts* |
| **SaaS / B2B Cloud** | **Unified Metric Command Engine Monolith** | Precision telemetry extrusion monolith with glowing KPI pipeline trenches and low-poly substrate | *Generic purple floating cards, cartoon cloud clipart with lightning* |
| **AI / Synthetic Intelligence** | **Latent Tensor Field & Attention Convergence** | High-dimensional dynamic dot-matrix with parabolic attention arcs converging into a reasoning core | *Glowing cyborg skulls, robot eyeballs, neon brain clipart, sci-fi lasers* |
| **E-commerce / Retail** | **Spatial Product Pedestal & Assembly** | 360° rotating material plinth, exploded packaging geometry, tactile textile/leather shaders | *Spinning shopping carts, floating gift boxes with ribbons, flashing badges* |
| **Real Estate / Architecture**| **Volumetric Architectural BIM Massing** | Architectural massing volume, exploded isometric floorplates, seasonal sunpath shadow simulation | *Cartoon house roofs with chimney smoke, spinning real-estate keys* |
| **Creative Agency / Studio** | **Optical Caustic Glass Prism & Refraction Mesh**| Real-time chromatic dispersion glass prism splitting white daylight into an editorial spectrum | *Random glossy floating chrome spheres, generic neon gradient blobs* |
| **Gaming / Interactive** | **Procedural Polyhedral Spatial Terrain** | Low-poly faceted topographical hex-grid with real-time dynamic elevation contouring | *Pixelated 8-bit joystick clipart, generic gamer skulls, rainbow RGB glows* |
| **Food & Restaurant** | **Artisanal Terracotta Vessel & Flavor Herbarium**| Warm matte ceramic dishware, laminar thermal steam dissipation, botanical ingredient geometry | *Spinning cartoon hamburgers, pizza slices, neon chef hats, flying forks* |
| **Fitness / Wellness** | **Kinetic Musculoskeletal Tension Lines** | Biomechanical kinetic gyroscope, caloric burn vector lines, athletic carbon-fiber mesh | *Cartoon bouncing dumbbells, spinning gym shoes, flames of fire around biceps* |
| **Travel & Hospitality** | **Topographical Elevation Contour & Flight Arcs**| Precision elevation contour relief model, orthographic great-circle transit curves | *Cartoon airplanes with cloud puffs, spinning beach balls, sunglasses* |
| **NFT / Web3** | **Cryptographic Hash Cube & State Machine** | Interlocking deterministic block lattice with verifiable transaction hashes and amber bloom | *Pixelated cartoon ape heads, neon casino roulette wheels, moon rockets* |
| **Beauty & Spa / Luxury** | **Viscous Emulsion Waveform & Ceramic Droplet** | Liquid silk surface tension shaders, pearlescent alabaster vessel, calm wave propagation | *Cartoon lipstick tubes, spinning perfume mist bottles, glittering sparkles* |
| **Developer Tools / DevOps** | **Distributed Server Blade & Packet Conduits** | Isometric server blade chassis, low-latency packet conduits, terminal monolith substrate | *Generic floating cartoon gears, wrench and screwdriver crossed icons* |
| **Entertainment / Media** | **Holographic Audio-Visual Waveguide** | Volumetric frequency spectrum ribbons, harmonic acoustic ripple fields, cinematic focal depth | *Spinning film reels, clapperboards violently clapping, popcorn tubs* |
| **Legal / Compliance** | **Balanced Precision Scales & Wax-Sealed Codex**| Burnished brass balance scales with micro-deflection, archival law charter with tactile seal | *Wooden auction gavels slamming violently, cartoon scales tipped 90 deg* |
| **Events & Conferences** | **Spatial Amphitheater Plinth & Stage Volume** | Concentric tiered acoustic amphitheater seating model, dynamic spotlight focus cones | *Party confetti cannons, spinning helium balloons, flying calendar pages* |

---

## 2. Technical Architectures for 3D Scrollytelling

### Pattern A: HTML5 Canvas Frame Sequencer
When pre-rendered 3D frames are preferred over runtime WebGL calculation, rendering an image frame sequence (e.g. 60–120 WebP frames) onto an HTML5 `<canvas>` provides predictable frame stepping without 3D model parsing overhead.

```javascript
// Frame Sequencer Engine
const canvas = document.getElementById("spatialCanvas");
const ctx = canvas.getContext("2d");
const totalFrames = 90;
const frames = [];

// Preload frames with high-DPI scaling
function preloadFrames() {
  for (let i = 1; i <= totalFrames; i++) {
    const img = new Image();
    const padded = String(i).padStart(4, "0");
    img.src = `./assets/frames/subject_${padded}.webp`;
    frames.push(img);
  }
}

// Map scroll progress (0.0 to 1.0) to frame index
function renderFrame(progress) {
  const frameIndex = Math.min(
    totalFrames - 1,
    Math.max(0, Math.floor(progress * totalFrames))
  );
  const img = frames[frameIndex];
  if (img && img.complete) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawContained(ctx, img, canvas.width, canvas.height);
  }
}
```

### Pattern B: Procedural Three.js / WebGL Spatial Stage
When real-time interaction (cursor tilt, orbit control, live lighting adjustments) is required, use Three.js configured with physical materials tailored to the subject brief:

```javascript
// Subject-tailored physical material setup
const subjectMaterial = new THREE.MeshStandardMaterial({
  color: 0xD97757,       // Grounded accent token or subject material color
  roughness: 0.65,       // Matte tactile finish, low specular shine
  metalness: 0.12,
});

// Diffused ambient and directional light matching the product palette
const ambientLight = new THREE.AmbientLight(0xffffff, 0.9);
const directionalKey = new THREE.DirectionalLight(0xfff6ee, 1.4);
directionalKey.position.set(5, 8, 4);
```

---

## 3. The Pinned Scrollytelling Stage Layout

A standard BC Design spatial section uses a sticky 100vh viewport pinned while narrative chapters scroll past:

```html
<section class="bc-spatial-showcase" id="spatialShowcase">
  <!-- Pinned Viewport (Remains in view) -->
  <div class="bc-spatial-stage-sticky">
    <div class="spatial-canvas-container">
      <canvas id="spatialCanvas" width="1280" height="720" class="pointer-events-none"></canvas>
    </div>

    <!-- Active Hairline Telemetry Overlay -->
    <div class="spatial-telemetry-hud" aria-live="polite">
      <div class="telemetry-bracket">
        <span class="telemetry-index" id="hudChapter">CHAPTER 01</span>
        <span class="telemetry-coord" id="hudCoord">AXIS: [X: 0.00, Y: 0.00, Z: 0.00]</span>
      </div>
      <div class="telemetry-annotations" id="hudAnnotation">
        <h3 class="telemetry-title" id="hudTitle">Subject Monolith</h3>
        <p class="telemetry-caption" id="hudCaption">Tactile casing crafted with archival precision.</p>
      </div>
    </div>
  </div>

  <!-- Scroll Progress Track (Controls scrub position) -->
  <div class="bc-spatial-scroll-track">
    <div class="scroll-milestone" data-step="0" style="height: 100vh;"></div>
    <div class="scroll-milestone" data-step="1" style="height: 100vh;"></div>
    <div class="scroll-milestone" data-step="2" style="height: 100vh;"></div>
    <div class="scroll-milestone" data-step="3" style="height: 100vh;"></div>
  </div>
</section>
```

---

## 4. Technical Baseline vs. Optional Aesthetic Moments

### Mandatory Technical Baseline (Enforced by Quality Gates)

1. **Hardware DPR Capping**: Always cap device pixel ratio with `Math.min(window.devicePixelRatio, 2)`. Uncapped 3x or 4x Retina displays force GPUs to render 8K fragment shaders, leading to thermal throttling and battery drain.
2. **Pointer Pass-Through**: Background spatial canvases must include `pointer-events: none` so that links, buttons, and text selections in the hero column remain unobstructed.
3. **Zero Text Overlap**: Restrict the interactive text column to `max-width: min(560px, 45vw)` and position 3D geometries in the opposite hemisphere ($X \ge 0.5$) so typography never collides with 3D meshes.
4. **Reduced Motion Compliance**: When `prefers-reduced-motion: reduce` is active:
   - Freeze continuous ambient rotation into a calm, static composition.
   - Disable automatic camera scrub snapping.
   - Provide explicit chapter buttons or step controls for manual inspection.
5. **GPU Lifecycle Teardown**: In single-page applications (React, Vue, Svelte), explicitly cancel `requestAnimationFrame`, traverse the scene to dispose geometries, materials, and textures, and call `renderer.dispose()` and `renderer.forceContextLoss()`.
6. **Measurable Performance Budgets**:
   - Draw calls: $\le 50$ per frame.
   - Geometry complexity: $\le 100\text{k}$ triangles.
   - Texture resolution: $\le 2048 \times 2048\text{px}$.
   - Initial asset payload: $\le 2.5\text{MB}$.

### Progressive Enhancement & Fallbacks

When WebGL context creation fails or hardware acceleration is unavailable:
1. Render a clean fallback SVG or high-resolution editorial photography of the subject artifact.
2. Display an informative, calm fallback message without breaking layout or throwing uncaught exceptions.
3. Keep the content narrative and interaction flow 100% accessible via standard HTML keyboard navigation.

---

## 5. Mathematical Spatial Engine & Shader Presets

The BC Design Spatial Engine integrates mathematical shaders and multi-plane scrollytelling architectures retoned to subject-grounded standards:

### Layered Depth Architecture
Authentic spatial depth is structured across distinct optical layers:
- **Layer 0 (`#gl-canvas`)**: Background WebGL substrate or canvas with subject-grounded depth.
- **Layer 1 (3D Ground / Wordmark)**: Typographic or architectural baseline positioned in 3D world space.
- **Layer 2 (`.fg-plane`)**: Subject artifact planes (e.g. isometric floorplates, technical instruments, biological membranes) anchored to the camera view with differential parallax.
- **Layer 3 (Ambient Radiance)**: Soft directional lighting with balanced contrast.
- **Layer 4 (UI & Telemetry)**: Editorial headlines, monospace telemetry brackets, interactive chapter chips, and milestone rails (`z-index: 10` or higher).

### Mathematical Shader Primitives
- **Ribbon Field (`ribbon-field`)**: Sinuous ribbon wave equations resolved through dynamic dot-matrix rasterization.
- **Predictive Arc (`predictive-arc`)**: Parabolic attention arcs rendered via additive particle rasterization.
- **Modular Hub (`erp-spatial`)**: Interlocking multi-division geometric cubes with synchronized telemetry conduits.
- **Open Codex (`school-spatial`)**: Interactive curved vellum folios with Euclidean geometry plates and bookmark ribbon.

---

## 6. CLI Spatial Generator Usage

The BC Design CLI provides built-in spatial code generation:

```bash
# List available spatial presets and their sector applications
python .agents/skills/bc-design/scripts/bc_design.py --spatial list

# Generate Open Codex standalone HTML for an educational institution
python .agents/skills/bc-design/scripts/bc_design.py --spatial school-spatial -o examples/school-spatial.html

# Generate Enterprise ERP Modular Hub
python .agents/skills/bc-design/scripts/bc_design.py --spatial erp-spatial -o examples/bc-erp-spatial.html

# Generate Ribbon Field standalone component
python .agents/skills/bc-design/scripts/bc_design.py --spatial ribbon-field --spatial-palette terracotta -o examples/bc-ribbon-field.html

# Generate Predictive Arc React component
python .agents/skills/bc-design/scripts/bc_design.py --spatial predictive-arc --spatial-format react -o src/components/PredictiveArc.tsx
```

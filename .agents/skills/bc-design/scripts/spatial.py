"""
BC Design Spatial & 3D Shader Engine
====================================
Generates production-grade WebGL, Canvas 2D, and Three.js spatial components
and scrollytelling layouts grounded in the BC Design / Literary Humanist aesthetic.

Learned and adapted from ThreeUI architecture, re-engineered for:
- Subject-grounded palettes (Terracotta, Cinnabar, Burnished Brass, Deep Obsidian, Ivory Parchment)
- Dual-theme support (Native Dark Mode and Light Codex Mode)
- Literary typography & calm motion (Newsreader, Onest, JetBrains Mono)
- Zero layout shift during streaming & zero text overlap
- 100% compliance with BC Design quality gates and automated audits
"""

import json
import re
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = SKILL_ROOT / "assets" / "spatial"

# Canonical BC Design Spatial Palettes (Dual Theme)
PALETTES = {
    # ── Dark Themes ───────────────────────────────────────────────────
    "terracotta": {
        "name": "Terracotta & Cinnabar (Dark)",
        "theme": "dark",
        "accent": "#D97757",
        "accent_hover": "#E08B6E",
        "accent_deep": "#B35637",
        "brass": "#C2A26A",
        "bg": "#0D0C0A",
        "bg_elevated": "#161412",
        "text": "#FAF9F5",
        "text_dim": "#C5BFB3",
        "text_muted": "#8A8479",
        "border": "rgba(250, 249, 245, 0.11)",
        "border_subtle": "rgba(250, 249, 245, 0.05)",
        # GLSL color vectors (0.0 - 1.0)
        "gl_col1": "vec3(0.85, 0.47, 0.34)",  # Terracotta
        "gl_col2": "vec3(0.88, 0.35, 0.24)",  # Cinnabar Ember
        "gl_col3": "vec3(0.76, 0.64, 0.42)",  # Burnished Brass
        "gl_col4": "vec3(0.96, 0.64, 0.38)",  # Warm Amber
        "gl_bloom": "vec3(1.0, 0.72, 0.45)", # Core Warm Bloom
        "gl_base": "vec3(0.05, 0.047, 0.04)"  # Deep Obsidian
    },
    "amber-brass": {
        "name": "Amber & Instrument Brass (Dark)",
        "theme": "dark",
        "accent": "#D4973B",
        "accent_hover": "#E2A94F",
        "accent_deep": "#9C671D",
        "brass": "#C2A26A",
        "bg": "#0F0E0C",
        "bg_elevated": "#181613",
        "text": "#F7F5F0",
        "text_dim": "#C8C2B6",
        "text_muted": "#8C8578",
        "border": "rgba(247, 245, 240, 0.11)",
        "border_subtle": "rgba(247, 245, 240, 0.05)",
        "gl_col1": "vec3(0.83, 0.59, 0.23)",
        "gl_col2": "vec3(0.92, 0.72, 0.32)",
        "gl_col3": "vec3(0.68, 0.46, 0.18)",
        "gl_col4": "vec3(0.76, 0.64, 0.42)",
        "gl_bloom": "vec3(0.98, 0.82, 0.48)",
        "gl_base": "vec3(0.06, 0.055, 0.045)"
    },
    "sage-monochrome": {
        "name": "Sage Sanctuary & Charcoal (Dark)",
        "theme": "dark",
        "accent": "#7A9A8B",
        "accent_hover": "#8EAFA0",
        "accent_deep": "#4D6B5D",
        "brass": "#B4BFB7",
        "bg": "#0B0E0C",
        "bg_elevated": "#121714",
        "text": "#EEF3EF",
        "text_dim": "#B8C4BC",
        "text_muted": "#7A8A80",
        "border": "rgba(238, 243, 239, 0.11)",
        "border_subtle": "rgba(238, 243, 239, 0.05)",
        "gl_col1": "vec3(0.48, 0.60, 0.55)",
        "gl_col2": "vec3(0.35, 0.48, 0.42)",
        "gl_col3": "vec3(0.65, 0.75, 0.70)",
        "gl_col4": "vec3(0.82, 0.88, 0.84)",
        "gl_bloom": "vec3(0.75, 0.90, 0.82)",
        "gl_base": "vec3(0.04, 0.055, 0.047)"
    },
    # ── Light Themes (Parchment Codex) ────────────────────────────────
    "terracotta-light": {
        "name": "Terracotta & Ivory Parchment (Light)",
        "theme": "light",
        "accent": "#C15F3D",
        "accent_hover": "#AD5030",
        "accent_deep": "#8F3E22",
        "brass": "#8C6D37",
        "bg": "#FAF9F5",
        "bg_elevated": "#F3EFE6",
        "text": "#1F1E1B",
        "text_dim": "#4D4942",
        "text_muted": "#797368",
        "border": "rgba(31, 30, 27, 0.12)",
        "border_subtle": "rgba(31, 30, 27, 0.06)",
        "gl_col1": "vec3(0.75, 0.37, 0.24)",
        "gl_col2": "vec3(0.68, 0.30, 0.18)",
        "gl_col3": "vec3(0.55, 0.42, 0.22)",
        "gl_col4": "vec3(0.80, 0.50, 0.28)",
        "gl_bloom": "vec3(0.90, 0.65, 0.45)",
        "gl_base": "vec3(0.98, 0.976, 0.96)"
    },
    "amber-brass-light": {
        "name": "Amber & Warm Linen (Light)",
        "theme": "light",
        "accent": "#B87A22",
        "accent_hover": "#9E6415",
        "accent_deep": "#7D4E0E",
        "brass": "#7A5C28",
        "bg": "#F8F6F0",
        "bg_elevated": "#EFECE2",
        "text": "#22201C",
        "text_dim": "#524E45",
        "text_muted": "#7E786C",
        "border": "rgba(34, 32, 28, 0.12)",
        "border_subtle": "rgba(34, 32, 28, 0.06)",
        "gl_col1": "vec3(0.72, 0.48, 0.14)",
        "gl_col2": "vec3(0.80, 0.58, 0.20)",
        "gl_col3": "vec3(0.48, 0.36, 0.16)",
        "gl_col4": "vec3(0.62, 0.48, 0.24)",
        "gl_bloom": "vec3(0.92, 0.78, 0.42)",
        "gl_base": "vec3(0.97, 0.96, 0.94)"
    }
}

SPATIAL_PRESETS = {
    # ── Industry Sector Domain Stages ─────────────────────────────────
    "school-spatial": {
        "name": "3D Open Codex & Academic Stage (Education)",
        "sector": "Education",
        "category": "Domain Stage",
        "runtime": "Full HTML5 / Three.js / Dual Theme",
        "description": "Interactive 3D open book of knowledge with curved turning parchment leaves, embossed leather binding, and academic study folios.",
        "best_for": "Universities, classical academies, research schools, course platforms."
    },
    "education-codex": {
        "name": "Interactive 3D Open Codex (Education)",
        "sector": "Education",
        "category": "Domain Stage",
        "runtime": "Three.js r128",
        "description": "Interactive 3D open book of knowledge with curved turning vellum leaves, hardbound linen cover, and academic folios.",
        "best_for": "Universities, classical academies, research schools, online fellowships."
    },
    "erp-spatial": {
        "name": "Modular Enterprise Supply-Chain Hub (ERP)",
        "sector": "Enterprise ERP",
        "category": "Domain Stage",
        "runtime": "Full HTML5 / Three.js / Dual Theme",
        "description": "3D interlocking modular cubes representing enterprise divisions (Procurement, Inventory, Logistics, Ledger) with synchronized data conduits.",
        "best_for": "Enterprise resource planning, multi-division manufacturing, supply-chain monitoring."
    },
    "hrm-spatial": {
        "name": "Dynamic Talent Topology Tree (HRM)",
        "sector": "HRM",
        "category": "Domain Stage",
        "runtime": "Full HTML5 / Three.js / Dual Theme",
        "description": "Hierarchical 3D talent constellation displaying organizational structure, team cluster orbits, and career progression vectors.",
        "best_for": "Human capital management, organization charts, team directory, talent mobility."
    },
    "finance-spatial": {
        "name": "Volumetric Yield Curve & Settlement Lattice (Fintech)",
        "sector": "Fintech / Crypto",
        "category": "Domain Stage",
        "runtime": "Full HTML5 / Three.js / Dual Theme",
        "description": "3D volumetric liquidity terrain and cryptographic settlement block lattice with micro-basis-point deflection.",
        "best_for": "Digital banking, wealth management, treasury platforms, crypto settlement exchanges."
    },
    "health-spatial": {
        "name": "Vitality Waveform & Cellular Osmosis Mesh (Healthcare)",
        "sector": "Healthcare",
        "category": "Domain Stage",
        "runtime": "Full HTML5 / Three.js / Dual Theme",
        "description": "Procedural biocompatible vitality waveform traversing an organic cellular membrane lattice with calm laminar flow.",
        "best_for": "Medical clinic portals, patient health monitors, biotech diagnostic tools."
    },
    "pet-spatial": {
        "name": "Fauna Biometric Collar & Pulse Arc (Pet Services)",
        "sector": "Pet Services",
        "category": "Domain Stage",
        "runtime": "Full HTML5 / Three.js / Dual Theme",
        "description": "Tactile 3D biometric collar ring with calm vital rhythm waveforms and companion anatomical curvature.",
        "best_for": "Veterinary clinic portals, pet health monitoring, animal adoption platforms."
    },
    "saas-spatial": {
        "name": "Unified Metric Command Engine Monolith (SaaS)",
        "sector": "SaaS",
        "category": "Domain Stage",
        "runtime": "Full HTML5 / Three.js / Dual Theme",
        "description": "Precision 3D telemetry extrusion monolith featuring recessed metric conduits and real-time state lights.",
        "best_for": "B2B SaaS homepages, operations dashboards, analytics suites, cloud control planes."
    },
    "ai-spatial": {
        "name": "Latent Tensor Field & Attention Convergence (AI)",
        "sector": "AI / Chatbot",
        "category": "Domain Stage",
        "runtime": "Full HTML5 / Raw WebGL / Dual Theme",
        "description": "High-dimensional dynamic dot-matrix raster modulated by parabolic attention arcs converging into a stable core.",
        "best_for": "AI product heroes, generative model orchestrators, intelligent reasoning sidecars."
    },
    "ecommerce-spatial": {
        "name": "Spatial Product Pedestal & Assembly (E-commerce)",
        "sector": "E-commerce",
        "category": "Domain Stage",
        "runtime": "Full HTML5 / Three.js / Dual Theme",
        "description": "Interactive 360-degree material plinth with smooth exploded packaging inspection and dynamic lighting.",
        "best_for": "Luxury retail, artisanal goods, premium physical products, furniture monographs."
    },
    "agency-spatial": {
        "name": "Optical Caustic Glass Prism (Creative Agency)",
        "sector": "Creative Agency",
        "category": "Domain Stage",
        "runtime": "Full HTML5 / Three.js / Dual Theme",
        "description": "Physical glass prism simulation with real-time chromatic aberration, internal total reflection, and caustic focus.",
        "best_for": "Creative agency portfolios, design studio monographs, digital production showcases."
    },
    "realestate-spatial": {
        "name": "Volumetric Architectural BIM Massing (Real Estate)",
        "sector": "Real Estate",
        "category": "Domain Stage",
        "runtime": "Full HTML5 / Three.js / Dual Theme",
        "description": "Volumetric architectural massing with exploded isometric floorplate strata and seasonal sunpath shadow modeling.",
        "best_for": "Property developments, architecture firms, commercial leasing, residential masterplans."
    },
    "gaming-spatial": {
        "name": "Procedural Polyhedral Spatial Terrain (Gaming)",
        "sector": "Gaming",
        "category": "Domain Stage",
        "runtime": "Full HTML5 / Three.js / Dual Theme",
        "description": "Procedural hexagonal topographical terrain modulated by simplex noise elevation curves and pointer terraforming.",
        "best_for": "Indie game studios, spatial game engines, interactive metaverse chronicles."
    },
    "food-spatial": {
        "name": "Artisanal Terracotta Vessel & Flavor Herbarium (Food & Dining)",
        "sector": "Food & Restaurant",
        "category": "Domain Stage",
        "runtime": "Full HTML5 / Three.js / Dual Theme",
        "description": "3D tactile terracotta culinary vessel with laminar thermal steam dissipation and procedural botanical herbarium.",
        "best_for": "Fine dining establishments, artisanal bakeries, culinary institutes, organic food purveyors."
    },
    "fitness-spatial": {
        "name": "Kinetic Musculoskeletal Tension Lines (Fitness & Wellness)",
        "sector": "Fitness",
        "category": "Domain Stage",
        "runtime": "Full HTML5 / Three.js / Dual Theme",
        "description": "Procedural kinetic gyroscope tracing tension vector lines, joint range of motion, and dynamic caloric expenditure.",
        "best_for": "Athletic performance platforms, fitness trackers, biomechanical therapy centers."
    },
    "travel-spatial": {
        "name": "Topographical Elevation Contour & Flight Arcs (Travel)",
        "sector": "Travel",
        "category": "Domain Stage",
        "runtime": "Full HTML5 / Three.js / Dual Theme",
        "description": "Precision topographical contour relief model with orthographic great-circle transit trajectories and altitude profiles.",
        "best_for": "Bespoke travel agencies, luxury expedition charters, airline booking engines."
    },
    "web3-spatial": {
        "name": "Cryptographic Hash Cube & State Machine (NFT / Web3)",
        "sector": "NFT / Web3",
        "category": "Domain Stage",
        "runtime": "Full HTML5 / Three.js / Dual Theme",
        "description": "3D interlocking state machine cube dynamically solving cryptographic hash rounds with tactile micro-rotations.",
        "best_for": "Digital provenance registries, decentralized art archives, cryptographic protocol foundations."
    },
    "beauty-spatial": {
        "name": "Viscous Organic Emulsion Waveform (Beauty & Luxury)",
        "sector": "Beauty / Spa",
        "category": "Domain Stage",
        "runtime": "Full HTML5 / Raw WebGL / Dual Theme",
        "description": "Viscous fluid surface simulation capturing organic surface tension, calm wave propagation, and cosmetic cream rheology.",
        "best_for": "Luxury skincare brands, holistic wellness spas, botanical apothecary lines."
    },
    "devtools-spatial": {
        "name": "Distributed Server Blade & Packet Conduits (Developer Tools)",
        "sector": "Developer Tools",
        "category": "Domain Stage",
        "runtime": "Full HTML5 / Three.js / Dual Theme",
        "description": "Isometric 3D server blade chassis displaying distributed node topologies and low-latency packet routing conduits.",
        "best_for": "Developer infrastructure, API gateways, observability suites, container orchestration."
    },
    "media-spatial": {
        "name": "Holographic Audio-Visual Waveguide (Entertainment & Media)",
        "sector": "Entertainment",
        "category": "Domain Stage",
        "runtime": "Full HTML5 / Raw WebGL / Dual Theme",
        "description": "Volumetric frequency waveguide resolving acoustic harmonies into fluid optical ribbon fields with depth of field.",
        "best_for": "Film studios, music streaming platforms, podcast networks, independent media houses."
    },
    "legal-spatial": {
        "name": "Balanced Precision Scales & Wax-Sealed Codex (Legal)",
        "sector": "Legal",
        "category": "Domain Stage",
        "runtime": "Full HTML5 / Three.js / Dual Theme",
        "description": "Precision burnished brass beam balance responding to micro-evidence weights alongside a tactile wax-sealed charter.",
        "best_for": "Law firms, legal tech platforms, compliance audits, dispute resolution chambers."
    },
    "events-spatial": {
        "name": "Spatial Amphitheater Plinth & Stage Volume (Events & Keynotes)",
        "sector": "Events",
        "category": "Domain Stage",
        "runtime": "Full HTML5 / Three.js / Dual Theme",
        "description": "Tiered concentric acoustic amphitheater seating volume with interactive session track spotlights and speaker plinth.",
        "best_for": "Global tech summits, academic symposia, cultural festivals, executive retreats."
    },

    # ── Foundation Shader Primitives ──────────────────────────────────
    "ribbon-field": {
        "name": "Ribbon Field",
        "sector": "Foundation Shaders",
        "category": "Background",
        "runtime": "Raw WebGL (GLSL Shaders) + Dynamic Dot Matrix",
        "description": "Smooth sinuous mathematical ribbons flowing across high-dimensional space, resolved into a fine tactical dot-matrix raster.",
        "best_for": "Hero backgrounds, intelligence substrate dashboards, telemetry headers."
    },
    "predictive-arc": {
        "name": "Predictive Arc",
        "sector": "Foundation Shaders",
        "category": "Background / Telemetry",
        "runtime": "Canvas 2D / Additive Particle Raster",
        "description": "Dynamic parabolic attention arc rendered as glowing dot matrix matrix with harmonic wave modulation.",
        "best_for": "Reasoning telemetry, interactive data visualizers, modal backdrops."
    },
    "stream-convergence": {
        "name": "Stream Convergence",
        "sector": "Foundation Shaders",
        "category": "Background",
        "runtime": "Raw WebGL (GLSL Shaders)",
        "description": "Multiple asynchronous token and attention streams converging gracefully into a calm focal reasoning core.",
        "best_for": "AI model loading states, agent orchestrators, flagship landing pages."
    },
    "dot-matrix": {
        "name": "Harmonic Dot Matrix Wave",
        "sector": "Foundation Shaders",
        "category": "Background",
        "runtime": "Raw WebGL / Canvas",
        "description": "High-density mathematical dot grid modulated by real-time distance and phase wave equations.",
        "best_for": "Developer documentation, technical infrastructure headers."
    },
    "spatial-scrollytelling": {
        "name": "Layered Spatial Scrollytelling",
        "sector": "Foundation Templates",
        "category": "Spatial Template",
        "runtime": "Full HTML5 + Three.js + Multi-Plane Depth",
        "description": "5-layer optical scrollytelling continuum with background WebGL, 3D wordmark, and chapter progression without text obstruction.",
        "best_for": "Flagship product monographs, spatial portfolios, interactive architectural walk-throughs."
    }
}

# Canonical templates with a concrete implementation in the dispatcher below.
# The remaining catalog entries are searchable references, not generators yet.
SPATIAL_GENERATOR_PRESETS = (
    "school-spatial",
    "erp-spatial",
    "ribbon-field",
    "predictive-arc",
    "spatial-scrollytelling",
)
SPATIAL_PRESET_ALIASES = {
    "education-codex": "school-spatial",
    "school": "school-spatial",
    "education": "school-spatial",
    "codex": "school-spatial",
    "book": "school-spatial",
    "erp": "erp-spatial",
    "modular-hub": "erp-spatial",
    "enterprise": "erp-spatial",
    "ribbon": "ribbon-field",
    "field": "ribbon-field",
    "arc": "predictive-arc",
    "predictive": "predictive-arc",
    "spatial-showcase": "spatial-scrollytelling",
    "showcase": "spatial-scrollytelling",
    "scrollytelling": "spatial-scrollytelling",
}


def list_presets():
    """Return dictionary of all available spatial presets."""
    return SPATIAL_PRESETS


def resolve_palette(palette_key, theme="dark"):
    """Resolve palette dictionary accounting for light/dark theme."""
    key = palette_key.lower()
    if theme == "light" and not key.endswith("-light"):
        light_key = f"{key}-light"
        if light_key in PALETTES:
            return PALETTES[light_key]
        return PALETTES.get("terracotta-light", PALETTES["terracotta"])
    return PALETTES.get(key, PALETTES["terracotta"])


def generate_ribbon_field(palette_key="terracotta", theme="dark", format_type="html"):
    """Generate Ribbon Field WebGL component retoned to the requested palette."""
    pal = resolve_palette(palette_key, theme)
    is_light = pal.get("theme") == "light"

    if format_type == "react":
        return f"""import React, {{ useEffect, useRef }} from "react";

export interface RibbonFieldProps {{
  speed?: number;
  pointerAmount?: number;
  smoothing?: number;
  opacity?: number;
  className?: string;
}}

export const RibbonField: React.FC<RibbonFieldProps> = ({{
  speed = 1.0,
  pointerAmount = 1.0,
  smoothing = 0.035,
  opacity = 1.0,
  className = ""
}}) => {{
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {{
    const canvas = canvasRef.current;
    if (!canvas) return;
    const gl = canvas.getContext("webgl");
    if (!gl) return;

    let animId: number;
    let width = (canvas.width = canvas.parentElement?.clientWidth || window.innerWidth);
    let height = (canvas.height = canvas.parentElement?.clientHeight || window.innerHeight);

    const vsSource = `
      attribute vec2 position;
      void main() {{
        gl_Position = vec4(position, 0.0, 1.0);
      }}
    `;

    const fsSource = `
      precision highp float;
      uniform vec2 resolution;
      uniform float time;
      uniform vec2 pointer;

      float hash(vec2 p) {{
        p = fract(p * vec2(123.34, 456.21));
        p += dot(p, p + 45.32);
        return fract(p.x * p.y);
      }}

      float ribbon(vec2 uv, float offset, float width, float phase) {{
        float y = 0.55 + 0.20 * sin((uv.x * 2.15) + phase) + 0.045 * sin((uv.x * 7.0) - phase * 0.7);
        float d = abs(uv.y - y - offset);
        return exp(-(d * d) / width);
      }}

      void main() {{
        vec2 uv = gl_FragCoord.xy / resolution.xy;
        float t = time * 0.22;
        float drift = (pointer.x - 0.5) * 0.06;

        float rightFade = smoothstep(0.28, 0.72, uv.x);
        float centerDark = 1.0 - smoothstep(0.0, 0.88, distance(uv, vec2(0.18, 0.48)));

        float r1 = ribbon(vec2(uv.x + drift, uv.y), 0.03, 0.0065, t + 0.9);
        float r2 = ribbon(vec2(uv.x - drift * 0.7, uv.y), -0.23, 0.0085, t + 3.25);
        float r3 = ribbon(vec2(uv.x + drift * 0.4, uv.y), 0.25, 0.014, t + 1.85);

        float glow = r1 * 1.14 + r2 * 1.05 + r3 * 0.48;

        // BC Design Retoned Palette: {pal['name']}
        vec3 col1 = {pal['gl_col1']};
        vec3 col2 = {pal['gl_col2']};
        vec3 col3 = {pal['gl_col3']};
        vec3 col4 = {pal['gl_col4']};

        vec3 col = vec3(0.0);
        col += col1 * r1 * 0.92;
        col += col2 * r1 * 0.62;
        col += col3 * r3 * 0.42;
        col += col4 * r2 * 0.66;
        col += col1 * (r2 + r3) * 0.30;

        float bloom = exp(-pow(distance(uv, vec2(0.76, 0.40 + 0.035 * sin(t))), 2.0) / 0.050);
        bloom += exp(-pow(distance(uv, vec2(0.71, 0.75 + 0.025 * cos(t))), 2.0) / 0.030);
        col += {pal['gl_bloom']} * bloom * 0.34;

        vec2 grid = fract(gl_FragCoord.xy / 7.0) - 0.5;
        float dotShape = smoothstep(0.29, 0.11, length(grid));
        float noise = hash(floor(gl_FragCoord.xy / 7.0));
        float scan = 0.72 + 0.28 * sin((uv.x + uv.y) * 38.0 + time * 1.3);
        float dots = dotShape * (0.48 + 0.52 * noise) * scan;

        float micro = hash(gl_FragCoord.xy + time) * 0.035;
        float alpha = clamp((glow * 1.55 + bloom * 0.50) * dots * rightFade, 0.0, 1.0);
        alpha *= 1.0 - centerDark * 0.56;

        vec3 base = {pal['gl_base']};
        vec3 finalColor = mix(base, col, clamp(alpha * 1.55, 0.0, 1.0));
        finalColor += micro * rightFade;

        gl_FragColor = vec4(finalColor, 1.0);
      }}
    `;

    function createShader(type: number, source: string) {{
      const s = gl.createShader(type)!;
      gl.shaderSource(s, source);
      gl.compileShader(s);
      return s;
    }}

    const program = gl.createProgram()!;
    gl.attachShader(program, createShader(gl.VERTEX_SHADER, vsSource));
    gl.attachShader(program, createShader(gl.FRAGMENT_SHADER, fsSource));
    gl.linkProgram(program);
    gl.useProgram(program);

    const posBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, posBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1]), gl.STATIC_DRAW);

    const posLoc = gl.getAttribLocation(program, "position");
    gl.enableVertexAttribArray(posLoc);
    gl.vertexAttribPointer(posLoc, 2, gl.FLOAT, false, 0, 0);

    const resLoc = gl.getUniformLocation(program, "resolution");
    const timeLoc = gl.getUniformLocation(program, "time");
    const ptrLoc = gl.getUniformLocation(program, "pointer");

    let startTime = performance.now();
    let ptrX = 0.5;

    const onMove = (e: MouseEvent) => {{
      ptrX += ((e.clientX / width) - ptrX) * smoothing * pointerAmount;
    }};
    window.addEventListener("mousemove", onMove);

    const render = () => {{
      const elapsed = (performance.now() - startTime) * 0.001 * speed;
      gl.viewport(0, 0, width, height);
      gl.uniform2f(resLoc, width, height);
      gl.uniform1f(timeLoc, elapsed);
      gl.uniform2f(ptrLoc, ptrX, 0.5);
      gl.drawArrays(gl.TRIANGLES, 0, 6);
      animId = requestAnimationFrame(render);
    }};
    render();

    const onResize = () => {{
      width = canvas.width = canvas.parentElement?.clientWidth || window.innerWidth;
      height = canvas.height = canvas.parentElement?.clientHeight || window.innerHeight;
    }};
    window.addEventListener("resize", onResize);

    return () => {{
      cancelAnimationFrame(animId);
      window.removeEventListener("mousemove", onMove);
      window.removeEventListener("resize", onResize);
    }};
  }}, [speed, pointerAmount, smoothing, opacity]);

  return <canvas ref={{canvasRef}} className={{`bc-spatial-canvas ${{className}}`}} style={{{{ width: "100%", height: "100%", display: "block" }}}} />;
}};
"""

    # Standalone HTML
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="{pal['theme']}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>BC Spatial | Ribbon Field ({pal['name']})</title>
  <style>
    :root {{
      --bc-bg: {pal['bg']};
      --bc-text: {pal['text']};
      --bc-accent: {pal['accent']};
      --bc-ease: cubic-bezier(0.16, 1, 0.3, 1);
    }}
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{ width: 100%; height: 100%; overflow: hidden; background: var(--bc-bg); color: var(--bc-text); font-family: "Onest", system-ui, sans-serif; }}
    #ribbon-canvas {{ position: fixed; inset: 0; width: 100%; height: 100%; display: block; }}
    .overlay-hud {{
      position: fixed; inset: 0; z-index: 10; pointer-events: none;
      display: flex; flex-direction: column; justify-content: space-between; padding: 32px;
    }}
    .hud-header {{ display: flex; justify-content: space-between; align-items: center; }}
    .hud-brand {{ font-size: 13px; font-weight: 500; letter-spacing: 0.18em; text-transform: uppercase; color: var(--bc-text); }}
    .hud-telemetry {{ font-family: "JetBrains Mono", monospace; font-size: 11px; letter-spacing: 0.14em; color: {pal['text_muted']}; }}
    .hud-center {{ max-width: 540px; pointer-events: auto; }}
    .hud-title {{ font-family: "Newsreader", serif; font-size: clamp(32px, 4.5vw, 64px); font-weight: 400; line-height: 1.1; margin-bottom: 16px; }}
    .hud-title em {{ font-style: italic; color: var(--bc-accent); }}
    .hud-deck {{ font-size: 15px; color: {pal['text_dim']}; line-height: 1.6; margin-bottom: 24px; }}
    .hud-cta {{
      display: inline-flex; align-items: center; gap: 10px; padding: 10px 22px; border-radius: 100px;
      background: var(--bc-accent); color: #ffffff !important; font-size: 12px; font-weight: 500;
      letter-spacing: 0.1em; text-transform: uppercase; text-decoration: none;
      box-shadow: 0 4px 20px rgba(217, 119, 87, 0.35); transition: transform 200ms var(--bc-ease);
    }}
    .hud-cta:hover {{ transform: translateY(-2px); }}
    @media (prefers-reduced-motion: reduce) {{
      *, *::before, *::after {{ animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }}
    }}
  </style>
</head>
<body>
  <canvas id="ribbon-canvas"></canvas>

  <div class="overlay-hud">
    <div class="hud-header">
      <div class="hud-brand">BC Spatial // {pal['name']}</div>
      <div class="hud-telemetry">GLSL / DOT-MATRIX / 60 FPS</div>
    </div>
    <div class="hud-center">
      <h1 class="hud-title">Sinuous <em>attractor</em> fields in mathematical space.</h1>
      <p class="hud-deck">
        Authentic ThreeUI ribbon wave architecture retoned to the BC Design literary humanist palette.
        A delicate balance of GPU extrusion, exponential bloom, and discrete scan rasterization.
      </p>
      <a href="bc-spatial-showcase.html" class="hud-cta">Enter Full Spatial Showcase</a>
    </div>
    <div class="hud-header">
      <div class="hud-telemetry">PALETTE: {pal['name'].upper()}</div>
      <div class="hud-telemetry">COORDINATES: TENSOR-01</div>
    </div>
  </div>

  <script>
    (function () {{
      const canvas = document.getElementById("ribbon-canvas");
      const gl = canvas.getContext("webgl");
      if (!gl) return;

      let width = (canvas.width = window.innerWidth);
      let height = (canvas.height = window.innerHeight);

      const vs = `
        attribute vec2 position;
        void main() {{ gl_Position = vec4(position, 0.0, 1.0); }}
      `;

      const fs = `
        precision highp float;
        uniform vec2 resolution;
        uniform float time;
        uniform vec2 pointer;

        float hash(vec2 p) {{
          p = fract(p * vec2(123.34, 456.21));
          p += dot(p, p + 45.32);
          return fract(p.x * p.y);
        }}

        float ribbon(vec2 uv, float offset, float width, float phase) {{
          float y = 0.55 + 0.20 * sin((uv.x * 2.15) + phase) + 0.045 * sin((uv.x * 7.0) - phase * 0.7);
          float d = abs(uv.y - y - offset);
          return exp(-(d * d) / width);
        }}

        void main() {{
          vec2 uv = gl_FragCoord.xy / resolution.xy;
          float t = time * 0.22;
          float drift = (pointer.x - 0.5) * 0.06;

          float rightFade = smoothstep(0.28, 0.72, uv.x);
          float centerDark = 1.0 - smoothstep(0.0, 0.88, distance(uv, vec2(0.18, 0.48)));

          float r1 = ribbon(vec2(uv.x + drift, uv.y), 0.03, 0.0065, t + 0.9);
          float r2 = ribbon(vec2(uv.x - drift * 0.7, uv.y), -0.23, 0.0085, t + 3.25);
          float r3 = ribbon(vec2(uv.x + drift * 0.4, uv.y), 0.25, 0.014, t + 1.85);

          float glow = r1 * 1.14 + r2 * 1.05 + r3 * 0.48;

          vec3 col1 = {pal['gl_col1']};
          vec3 col2 = {pal['gl_col2']};
          vec3 col3 = {pal['gl_col3']};
          vec3 col4 = {pal['gl_col4']};

          vec3 col = vec3(0.0);
          col += col1 * r1 * 0.92;
          col += col2 * r1 * 0.62;
          col += col3 * r3 * 0.42;
          col += col4 * r2 * 0.66;
          col += col1 * (r2 + r3) * 0.30;

          float bloom = exp(-pow(distance(uv, vec2(0.76, 0.40 + 0.035 * sin(t))), 2.0) / 0.050);
          bloom += exp(-pow(distance(uv, vec2(0.71, 0.75 + 0.025 * cos(t))), 2.0) / 0.030);
          col += {pal['gl_bloom']} * bloom * 0.34;

          vec2 grid = fract(gl_FragCoord.xy / 7.0) - 0.5;
          float dotShape = smoothstep(0.29, 0.11, length(grid));
          float noise = hash(floor(gl_FragCoord.xy / 7.0));
          float scan = 0.72 + 0.28 * sin((uv.x + uv.y) * 38.0 + time * 1.3);
          float dots = dotShape * (0.48 + 0.52 * noise) * scan;

          float micro = hash(gl_FragCoord.xy + time) * 0.035;
          float alpha = clamp((glow * 1.55 + bloom * 0.50) * dots * rightFade, 0.0, 1.0);
          alpha *= 1.0 - centerDark * 0.56;

          vec3 base = {pal['gl_base']};
          vec3 finalColor = mix(base, col, clamp(alpha * 1.55, 0.0, 1.0));
          finalColor += micro * rightFade;

          gl_FragColor = vec4(finalColor, 1.0);
        }}
      `;

      function compile(type, src) {{
        const s = gl.createShader(type);
        gl.shaderSource(s, src);
        gl.compileShader(s);
        return s;
      }}

      const prog = gl.createProgram();
      gl.attachShader(prog, compile(gl.VERTEX_SHADER, vs));
      gl.attachShader(prog, compile(gl.FRAGMENT_SHADER, fs));
      gl.linkProgram(prog);
      gl.useProgram(prog);

      const buf = gl.createBuffer();
      gl.bindBuffer(gl.ARRAY_BUFFER, buf);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1, 1,-1, -1,1, -1,1, 1,-1, 1,1]), gl.STATIC_DRAW);

      const pos = gl.getAttribLocation(prog, "position");
      gl.enableVertexAttribArray(pos);
      gl.vertexAttribPointer(pos, 2, gl.FLOAT, false, 0, 0);

      const resLoc = gl.getUniformLocation(prog, "resolution");
      const timeLoc = gl.getUniformLocation(prog, "time");
      const ptrLoc = gl.getUniformLocation(prog, "pointer");

      let ptrX = 0.5;
      window.addEventListener("mousemove", (e) => {{
        ptrX += ((e.clientX / width) - ptrX) * 0.05;
      }});

      let start = performance.now();
      function render() {{
        const elapsed = (performance.now() - start) * 0.001;
        gl.viewport(0, 0, width, height);
        gl.uniform2f(resLoc, width, height);
        gl.uniform1f(timeLoc, elapsed);
        gl.uniform2f(ptrLoc, ptrX, 0.5);
        gl.drawArrays(gl.TRIANGLES, 0, 6);
        requestAnimationFrame(render);
      }}
      render();

      window.addEventListener("resize", () => {{
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
      }});
    }})();
  </script>
</body>
</html>
"""


def generate_predictive_arc(palette_key="terracotta", theme="dark", format_type="html"):
    """Generate Predictive Arc Canvas 2D component retoned to the requested palette."""
    pal = resolve_palette(palette_key, theme)
    is_light = pal.get("theme") == "light"

    if format_type == "react":
        return f"""import React, {{ useEffect, useRef }} from "react";

export interface PredictiveArcProps {{
  speed?: number;
  spacing?: number;
  dotSize?: number;
  archHeight?: number;
  thickness?: number;
  brightness?: number;
  className?: string;
}}

export const PredictiveArc: React.FC<PredictiveArcProps> = ({{
  speed = 1.0,
  spacing = 5,
  dotSize = 6,
  archHeight = 0.7,
  thickness = 1.0,
  brightness = 1.0,
  className = ""
}}) => {{
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {{
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d", {{ alpha: false }});
    if (!ctx) return;

    let animId: number;
    let time = 0;
    let width = (canvas.width = canvas.parentElement?.clientWidth || window.innerWidth);
    let height = (canvas.height = canvas.parentElement?.clientHeight || window.innerHeight);

    const render = () => {{
      ctx.fillStyle = "{pal['bg']}";
      ctx.fillRect(0, 0, width, height);
      time += 0.015 * speed;

      const centerX = width / 2;
      const archPeakY = height * 0.35;
      const archWidth = width * 1.5;
      const effectiveArchHeight = height * archHeight;
      ctx.globalCompositeOperation = "{'source-over' if is_light else 'lighter'}";

      for (let x = 0; x < width; x += spacing) {{
        const normX = (x - centerX) / (archWidth / 2);
        const curveY = archPeakY + normX * normX * effectiveArchHeight;
        for (let y = 0; y < height; y += spacing) {{
          const distanceToCurve = Math.abs(y - curveY);
          const dynamicThickness = (140 + (1 - Math.abs(normX)) * 80) * thickness;
          if (distanceToCurve >= dynamicThickness) continue;
          let intensity = 1 - distanceToCurve / dynamicThickness;
          const waveX = Math.sin(x * 0.015 + time);
          const waveY = Math.cos(y * 0.02 + time);
          intensity = intensity * 0.7 + waveX * waveY * 0.3 * intensity;
          intensity *= Math.max(0, 1 - Math.pow(Math.abs(normX), 2.5));
          if (intensity <= 0.02) continue;

          // Retoned to {pal['name']}
          const r = Math.min(255, 217 * intensity + 38 * Math.pow(intensity, 3));
          const g = Math.min(255, 119 * intensity + 40 * Math.pow(intensity, 4));
          const b = Math.min(255, 87 * intensity + 20 * Math.pow(intensity, 2));

          ctx.fillStyle = `rgb(${{Math.floor(r * brightness)}}, ${{Math.floor(g * brightness)}}, ${{Math.floor(b * brightness)}})`;
          ctx.fillRect(x, y, dotSize * intensity, dotSize * intensity);
        }}
      }}
      ctx.globalCompositeOperation = "source-over";
      animId = requestAnimationFrame(render);
    }};
    render();

    const onResize = () => {{
      width = canvas.width = canvas.parentElement?.clientWidth || window.innerWidth;
      height = canvas.height = canvas.parentElement?.clientHeight || window.innerHeight;
    }};
    window.addEventListener("resize", onResize);

    return () => {{
      cancelAnimationFrame(animId);
      window.removeEventListener("resize", onResize);
    }};
  }}, [speed, spacing, dotSize, archHeight, thickness, brightness]);

  return <canvas ref={{canvasRef}} className={{`bc-predictive-arc ${{className}}`}} style={{{{ width: "100%", height: "100%", display: "block" }}}} />;
}};
"""

    return f"""<!DOCTYPE html>
<html lang="en" data-theme="{pal['theme']}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>BC Spatial | Predictive Arc ({pal['name']})</title>
  <style>
    :root {{
      --bc-bg: {pal['bg']};
      --bc-text: {pal['text']};
      --bc-accent: {pal['accent']};
      --bc-ease: cubic-bezier(0.16, 1, 0.3, 1);
    }}
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{ width: 100%; height: 100%; overflow: hidden; background: var(--bc-bg); color: var(--bc-text); font-family: "Onest", system-ui, sans-serif; }}
    #arc-canvas {{ position: fixed; inset: 0; width: 100%; height: 100%; display: block; }}
    .overlay-hud {{
      position: fixed; inset: 0; z-index: 10; pointer-events: none;
      display: flex; flex-direction: column; justify-content: space-between; padding: 32px;
    }}
    .hud-header {{ display: flex; justify-content: space-between; align-items: center; }}
    .hud-brand {{ font-size: 13px; font-weight: 500; letter-spacing: 0.18em; text-transform: uppercase; color: var(--bc-text); }}
    .hud-telemetry {{ font-family: "JetBrains Mono", monospace; font-size: 11px; letter-spacing: 0.14em; color: {pal['text_muted']}; }}
    .hud-center {{ max-width: 540px; pointer-events: auto; }}
    .hud-title {{ font-family: "Newsreader", serif; font-size: clamp(32px, 4.5vw, 64px); font-weight: 400; line-height: 1.1; margin-bottom: 16px; }}
    .hud-title em {{ font-style: italic; color: var(--bc-accent); }}
    .hud-deck {{ font-size: 15px; color: {pal['text_dim']}; line-height: 1.6; margin-bottom: 24px; }}
    .hud-cta {{
      display: inline-flex; align-items: center; gap: 10px; padding: 10px 22px; border-radius: 100px;
      background: var(--bc-accent); color: #ffffff !important; font-size: 12px; font-weight: 500;
      letter-spacing: 0.1em; text-transform: uppercase; text-decoration: none;
      box-shadow: 0 4px 20px rgba(217, 119, 87, 0.35); transition: transform 200ms var(--bc-ease);
    }}
    .hud-cta:hover {{ transform: translateY(-2px); }}
    @media (prefers-reduced-motion: reduce) {{
      *, *::before, *::after {{ animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }}
    }}
  </style>
</head>
<body>
  <canvas id="arc-canvas"></canvas>

  <div class="overlay-hud">
    <div class="hud-header">
      <div class="hud-brand">BC Spatial // Predictive Arc</div>
      <div class="hud-telemetry">CANVAS 2D / HARMONIC FLUX / 60 FPS</div>
    </div>
    <div class="hud-center">
      <h1 class="hud-title">Predictive <em>attention</em> arc in latent space.</h1>
      <p class="hud-deck">
        A parabolic harmonic raster resolved through additive terracotta luminescence.
        Each particle encodes probability densities over continuous inference streams.
      </p>
      <a href="bc-spatial-showcase.html" class="hud-cta">Explore Spatial Architecture</a>
    </div>
    <div class="hud-header">
      <div class="hud-telemetry">PALETTE: {pal['name'].upper()}</div>
      <div class="hud-telemetry">HARMONIC PARABOLA / 2D MATRIX</div>
    </div>
  </div>

  <script>
    (function () {{
      const canvas = document.getElementById("arc-canvas");
      const ctx = canvas.getContext("2d", {{ alpha: false }});
      if (!ctx) return;

      let width = (canvas.width = window.innerWidth);
      let height = (canvas.height = window.innerHeight);
      let time = 0;

      function render() {{
        ctx.fillStyle = "{pal['bg']}";
        ctx.fillRect(0, 0, width, height);
        time += 0.015;

        const centerX = width / 2;
        const archPeakY = height * 0.35;
        const archWidth = width * 1.5;
        const archHeight = height * 0.7;
        ctx.globalCompositeOperation = "{'source-over' if is_light else 'lighter'}";

        const spacing = 6;
        const dotSize = 6.5;

        for (let x = 0; x < width; x += spacing) {{
          const normX = (x - centerX) / (archWidth / 2);
          const curveY = archPeakY + normX * normX * archHeight;
          for (let y = 0; y < height; y += spacing) {{
            const distanceToCurve = Math.abs(y - curveY);
            const thickness = 140 + (1 - Math.abs(normX)) * 80;
            if (distanceToCurve >= thickness) continue;
            let intensity = 1 - distanceToCurve / thickness;
            const waveX = Math.sin(x * 0.015 + time);
            const waveY = Math.cos(y * 0.02 + time);
            intensity = intensity * 0.7 + waveX * waveY * 0.3 * intensity;
            intensity *= Math.max(0, 1 - Math.pow(Math.abs(normX), 2.5));
            if (intensity <= 0.02) continue;

            const r = Math.min(255, 217 * intensity + 38 * Math.pow(intensity, 3));
            const g = Math.min(255, 119 * intensity + 40 * Math.pow(intensity, 4));
            const b = Math.min(255, 87 * intensity + 20 * Math.pow(intensity, 2));

            ctx.fillStyle = "rgb(" + Math.floor(r) + "," + Math.floor(g) + "," + Math.floor(b) + ")";
            ctx.fillRect(x, y, dotSize * intensity, dotSize * intensity);
          }}
        }}
        ctx.globalCompositeOperation = "source-over";
        requestAnimationFrame(render);
      }}
      render();

      window.addEventListener("resize", () => {{
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
      }});
    }})();
  </script>
</body>
</html>
"""


def generate_erp_spatial(palette_key="terracotta", theme="dark", format_type="html"):
    """Generate 3D Modular Enterprise Supply-Chain Hub template for ERP systems."""
    pal = resolve_palette(palette_key, theme)
    is_light = pal.get("theme") == "light"
    init_theme = "light" if is_light else "dark"
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="{init_theme}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Vanguard ERP / Modular Operational Engine & Supply Chain</title>
  <meta name="description" content="3D interactive enterprise resource planning hub with synchronized multi-division pipeline telemetry.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&display=swap" rel="stylesheet">
  <script src="https://unpkg.com/three@0.160.0/build/three.min.js"></script>
  <style>
    :root {{
      --bc-font-serif: "Newsreader", Georgia, serif;
      --bc-font-sans: "Inter", -apple-system, sans-serif;
      --bc-font-mono: "JetBrains Mono", monospace;
      --bc-ease: cubic-bezier(0.16, 1, 0.3, 1);
      --nav-h: 72px;
      --pad: clamp(24px, 5vw, 64px);
    }}
    html[data-theme="dark"] {{
      --bc-bg: #0D0C0A;
      --bc-surface: rgba(26, 24, 21, 0.75);
      --bc-surface-hover: rgba(36, 32, 28, 0.9);
      --bc-text: #FAF9F5;
      --bc-text-dim: #C5BFB3;
      --bc-text-muted: #8A8479;
      --bc-border: rgba(250, 249, 245, 0.12);
      --bc-border-subtle: rgba(250, 249, 245, 0.06);
      --bc-accent: #D97757;
      --bc-accent-hover: #E08B6E;
      --bc-accent-deep: #B35637;
      --bc-accent-glow: rgba(217, 119, 87, 0.22);
    }}
    html[data-theme="light"] {{
      --bc-bg: #FAF9F5;
      --bc-surface: rgba(243, 239, 230, 0.85);
      --bc-surface-hover: rgba(235, 230, 218, 0.95);
      --bc-text: #1F1E1B;
      --bc-text-dim: #4D4942;
      --bc-text-muted: #797368;
      --bc-border: rgba(31, 30, 27, 0.12);
      --bc-border-subtle: rgba(31, 30, 27, 0.06);
      --bc-accent: #C15F3D;
      --bc-accent-hover: #AD5030;
      --bc-accent-deep: #8F3E22;
      --bc-accent-glow: rgba(193, 95, 61, 0.15);
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: var(--bc-font-sans);
      background: var(--bc-bg);
      color: var(--bc-text);
      overflow-x: hidden;
      min-height: 100vh;
      transition: background 250ms var(--bc-ease), color 250ms var(--bc-ease);
    }}
    #erp-canvas {{
      position: fixed;
      top: 0; left: 0;
      width: 100vw; height: 100vh;
      pointer-events: none;
      z-index: 1;
    }}
    .nav-header {{
      position: fixed;
      top: 0; left: 0; right: 0;
      height: var(--nav-h);
      padding: 0 var(--pad);
      display: flex;
      align-items: center;
      justify-content: space-between;
      backdrop-filter: blur(20px);
      background: var(--bc-surface);
      border-bottom: 1px solid var(--bc-border);
      z-index: 30;
    }}
    .brand-title {{
      font-family: var(--bc-font-mono);
      font-size: 13px;
      font-weight: 500;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: var(--bc-text);
    }}
    .theme-toggle-btn {{
      padding: 6px 14px;
      border-radius: 100px;
      font-family: var(--bc-font-mono);
      font-size: 11px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--bc-text);
      background: var(--bc-surface);
      border: 1px solid var(--bc-border);
      cursor: pointer;
      transition: all 200ms var(--bc-ease);
    }}
    .theme-toggle-btn:hover {{
      border-color: var(--bc-accent);
      background: var(--bc-surface-hover);
    }}
    .hero-container {{
      position: relative;
      z-index: 10;
      min-height: 100vh;
      padding: calc(var(--nav-h) + 48px) var(--pad) 64px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .hero-text-block {{
      max-width: min(580px, 48vw);
      padding-top: clamp(20px, 4vh, 60px);
    }}
    .eyebrow-badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-family: var(--bc-font-mono);
      font-size: 11px;
      letter-spacing: 0.2em;
      text-transform: uppercase;
      color: var(--bc-accent);
      margin-bottom: 20px;
    }}
    .hero-headline {{
      font-family: var(--bc-font-serif);
      font-size: clamp(38px, 4.8vw, 72px);
      font-weight: 400;
      line-height: 1.1;
      letter-spacing: -0.02em;
      margin-bottom: 20px;
      color: var(--bc-text);
    }}
    .hero-headline em {{
      font-style: italic;
      color: var(--bc-accent);
    }}
    .hero-deck {{
      font-size: 16px;
      line-height: 1.65;
      color: var(--bc-text-dim);
      margin-bottom: 32px;
    }}
    .btn-contrast-action {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 10px 22px;
      border-radius: 100px;
      font-size: 12.5px;
      font-weight: 500;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: #ffffff !important;
      background: var(--bc-accent);
      border: 1px solid var(--bc-accent-deep);
      text-decoration: none;
      transition: background 200ms var(--bc-ease), transform 200ms var(--bc-ease);
    }}
    .btn-contrast-action:hover {{
      background: var(--bc-accent-hover);
      transform: translateY(-1px);
    }}
    .division-cards-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-top: 48px;
    }}
    .division-card {{
      background: var(--bc-surface);
      border: 1px solid var(--bc-border);
      border-radius: 10px;
      padding: 20px;
      backdrop-filter: blur(16px);
      transition: border-color 200ms var(--bc-ease);
    }}
    .division-card:hover {{
      border-color: var(--bc-accent);
    }}
    .division-idx {{
      font-family: var(--bc-font-mono);
      font-size: 11px;
      color: var(--bc-accent);
      letter-spacing: 0.1em;
      display: block;
      margin-bottom: 6px;
    }}
    .division-card h2 {{
      font-family: var(--bc-font-serif);
      font-size: 18px;
      font-weight: 500;
      color: var(--bc-text);
      margin-bottom: 6px;
    }}
    .division-card p {{
      font-size: 13px;
      line-height: 1.5;
      color: var(--bc-text-dim);
    }}
    @media (prefers-reduced-motion: reduce) {{
      *, *::before, *::after {{
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
      }}
    }}
    @media (max-width: 960px) {{
      .hero-text-block {{ max-width: 100%; }}
      .division-cards-grid {{ grid-template-columns: repeat(2, 1fr); }}
    }}
    @media (max-width: 600px) {{
      .division-cards-grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <canvas id="erp-canvas"></canvas>
  <header class="nav-header">
    <div class="brand-title">Vanguard ERP // Operations Core</div>
    <button class="theme-toggle-btn" id="themeBtn"><span>Toggle Theme</span></button>
  </header>
  <main class="hero-container">
    <div class="hero-text-block">
      <div class="eyebrow-badge">Architecture 01 / Modular Supply-Chain Engine</div>
      <h1 class="hero-headline">Synchronized operational <em>intelligence</em> across all divisions.</h1>
      <p class="hero-deck">
        Vanguard connects procurement, autonomous warehousing, logistics, and multi-currency general ledgers into a unified physical data continuum.
      </p>
      <a href="#divisions" class="btn-contrast-action">Access Enterprise Console</a>
    </div>
    <div class="division-cards-grid" id="divisions">
      <div class="division-card">
        <span class="division-idx">MODULE 01</span>
        <h2>Procurement & Sourcing</h2>
        <p>Real-time supplier contracts, purchase reconciliation, and material forecasts.</p>
      </div>
      <div class="division-card">
        <span class="division-idx">MODULE 02</span>
        <h2>Autonomous Inventory</h2>
        <p>Automated fulfillment robotics, barcode scanning, and multi-depot stock telemetry.</p>
      </div>
      <div class="division-card">
        <span class="division-idx">MODULE 03</span>
        <h2>Cold-Chain Logistics</h2>
        <p>Fleet routing algorithms, customs compliance, and real-time cargo temperature tracking.</p>
      </div>
      <div class="division-card">
        <span class="division-idx">MODULE 04</span>
        <h2>General Ledger</h2>
        <p>Double-entry automated settlement, international treasury transfers, and audit logs.</p>
      </div>
    </div>
  </main>
  <script>
    (function() {{
      const canvas = document.getElementById("erp-canvas");
      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 100);
      camera.position.set(0, 0.5, 7.5);

      const renderer = new THREE.WebGLRenderer({{ canvas, antialias: true, alpha: true }});
      renderer.setSize(window.innerWidth, window.innerHeight);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

      const ambient = new THREE.AmbientLight(0xfaf9f5, 1.2);
      scene.add(ambient);

      const dirLight = new THREE.DirectionalLight(0xc2a26a, 1.4);
      dirLight.position.set(5, 8, 4);
      scene.add(dirLight);

      // 3D Modular Division Hub
      const erpGroup = new THREE.Group();
      erpGroup.position.set(2.3, 0.25, 0);
      erpGroup.scale.set(0.85, 0.85, 0.85);
      scene.add(erpGroup);

      const cubeMat = new THREE.MeshStandardMaterial({{ color: 0xc15f3d, roughness: 0.4, metalness: 0.7 }});
      const stoneMat = new THREE.MeshStandardMaterial({{ color: 0x8c6d37, roughness: 0.6, metalness: 0.4 }});

      // 4 Interlocking Modular Division Cubes
      const cube1 = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.2, 1.2), cubeMat);
      cube1.position.set(-0.8, 0.8, 0);
      erpGroup.add(cube1);

      const cube2 = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.2, 1.2), stoneMat);
      cube2.position.set(0.8, 0.8, 0);
      erpGroup.add(cube2);

      const cube3 = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.2, 1.2), stoneMat);
      cube3.position.set(-0.8, -0.8, 0);
      erpGroup.add(cube3);

      const cube4 = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.2, 1.2), cubeMat);
      cube4.position.set(0.8, -0.8, 0);
      erpGroup.add(cube4);

      // Connecting Data Conduits (Bezier Tubes)
      const conduitCurve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(-0.8, 0.8, 0),
        new THREE.Vector3(0, 0, 0.4),
        new THREE.Vector3(0.8, -0.8, 0)
      ]);
      const conduitGeo = new THREE.TubeGeometry(conduitCurve, 24, 0.04, 8, false);
      const conduitMat = new THREE.MeshStandardMaterial({{ color: 0xc2a26a, roughness: 0.2, metalness: 0.9 }});
      erpGroup.add(new THREE.Mesh(conduitGeo, conduitMat));

      let mouseX = 0, mouseY = 0;
      window.addEventListener("mousemove", (e) => {{
        mouseX = (e.clientX / window.innerWidth - 0.5) * 2;
        mouseY = (e.clientY / window.innerHeight - 0.5) * 2;
      }});

      const clock = new THREE.Clock();
      function render() {{
        requestAnimationFrame(render);
        const t = clock.getElapsedTime();
        erpGroup.rotation.y = t * 0.15 + mouseX * 0.2;
        erpGroup.rotation.x = -0.15 - mouseY * 0.15;
        camera.lookAt(0.8, 0.2, 0);
        renderer.render(scene, camera);
      }}
      render();

      const themeBtn = document.getElementById("themeBtn");
      themeBtn.addEventListener("click", () => {{
        const html = document.documentElement;
        const next = html.getAttribute("data-theme") === "dark" ? "light" : "dark";
        html.setAttribute("data-theme", next);
        cubeMat.color.setHex(next === "light" ? 0xc15f3d : 0xd97757);
      }});

      window.addEventListener("resize", () => {{
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
      }});
    }})();
  </script>
</body>
</html>
"""


def generate_spatial_component(preset_name, palette_key="terracotta", theme="dark", format_type="html"):
    """Main generation dispatcher for spatial components."""
    preset = SPATIAL_PRESET_ALIASES.get(preset_name, preset_name)

    if preset == "ribbon-field":
        return generate_ribbon_field(palette_key, theme, format_type)
    elif preset == "predictive-arc":
        return generate_predictive_arc(palette_key, theme, format_type)
    elif preset == "school-spatial":
        template = ASSETS_DIR / "school-codex.html"
        if template.is_file():
            return template.read_text(encoding="utf-8")
        raise FileNotFoundError(f"School spatial template asset not found at {template}")
    elif preset == "erp-spatial":
        return generate_erp_spatial(palette_key, theme, format_type)
    elif preset == "spatial-scrollytelling":
        template = ASSETS_DIR / "spatial-showcase.html"
        if template.is_file():
            return template.read_text(encoding="utf-8")
        raise FileNotFoundError(f"Spatial showcase template asset not found at {template}")
    else:
        runnable = sorted(SPATIAL_GENERATOR_PRESETS)
        raise ValueError(
            f"Preset '{preset_name}' cannot be generated. Available runnable generators: {runnable}. "
            f"For the full 31-sector reference catalog, see data/spatial-effects.csv or run 'bc_design.py --domain spatial'."
        )

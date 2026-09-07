# BC Design System - Component Blueprints

Detailed architectural specifications and component patterns embodying the **BC Design Language**.

---

## 1. The BC Design Auth Card (Login & Sign Up)

Designed as a warm, focused reference surface for BC Design interfaces.

### Key Characteristics:
* **Background**: Centered on the warm parchment canvas (`#FAF9F5`).
* **Container**: Flat, clean card (`#FFFFFF`) with a 1px delicate warm hairline border (`rgba(31, 30, 27, 0.08)`) and soft diffused elevation.
* **Heading**: High-contrast, literary serif (`var(--bc-font-serif)` with Newsreader/Georgia fallback).
* **CTA Button**: Signature Terracotta (`#D97757`) with subtle dark hover (`#C15F3E`).
* **OAuth Options**: Warm white surface with subtle 1px border.

```html
<div class="bc-auth-wrapper">
  <div class="bc-card bc-fade-up">
    <!-- Starburst / Logo Mark -->
    <div class="bc-logo-mark">
      <svg width="36" height="36" viewBox="0 0 24 24" fill="none">
        <path d="M12 2L14.2 9.8L22 12L14.2 14.2L12 22L9.8 14.2L2 12L9.8 9.8L12 2Z" fill="#D97757"/>
      </svg>
    </div>

    <h1 class="bc-heading-serif">Welcome to BC Design</h1>
    <p class="bc-subtext">Enter your email to sign in or create an account.</p>

    <form class="bc-form">
      <label class="bc-label" for="email">Email address</label>
      <input type="email" id="email" class="bc-input" placeholder="you@company.com" required />
      
      <button type="submit" class="bc-btn-primary bc-interactive">
        Continue with email
      </button>
    </form>

    <div class="bc-divider">
      <span>or</span>
    </div>

    <div class="bc-social-group">
      <button class="bc-btn-secondary bc-interactive">
        <svg width="18" height="18" viewBox="0 0 24 24" class="mr-2">...</svg>
        Continue with Google
      </button>
      <button class="bc-btn-secondary bc-interactive">
        <svg width="18" height="18" viewBox="0 0 24 24" class="mr-2">...</svg>
        Continue with Apple
      </button>
    </div>
  </div>
</div>
```

---

## 2. The BC Design Floating Prompt Box

The iconic conversational input container on BC Design:

* **Container**: `border-radius: 18px;`, warm white surface, gentle shadow.
* **Textarea**: Auto-resizing, clean sans-serif typography, no harsh native borders.
* **Controls Row**: Attached model picker badge (`BC Design · Current model`), attachment paperclip, and a clearly labelled terracotta send control.

```html
<div class="bc-prompt-container">
  <textarea 
    class="bc-prompt-textarea" 
    placeholder="Reply to BC Design..."
    rows="2"
  ></textarea>

  <div class="bc-prompt-toolbar">
    <div class="bc-model-badge">
      BC Design · Current model
    </div>

    <button class="bc-send-btn" aria-label="Send message">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <line x1="12" y1="19" x2="12" y2="5"></line>
        <polyline points="5 12 12 5 19 12"></polyline>
      </svg>
    </button>
  </div>
</div>
```

---

## 3. The Artifacts Split-Screen Panel

When code, SVG graphics, or documentation are rendered:

* **Trigger**: Slides in from right (`bcDrawerIn` animation).
* **Header**: Tab switcher between *Code* and *Preview*, Copy button, popout button.
* **Theme**: Seamless warm charcoal for code, or sand-toned preview frame.

---

## 4. The Feature Onboarding Hero ("Customize BC Design")

Centered hero for product capabilities, settings, or integrations:

* **Icon**: Hairline SVG line-art (e.g. hand sliding horizontal faders).
* **Heading**: Literary Serif (`var(--bc-font-serif)`), medium weight, 32px-40px, centered.
* **Button Pair**: High-contrast Solid White (`.bc-btn-contrast`) for primary action, Dark Glass (`.bc-btn-glass`) for secondary.

```html
<div class="bc-hero-container">
  <div class="bc-hero-icon">
    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <!-- Hand adjusting slider fader -->
      <path d="M12 4V20M8 8H16M6 16H14" />
    </svg>
  </div>
  <h1 class="bc-heading-serif">Customize BC Design<br>for the best results</h1>
  <p class="bc-subtext">
    Connectors bring your apps and data into BC Design to complete tasks. Plugins combine connectors and skills to complete workflows.
  </p>
  <div class="bc-btn-group">
    <button class="bc-btn-contrast">Browse connectors</button>
    <button class="bc-btn-glass">Explore plugins</button>
  </div>
</div>
```

---

## 5. The Split-Illustration Modal ("Review updates to BC Design's memory")

BC Design's signature modal layout combining product features on the left with an **organic, hand-drawn crayon illustration** on the right:

* **Container**: Dark surface (`#1F1E1D`), 16px radius, subtle border.
* **Left Column**: Serif header, list of feature bullets with clean icons, and modern toggle switch.
* **Right Column**: Warm terracotta thought bubble with chalk/crayon hand-drawn squiggles.
* **Bottom Action**: Full-width high-contrast white button (`.bc-btn-contrast`).

```html
<div class="bc-modal-backdrop">
  <div class="bc-modal-split">
    <!-- Left Column: Settings / Feature List -->
    <div class="bc-modal-left">
      <h2 class="bc-heading-serif">Review updates to BC Design's memory</h2>
      
      <div class="bc-feature-item">
        <svg class="feature-icon" viewBox="0 0 24 24">...</svg>
        <div>
          <h4>BC Design remembers Cowork tasks too</h4>
          <p>Not just your chats—what you work on in Cowork gets remembered the same way.</p>
        </div>
      </div>

      <div class="bc-toggle-row">
        <div>
          <h4>Include sensitive topics in memory</h4>
          <p>You can change this anytime in settings.</p>
        </div>
        <label class="bc-toggle">
          <input type="checkbox" checked />
          <span class="bc-toggle-slider"></span>
        </label>
      </div>

      <button class="bc-btn-contrast w-full">Save preferences</button>
    </div>

    <!-- Right Column: Organic Terracotta Crayon Illustration -->
    <div class="bc-modal-right">
      <svg width="240" height="240" viewBox="0 0 200 200" fill="none">
        <!-- Organic Thought Bubble in Terracotta -->
        <path d="M40,100 C30,70 60,35 110,35 C160,35 185,70 175,105 C165,140 130,155 85,150 C55,145 45,120 40,100 Z" fill="#D97757" />
        <circle cx="35" cy="165" r="12" fill="#D97757" />
        <circle cx="20" cy="180" r="7" fill="#D97757" />
        <!-- Hand-drawn Chalk Squiggle -->
        <path d="M60,95 Q75,70 90,95 T120,95 T150,95" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" />
      </svg>
    </div>
  </div>
</div>
```

---

## 6. The Learning Hub Tutorial Card with macOS Window Chrome

Used in BC Design's "Learn" and "Getting started" sections:

* **Preview Frame**: Mini desktop mockup with macOS traffic light dots (🔴 🟡 🟢).
* **Duration Badge**: Floating pill `"4 min"` in the top-right corner.
* **Category Label**: Muted small uppercase `"Tutorial"`.
* **Title**: High-contrast, clean sans or serif.

```html
<div class="bc-tutorial-card">
  <div class="bc-window-preview">
    <div class="bc-mac-chrome">
      <span class="mac-dot mac-dot-red"></span>
      <span class="mac-dot mac-dot-yellow"></span>
      <span class="mac-dot mac-dot-green"></span>
      <span class="bc-duration-tag">4 min</span>
    </div>
    <div class="bc-preview-screen">
      <!-- Mini UI preview -->
    </div>
  </div>
  <div class="bc-tutorial-body">
    <span class="bc-label-muted">Tutorial</span>
    <h3 class="bc-card-title">Get started in BC Design Cowork</h3>
  </div>
</div>
```

---

## 7. The Role / Category Grid

10 role selector cards for onboarding and prompt exploration:

* **Container**: Grid with 3 or 4 columns.
* **Card**: Rounded rectangle with 1px border (`rgba(255, 255, 255, 0.08)`).
* **Icon**: Monoline SVG icon inside a rounded square well (`.bc-role-icon`).
* **Badges**: Optional `"For you"` pill badge in vibrant blue (`#1A62D6`).

---

## 8. Earth Pastel Course Cards with Dynamic Arrow Buttons (Light Mode)

As seen in BC Design's Light Mode "Learn" hub:

* **Thumbnail Colors**:
  * **Sage / Eucalyptus Green** (`#A8C2B7`): For system / Cowork courses.
  * **Blush Peach / Clay** (`#E8CFC5`): For core prompting / BC Design 101 courses.
* **Inner Badge**: Off-white squircle pill with fine line-art SVG icon.
* **Circle Arrow Action**:
  * Default course: Soft neutral circle (`#F3F2EE`) with dark arrow.
  * Highlighted / Primary course: **Solid Ink Black circle (`#1F1E1B`) with crisp white arrow**!

```html
<div class="bc-course-card">
  <div class="bc-thumb-peach" style="width: 130px; height: 90px;">
    <div class="bc-inner-squircle">
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor">...</svg>
    </div>
  </div>
  <div class="bc-course-info">
    <span class="bc-label-muted">Course</span>
    <h3 class="bc-heading-serif">BC Design 101</h3>
    <p>Learn to use BC Design for everyday work, from your first conversation to artifacts and tools.</p>
  </div>
  <button class="bc-circle-btn-dark">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <line x1="5" y1="12" x2="19" y2="12"></line>
      <polyline points="12 5 19 12 12 19"></polyline>
    </svg>
  </button>
</div>
```

---

## 9. Form Inputs & Settings Fields (Profile Settings)

Light mode form inputs as seen in BC Design's account settings:

* **Surface**: Pure white `#FFFFFF` with delicate 1px border (`#E5E2DA`).
* **Corner Radius**: `8px` (`rounded-lg`).
* **Typography**: Base 14.5px, medium label color `#1F1E1B`.

```html
<div class="bc-form-row">
  <label class="bc-label">Full name</label>
  <input type="text" class="bc-input" value="Raden Rizky Adi Prasetya" />
</div>

<div class="bc-form-row">
  <label class="bc-label">What best describes your work?</label>
  <select class="bc-select">
    <option>Data science</option>
    <option>Software engineering</option>
    <option>Product design</option>
  </select>
</div>
```

---

## 10. The Artifact "Tweaks" Popover & Terracotta Action Button

Seen when interacting with BC Design Artifacts ("Design with BC Design"):

* **"Tweaks" Pill**: Solid Terracotta `#D97757` with contrast-safe dark ink text (`#1F1E1B`).
* **Floating Popover**: White card with soft elevation.
* **Input State**: Highlighted with an **accent terracotta border** (`#D97757`) and subtle warm glow ring.
* **Buttons Row**:
  * Subtle "Cancel" button.
  * **Solid Terracotta "Send" button (`#D97757`)** with contrast-safe dark ink text (`#1F1E1B`).

```html
<div class="bc-popover-box">
  <p class="bc-popover-title">Ask BC Design to add tweakable sliders or options</p>
  <textarea class="bc-input-terracotta" rows="2">
Add controls for the globe and options to see different breakpoints
  </textarea>
  <div style="display: flex; justify-content: flex-end; gap: 8px; margin-top: 12px;">
    <button class="bc-btn-glass">Cancel</button>
    <button class="bc-btn-terracotta">Send</button>
  </div>
</div>
```

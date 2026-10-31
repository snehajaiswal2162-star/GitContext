---
name: Contextual Developer Intelligence
colors:
  surface: '#10141a'
  surface-dim: '#10141a'
  surface-bright: '#353940'
  surface-container-lowest: '#0a0e14'
  surface-container-low: '#181c22'
  surface-container: '#1c2026'
  surface-container-high: '#262a31'
  surface-container-highest: '#31353c'
  on-surface: '#dfe2eb'
  on-surface-variant: '#bbcabf'
  inverse-surface: '#dfe2eb'
  inverse-on-surface: '#2d3137'
  outline: '#86948a'
  outline-variant: '#3c4a42'
  surface-tint: '#4edea3'
  primary: '#4edea3'
  on-primary: '#003824'
  primary-container: '#10b981'
  on-primary-container: '#00422b'
  inverse-primary: '#006c49'
  secondary: '#4cd7f6'
  on-secondary: '#003640'
  secondary-container: '#03b5d3'
  on-secondary-container: '#00424e'
  tertiary: '#d0bcff'
  on-tertiary: '#3c0091'
  tertiary-container: '#b090ff'
  on-tertiary-container: '#4600a7'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#6ffbbe'
  primary-fixed-dim: '#4edea3'
  on-primary-fixed: '#002113'
  on-primary-fixed-variant: '#005236'
  secondary-fixed: '#acedff'
  secondary-fixed-dim: '#4cd7f6'
  on-secondary-fixed: '#001f26'
  on-secondary-fixed-variant: '#004e5c'
  tertiary-fixed: '#e9ddff'
  tertiary-fixed-dim: '#d0bcff'
  on-tertiary-fixed: '#23005c'
  on-tertiary-fixed-variant: '#5516be'
  background: '#10141a'
  on-background: '#dfe2eb'
  surface-variant: '#31353c'
typography:
  headline-xl:
    fontFamily: Geist
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.025em
  headline-xl-mobile:
    fontFamily: Geist
    fontSize: 26px
    fontWeight: '600'
    lineHeight: 34px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Geist
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 26px
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: Geist
    fontSize: 15px
    fontWeight: '500'
    lineHeight: 22px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Geist
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: -0.01em
  body-md:
    fontFamily: Geist
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: -0.005em
  body-sm:
    fontFamily: Geist
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 18px
    letterSpacing: '0'
  label-lg:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
    letterSpacing: -0.01em
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 10px
    fontWeight: '500'
    lineHeight: 14px
    letterSpacing: 0.04em
  code-block:
    fontFamily: JetBrains Mono
    fontSize: 12.5px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: '0'
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-mobile: 0.75rem
  margin: 1.5rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 0.75rem
  space-lg: 1.25rem
  space-xl: 1.75rem
---

## Brand & Style

This design system embodies the precision, high-density clarity, and focused calm demanded by modern software engineers and technical leaders. Drawing inspiration from high-craft developer tools like Linear, Raycast, and Cursor, the aesthetic combines hyper-legible utility with refined modernism: deep void-like backdrops, luminous micro-accents, crisp hairline borders, and zero ornamental noise.

The interface evokes deep focus, effortless mastery, and immediate confidence. Every visual cue communicates operational state, semantic depth, and data freshness with surgical precision. Motion is snappy and physical (under 180ms), visual weight is distributed strictly through tonal layering and typography rather than bulky cards or aggressive shadows, and source grounding is given first-class tactile treatment.

## Colors

The palette is engineered natively for dark mode, utilizing deep cold-slate and obsidian tones to eliminate visual fatigue during sustained engineering workflows.

### Surfaces & Neutrals
- **Canvas Base:** `#090D16` – The deepest foundational viewport background.
- **Surface Layer 1 (Nav & Sidebars):** `#0D1117` – Structural panels, docked views, repository explorer.
- **Surface Layer 2 (Cards & Inspectors):** `#161B22` – Working canvas panels, query inspectors, AST node previews.
- **Surface Elevated (Floating & Modals):** `#21262D` – Command palettes, popovers, syntax search menus.
- **Hairline Borders:** `rgba(240, 246, 252, 0.1)` (`#30363D` fallback) – Structural separators and element edges.
- **Text High-Contrast:** `#F0F6FC` – Primary code, symbols, active headers.
- **Text Subdued:** `#8B949E` – File trees, metadata keys, unselected tab items.
- **Text Muted:** `#484F58` – Line numbers, disabled operations, AST syntax trivia.

### Intelligence Accents
- **Primary Emerald (`#10B981`):** Vector-indexed readiness, AST parsing verified, high semantic confidence.
- **Secondary Cyan (`#06B6D4`):** Active contextual retrieval, embedding calculations, semantic search hits.
- **Tertiary Violet (`#8B5CF6`):** LLM generation, agentic reasoning, cross-file synthesis logic.

### Telemetry & State Colors
- **Indexing / Ingestion:** `#F59E0B` (Amber 500) with glowing pulse overlay or `#06B6D4` when calculating embeddings.
- **Indexed / Grounded:** `#10B981` (Emerald 500) with a 15% opacity ambient pill fill.
- **Stale Context / Drift:** `#D97706` (Amber 600) with solid indicator dot.
- **Parsing / Ingestion Error:** `#F43F5E` (Rose 500) paired with background tint `rgba(244, 63, 94, 0.12)`.

## Typography

The typographic hierarchy relies on a dual-engine pairing: **Geist** for natural structural readability, conversational prompts, and dense metadata tables; alongside **JetBrains Mono** for all code blocks, syntax trees, commit SHAs, filepaths, line indices, and telemetry state pills.

### Typographic Rules
- **Line Heights & Tight Tracking:** Geist uses negative letter-tracking at sizes 15px and above to produce the crisp, high-density feel native to developer command consoles.
- **Monospace Isolation:** JetBrains Mono is strictly utilized whenever rendering code tokens, vector embeddings, chunk boundaries (`L12-L48`), and telemetry stats (e.g. `12.4ms`, `4,812 tokens`).
- **Tabular Figures:** Monospace and numerical data always enable open-type tabular lining (`font-variant-numeric: tabular-nums`) to ensure query times, line counts, and diff statistics align across rows without layout jitter.

## Layout & Spacing

This design system uses a fluid layout model optimized for high-density IDE environments, multi-pane split editors, and retractable telemetry drawers.

### Spacing Engine & Density
- Base scale adheres to an efficient 4px sub-grid with tight compact padding (`space-xs` = 4px, `space-sm` = 8px, `space-md` = 12px) to pack maximum codebase context into the viewport without causing claustrophobia.
- Interactive controls maintain a compact default height of 32px (down to 26px for micro-actions and filter pills in breadcrumb bars).

### Viewport Breakpoints & Adapters
- **Desktop (≥ 1280px):** 3-column split active: Collapsible repository tree and AST map (260px–320px fixed), primary retrieval copilot stream (fluid), and inspect/grounding drawer (380px fixed).
- **Tablet (768px – 1279px):** 2-column mode; AST tree moves to a slide-over panel, retaining fluid main copilot stream and tabbed inspector.
- **Mobile (< 768px):** Single-column stacked mode with persistent bottom status strip indicating indexing health and branch sync status. Margins contract to `margin-mobile` (16px).

## Elevation & Depth

Visual hierarchy does not rely on heavy drop shadows or skeuomorphic bevels. Instead, depth is articulated through low-contrast hairline borders, dark surface luminance layering, and localized intelligence glow effects.

### Tonal Surface Stack
- **Floor (`#090D16`):** The ground level. Transparent to subtle sub-pixel dot patterns or vector chunk heatmaps.
- **Tier 1 (`#0D1117`):** Navigational framing and persistent sidebars. Bordered with `1px solid rgba(255, 255, 255, 0.08)`.
- **Tier 2 (`#161B22`):** Cards, terminal blocks, code chunks, grounded reference panels. Features a `1px` inner highlight `inset 0 1px 0 rgba(255, 255, 255, 0.05)`.
- **Tier 3 (`#21262D`):** Command palettes, floating tooltips, and contextual dropdowns.

### Hairline Borders & Edge Radiance
- Elements are defined by a crisp 1px border using `rgba(240, 246, 252, 0.1)`.
- Active focus states use a hairline stroke of the accent color paired with an ultra-soft radial glow:
  - Cyan context retrieval: `box-shadow: 0 0 0 1px #06B6D4, 0 0 16px -4px rgba(6, 182, 212, 0.25);`
  - Emerald grounded completion: `box-shadow: 0 0 0 1px #10B981, 0 0 16px -4px rgba(16, 185, 129, 0.25);`
  - Violet copilot thinking: `box-shadow: 0 0 0 1px #8B5CF6, 0 0 16px -4px rgba(139, 92, 246, 0.25);`

## Shapes

The design system operates with soft, technical geometry (level `1`). Surfaces feel engineered, compact, and structured like high-end developer hardware.

### Corner Radii Guidelines
- **Input Fields, Terminal Pills, Table Rows:** `0.25rem` (4px). Provides tight alignment with code blocks and terminal interfaces.
- **Cards, AST Code Panels, Floating Drawers:** `0.5rem` (8px). Softens modular components while preserving strict geometric grid alignment.
- **Global Modals, Command Bar (`Cmd+K`):** `0.75rem` (12px). Distinct floating hierarchy.
- **Status Badges & Line Indicator Badges:** Full-pill (`9999px`) for compact state indicators (`Indexing`, `Indexed`, `L32-40`).

## Components

### Buttons
- **Primary (Grounded / Action):** Solid emerald background (`#10B981`), dark slate text (`#090D16`), 500 font weight, 32px height, 4px border radius. Hover introduces a brightened emerald tint (`#34D399`) and subtle cyan-tinged ambient bloom.
- **Secondary / Ghost:** Transparent background with `#161B22` fill, framed by `1px solid rgba(255, 255, 255, 0.1)`. Text is `#F0F6FC`. On hover, background shifts to `#21262D`.
- **Micro-Action (Icon-only / Copy SHA / Insert Code):** 24px x 24px square, 4px radius, transparent fill, text `#8B949E`. Hover reveals `#161B22` and text `#F0F6FC`.

### Status Badges & State Indicators
Pills with a height of 20px, uppercase 10px JetBrains Mono typography, padding 0 8px, and a leading 6px circular dot:
- **Indexing:** Background `rgba(245, 158, 11, 0.12)`, text `#FBBF24`, dot `#F59E0B` with an animated 1.5s ease-in-out breathing pulse opacity (`0.4` to `1.0`).
- **Indexed:** Background `rgba(16, 185, 129, 0.12)`, text `#34D399`, dot `#10B981` (static steady glow).
- **Stale:** Background `rgba(217, 119, 6, 0.12)`, text `#F59E0B`, dot `#D97706`.
- **Error:** Background `rgba(244, 63, 94, 0.12)`, text `#FB7185`, dot `#F43F5E`.

### Grounded Source Citation Pills
- Clickable metadata chips displaying repository filepath and chunk range (e.g., `src/indexer/ast.ts:42-88`).
- Background `#161B22`, border `1px solid rgba(255, 255, 255, 0.1)`, 22px height, 6px horizontal padding.
- Typography: 11px JetBrains Mono in `#8B949E`. Hover transitions text to `#06B6D4` (Cyan) and border to `rgba(6, 182, 212, 0.4)`.

### Code Reference & AST Cards
- Background `#161B22`, 1px border in `rgba(255, 255, 255, 0.08)`, 8px corner radius.
- Header strip: 30px height, background `#0D1117`, border-bottom `1px solid rgba(255, 255, 255, 0.06)`, housing breadcrumb path, language badge, and clipboard action.
- Code viewport: Inset padding 12px, syntax highlighted with strict dark tones, and alternating 2px accent bar on left for semantic match spans.

### Input Fields & Command Bar
- Inset dark input (`#0D1117`), border `1px solid rgba(255, 255, 255, 0.1)`, text `#F0F6FC`, placeholder `#484F58`.
- Focus ring: zero native browser outline, replaced by `1px solid #10B981` with an inner 1px cyan tint glow.
- Includes embedded shortcut token caps on the right side (e.g., `⌘K`, `Enter ↵`) styled with `#21262D` background and `#8B949E` 10px JetBrains Mono font.

### Checkboxes & Radios
- 14px x 14px compact square, 3px border radius, border `1px solid #30363D`, background `#0D1117`.
- Selected state fills with `#10B981` and renders a `#090D16` checkmark path.
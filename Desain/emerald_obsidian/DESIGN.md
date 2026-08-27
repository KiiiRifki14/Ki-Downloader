---
name: Emerald Obsidian
colors:
  surface: '#f7f9fb'
  surface-dim: '#d8dadc'
  surface-bright: '#f7f9fb'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f4f6'
  surface-container: '#eceef0'
  surface-container-high: '#e6e8ea'
  surface-container-highest: '#e0e3e5'
  on-surface: '#191c1e'
  on-surface-variant: '#3d4a42'
  inverse-surface: '#2d3133'
  inverse-on-surface: '#eff1f3'
  outline: '#6d7a72'
  outline-variant: '#bccac0'
  surface-tint: '#006c4a'
  primary: '#006948'
  on-primary: '#ffffff'
  primary-container: '#00855d'
  on-primary-container: '#f5fff7'
  inverse-primary: '#68dba9'
  secondary: '#006c4e'
  on-secondary: '#ffffff'
  secondary-container: '#97f5cc'
  on-secondary-container: '#007353'
  tertiary: '#9b3e3b'
  on-tertiary: '#ffffff'
  tertiary-container: '#ba5551'
  on-tertiary-container: '#fffbff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#85f8c4'
  primary-fixed-dim: '#68dba9'
  on-primary-fixed: '#002114'
  on-primary-fixed-variant: '#005137'
  secondary-fixed: '#97f5cc'
  secondary-fixed-dim: '#7bd8b1'
  on-secondary-fixed: '#002115'
  on-secondary-fixed-variant: '#00513a'
  tertiary-fixed: '#ffdad7'
  tertiary-fixed-dim: '#ffb3ae'
  on-tertiary-fixed: '#410004'
  on-tertiary-fixed-variant: '#7f2928'
  background: '#f7f9fb'
  on-background: '#191c1e'
  surface-variant: '#e0e3e5'
  charcoal-dark: '#0f172a'
  charcoal-muted: '#1e293b'
  slate-border: '#e2e8f0'
  muted-slate-text: '#64748b'
  mint-surface: '#ecfdf5'
  mint-accent: '#d1fae5'
typography:
  headline-lg:
    fontFamily: Manrope
    fontSize: 40px
    fontWeight: '800'
    lineHeight: 48px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Manrope
    fontSize: 28px
    fontWeight: '800'
    lineHeight: 34px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Manrope
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  headline-sm:
    fontFamily: Manrope
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  touch-target-min: 54px
  gutter: 16px
  margin-mobile: 20px
  margin-desktop: auto
  container-max-width: 800px
  stack-gap: 24px
---

## Brand & Style

The design system is anchored in a **Premium Modernist** aesthetic, specifically tailored for a high-utility mobile utility tool. It rejects the aggressive, high-saturation "neon" trends of typical downloader sites in favor of a sophisticated, editorial-grade interface. The personality is efficient, reliable, and "Apple-esque" in its restraint.

The style leverages **Minimalism** with a focus on tactile interaction. By utilizing a "Snow White" and "Slate Light" foundation, the interface feels expansive even on small mobile screens. Interaction points are characterized by large tap targets and subtle elevation shifts, ensuring the user feels a sense of quality and "mechanical" precision during the link-processing workflow.

**Design Principles:**
- **Clarity over Clutter:** Every element must serve a functional purpose in the downloading journey.
- **Organic Precision:** Combining strict grid alignment with soft, rounded corners to feel approachable yet professional.
- **Visual Silence:** High use of white space to isolate the primary call-to-action (the URL input).

## Colors

The palette is built on the **Emerald Obsidian** concept. It uses a range of deep greens for primary actions to convey success and growth, contrasting against a base of cool slates.

- **Primary & Secondary:** A transition from `#059669` to `#047857` is used for primary buttons and brand accents. This gradient should be subtle, applied top-to-bottom.
- **Surface Palette:** The background uses `Snow White` (#ffffff) for primary content cards and `Slate Light` (#f8fafc) for the page background to create a tiered depth effect.
- **Typography:** `Charcoal Dark` (#0f172a) is reserved for high-hierarchy headings to ensure maximum legibility, while `Muted Slate` (#64748b) handles all secondary metadata and descriptions.
- **Strict Policy:** Neon greens (#00ff00) and artificial glows are strictly prohibited to maintain the premium positioning.

## Typography

This design system uses **Manrope** for headlines to provide a modern, geometric, and technical feel that aligns with a "downloader" tool. Its high legibility and balanced proportions make it ideal for the "Ki.Downloader" wordmark and section titles.

**Inter** is utilized for body text and labels for its neutral, functional utility. It ensures that complex metadata (file sizes, formats, URLs) remains clear and unobtrusive.

**Implementation Notes:**
- **Input Text:** Must remain at `16px` on mobile to prevent browser-level layout shifting (iOS auto-zoom).
- **Letter Spacing:** Headlines use a slight negative tracking (-0.02em) to appear tighter and more "designed."
- **Contrast:** Headings use `Charcoal Dark`, while body text uses the `Muted Slate` to establish a clear information hierarchy.

## Layout & Spacing

The layout follows a **Mobile-First Responsive** model. 

- **Mobile:** A single-column vertical stack. Content is housed in cards that span the full width of the viewport minus the 20px side margins. 
- **Desktop:** The layout centralizes into a 12-column grid with a maximum container width of 800px for the primary tool area, ensuring the user's focus remains on the input field. Results cards can expand to a 2 or 3-column grid depending on screen width.
- **Rhythm:** A base-8 spacing system is used. Gaps between related elements (like an input and its label) are 8px, while gaps between distinct sections or cards are 24px-32px.
- **Touch Areas:** All interactive elements (buttons, pills, inputs) must maintain a minimum height of `54px` to accommodate thumb-driven navigation.

## Elevation & Depth

This design system uses **Tonal Layers** combined with **Ambient Shadows** to create a premium feel without resorting to heavy gradients.

- **The Base:** The `Slate Light` background acts as the lowest layer.
- **The Cards:** White surfaces (`#ffffff`) are elevated using a custom "Soft Elevation Shadow": `box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04)`. This creates a floating effect that is barely perceptible but provides a clear distinction from the background.
- **Borders:** To define shapes clearly on bright screens, containers use a `1px` solid border in `Slate Border` (#e2e8f0).
- **Active State:** When an element is interacted with, the shadow should deepen slightly, and the border color should shift to the Primary Emerald for focus states.

## Shapes

The shape language is defined by **Soft Roundedness** with specific emphasis on pill-shaped elements for interaction.

- **Inputs & Primary Buttons:** Use a specific `14px` border-radius. This curvature is significant enough to feel modern and friendly but maintains enough structure for a professional utility.
- **Result Cards:** Follow the standard `rounded-lg` (16px) to house content comfortably.
- **Format Pills:** Use a fully rounded/pill shape (999px) for format selection (MP4, MP3) to differentiate them from primary action buttons.

## Components

### Buttons
- **Primary Action:** Large (min-height 54px), `#059669` background, white text. Subtle gradient to `#047857`.
- **Secondary/Paste:** Sits adjacent to the input, uses `Mint Surface` background with `Primary Emerald` text.

### Input Fields
- **URL Input:** `14px` rounded corners, `16px` font size. On focus, the border changes to `Primary Emerald` with a `4px` spread soft ring shadow at 15% opacity.

### Result Cards
- **Structure:** Features a top media preview (240px height, `object-fit: cover`), followed by a platform badge (e.g., TikTok logo), the title in `Charcoal Dark`, and a bottom row of format pill buttons.
- **Shadow:** Applied as per the Elevation section (Soft Elevation).

### Pills (Format Selection)
- Small, rounded-full elements. Inactive: `Slate Border` outline. Active: `Primary Emerald` background with white text.

### Badge Status
- "⚡ Multi-Media Ready": Small uppercase label using `Mint Accent` background and `Primary Emerald` text, placed in the header for immediate credibility.

### Slots (Ads)
- Ad containers should maintain the same `14px` roundedness as the UI to feel integrated. They should be clearly labeled with a `label-sm` "ADVERTISEMENT" tag in `Muted Slate`.
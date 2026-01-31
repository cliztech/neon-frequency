## 2024-05-22 - Transport Controls Accessibility
**Learning:** Critical control components like `TransportControls` used icon-only buttons (Lucide icons) without `aria-label` or `title` attributes, making them inaccessible to screen readers and confusing for some users. Keyboard focus indicators were also missing.
**Action:** When working on control panels in this app, always check for icon-only buttons and ensure they have dynamic `aria-label` (for stateful buttons like Play/Stop), `title` tooltips, and explicit `focus-visible` styles using the theme's `neon-cyan` color.

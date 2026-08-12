# Tinkr — Component Library

> The 12 components that ship in v1. Each one has one job, one anatomy, seven states, accessibility rules, and working HTML + Tailwind.
> All examples assume the design tokens from `03-design-tokens.json` are loaded as CSS variables. The Tailwind classes reference the brand colors directly for clarity; in production, use the token-driven config.

---

## Conventions used in every example

- **Color shortcuts** — `bg-primary` = `bg-brand-primary`, `text-fg` = `text-text-primary-{theme}`, `border-default` = `border-border-default-{theme}`. Tokens resolve to light or dark via the `data-theme` attribute on `<html>`.
- **Default theme is dark.** The light examples are shown explicitly with `data-theme="light"`.
- **Inter is the UI font**, JetBrains Mono is the code font. All examples assume both are loaded.
- **Icons are Lucide.** Use `<svg>` inline with the icon name as a comment for clarity.
- **Focus rings are mandatory.** The class `focus-visible:ring-2 focus-visible:ring-brand-primary focus-visible:ring-offset-2 focus-visible:ring-offset-surface-bg` is on every interactive element.

---

## 1. Button

The primary action surface. Triggers a single, well-defined behavior.

### 1.1 Anatomy

```
┌─────────────────────────┐
│  [icon]  Label  [icon]  │
└─────────────────────────┘
     ↑           ↑
   leading     trailing
   (optional)  (optional, e.g. arrow)
```

- **Label**: required, 1–3 words, sentence case. ("Deploy to device" not "Deploy To Device".)
- **Leading icon**: optional. Use when the icon adds meaning the label doesn't carry.
- **Trailing icon**: optional. Almost always a chevron or arrow indicating progression.
- **No label**: icon-only buttons are allowed but must have `aria-label`.

### 1.2 Variants

| Variant | Background | Text | Border | Usage |
|---|---|---|---|---|
| **Primary** | `bg-brand-accent` | `text-text-inverse-dark` | none | The single most important action on a screen. Use once. |
| **Secondary** | `bg-surface-raised-{theme}` | `text-text-primary-{theme}` | `border-border-default-{theme}` | The second most important. Cancel, back, alternative actions. |
| **Ghost** | transparent | `text-text-primary-{theme}` | none | Tertiary actions. Inline in text, table rows, card actions. |
| **Danger** | `bg-status-error` | `text-text-inverse-dark` | none | Destructive actions. Erase flash, delete project, uninstall plugin. |

### 1.3 Sizes

| Size | Height | Padding (x) | Font size | Icon | Usage |
|---|---|---|---|---|---|
| `sm` | 28 px | 12 px | 14 px | 16 px | Tables, dense toolbars |
| `md` | 36 px | 16 px | 14 px | 20 px | Default |
| `lg` | 44 px | 20 px | 16 px | 20 px | Primary CTAs, hero |

### 1.4 States

| State | Visual change | Notes |
|---|---|---|
| **Default** | as variant | |
| **Hover** | background → `-dim` of the variant color | +1 elevation, never scale |
| **Active / pressed** | background → `-dim` again | stays pressed for the duration of the click |
| **Focus** | `ring-2 ring-brand-primary ring-offset-2 ring-offset-surface-bg` | visible on keyboard, not on click |
| **Disabled** | `opacity-50 cursor-not-allowed` | `disabled` attribute, not just visual |
| **Loading** | label → spinner + "Working…"; button is `aria-busy="true"` and disabled | the action is in progress, not silent |
| **Error** | for a moment after a failed action: shake + red border (200 ms) | then revert; show error via toast |

### 1.5 Spacing rules

- 8 px minimum gap between adjacent buttons.
- In a button group (Save / Cancel), the primary is on the right; the secondary is on the left.
- A button never sits alone with no surrounding padding — minimum 16 px from the nearest edge.

### 1.6 Accessibility

- Always a real `<button>` element (not a div).
- Always has visible or `aria-` text.
- Loading state uses `aria-busy="true"`.
- Disabled state uses the `disabled` attribute (not just visual styling).
- Trailing-icon-only buttons (rare) need `aria-label`.

### 1.7 Code — Primary (md)

```html
<button
  type="button"
  class="inline-flex items-center justify-center gap-2
         h-9 px-4 rounded-md
         bg-brand-accent text-text-inverse-dark font-medium text-sm
         hover:bg-brand-accent-dim
         active:bg-brand-accent-dim
         focus-visible:outline-none focus-visible:ring-2
         focus-visible:ring-brand-primary focus-visible:ring-offset-2
         focus-visible:ring-offset-surface-bg
         disabled:opacity-50 disabled:cursor-not-allowed
         transition-colors duration-150"
>
  <!-- icon: lucide/zap -->
  <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
  </svg>
  Deploy to device
</button>
```

### 1.8 Code — Secondary (md)

```html
<button
  type="button"
  class="inline-flex items-center justify-center gap-2
         h-9 px-4 rounded-md
         bg-surface-raised-dark text-text-primary-dark font-medium text-sm
         border border-border-default-dark
         hover:bg-surface-sunken-dark
         active:bg-surface-sunken-dark
         focus-visible:outline-none focus-visible:ring-2
         focus-visible:ring-brand-primary focus-visible:ring-offset-2
         focus-visible:ring-offset-surface-bg
         disabled:opacity-50 disabled:cursor-not-allowed
         transition-colors duration-150"
>
  Cancel
</button>
```

### 1.9 Code — Ghost (sm, icon-only)

```html
<button
  type="button"
  aria-label="Copy to clipboard"
  class="inline-flex items-center justify-center
         w-7 h-7 rounded-md
         text-text-secondary-dark
         hover:bg-surface-raised-dark hover:text-text-primary-dark
         active:bg-surface-sunken-dark
         focus-visible:outline-none focus-visible:ring-2
         focus-visible:ring-brand-primary focus-visible:ring-offset-2
         focus-visible:ring-offset-surface-bg
         disabled:opacity-50 disabled:cursor-not-allowed
         transition-colors duration-150"
>
  <!-- icon: lucide/copy -->
  <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <rect width="14" height="14" x="8" y="8" rx="2" ry="2"/>
    <path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>
  </svg>
</button>
```

---

## 2. Input

Text input for single-line values. The same component handles text, number, password, and search.

### 2.1 Anatomy

```
   Label *
   ┌────────────────────────────┐
   │ Value          [icon] [👁] │  ← input
   └────────────────────────────┘
   Helper text or error message
```

- **Label**: required, above the input, sentence case.
- **Required marker**: `*` next to the label, in `status-error` for color + visible `*` for the marker.
- **Input**: the value.
- **Leading icon**: optional, for search (`ui-search`) or known prefixes.
- **Trailing icon**: optional, for password toggle, clear button, etc.
- **Helper text**: below the input, `text-secondary-{theme}`. Replaced by error message on error.
- **Error message**: below the input, `text-status-error`, with a specific message and an `aria-describedby` link.

### 2.2 States

| State | Border | Background | Notes |
|---|---|---|---|
| **Default** | `border-default-{theme}` | `bg-surface-raised-{theme}` | |
| **Hover** | `border-strong-{theme}` | same | |
| **Focus** | `border-brand-primary` + ring | same | visible focus, never removed |
| **Filled** | `border-default-{theme}` | same | shows the value is committed |
| **Disabled** | `border-subtle-{theme}` | `bg-surface-sunken-{theme}` | `disabled` attribute |
| **Error** | `border-status-error` | same | error message below, `aria-invalid="true"` |
| **Loading** | spinner on the right | same | for async validation |

### 2.3 Sizes

| Size | Height | Padding (x) | Font size |
|---|---|---|---|
| `sm` | 28 px | 12 px | 14 px |
| `md` | 36 px | 12 px | 14 px (default) |
| `lg` | 44 px | 16 px | 16 px |

### 2.4 Accessibility

- Always a real `<input>` (not a div with `contenteditable`).
- Label is always associated via `<label for="id">` or wrapping.
- Error message uses `aria-describedby` to link to the input.
- Required uses `aria-required="true"` and a visible `*`.
- Search inputs use `type="search"` and `role="searchbox"` on the wrapping form.

### 2.5 Code — Text input (md)

```html
<div class="flex flex-col gap-1.5">
  <label for="device-name" class="text-sm font-medium text-text-primary-dark">
    Device name <span class="text-status-error" aria-hidden="true">*</span>
  </label>
  <div class="relative">
    <input
      id="device-name"
      name="device-name"
      type="text"
      required
      aria-required="true"
      placeholder="esp32s3-left"
      class="w-full h-9 px-3 rounded-md
             bg-surface-raised-dark text-text-primary-dark
             placeholder:text-text-tertiary-dark
             border border-border-default-dark
             hover:border-border-strong-dark
             focus:outline-none focus:border-brand-primary
             focus-visible:ring-2 focus-visible:ring-brand-primary
             focus-visible:ring-offset-2 focus-visible:ring-offset-surface-bg
             disabled:opacity-50 disabled:cursor-not-allowed
             transition-colors duration-150"
    />
  </div>
  <p class="text-xs text-text-secondary-dark">
    Used as the default device ID for this project. Lowercase, hyphens allowed.
  </p>
</div>
```

### 2.6 Code — Error state

```html
<div class="flex flex-col gap-1.5">
  <label for="port" class="text-sm font-medium text-text-primary-dark">
    Serial port <span class="text-status-error" aria-hidden="true">*</span>
  </label>
  <input
    id="port"
    name="port"
    type="text"
    required
    aria-required="true"
    aria-invalid="true"
    aria-describedby="port-error"
    value="/dev/cu.usbserial-XXXX"
    class="w-full h-9 px-3 rounded-md
           bg-surface-raised-dark text-text-primary-dark
           border border-status-error
           focus:outline-none focus:ring-2
           focus:ring-status-error focus:ring-offset-2 focus:ring-offset-surface-bg"
  />
  <p id="port-error" class="text-xs text-status-error flex items-center gap-1">
    <!-- icon: lucide/alert-circle -->
    <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <circle cx="12" cy="12" r="10"/>
      <line x1="12" y1="8" x2="12" y2="12"/>
      <line x1="12" y1="16" x2="12.01" y2="16"/>
    </svg>
    No device found at this port. Check the USB cable.
  </p>
</div>
```

---

## 3. Card

A container for related content with a single topic. The default for plugin entries, device cards, KB entries, and feature blocks.

### 3.1 Variants

| Variant | Border | Background | Usage |
|---|---|---|---|
| **Basic** | `border-default-{theme}` | `bg-surface-raised-{theme}` | Default |
| **With header / footer** | `border-default-{theme}` | `bg-surface-raised-{theme}` | Header has title + actions, footer has meta |
| **With actions** | `border-default-{theme}` | `bg-surface-raised-{theme}` | Action row at the top-right (more menu, pin) |
| **With badge** | `border-default-{theme}` | `bg-surface-raised-{theme}` | Status badge in the corner (stable, beta, deprecated) |
| **Interactive** | `border-default-{theme}` | `bg-surface-raised-{theme}` | Hover state makes it look pressable (the entire card is the click target) |

### 3.2 Anatomy (plugin card example)

```
┌──────────────────────────────────────────┐
│  [chip-icon]  tinkr-esp32          [ⓘ]  │  ← header
│  ESP32 family support                    │  ← subtitle
│ ──────────────────────────────────────── │
│  flash · repl · fs · plotter             │  ← capabilities row
│  v1.2.3 · stable · 12.4k downloads       │  ← meta
│  [Install]  [Details]                    │  ← actions
└──────────────────────────────────────────┘
```

### 3.3 States (interactive only)

| State | Visual change |
|---|---|
| **Default** | `border-default-{theme}` |
| **Hover** | `border-strong-{theme}` + slight `bg-surface-sunken-{theme}` shift |
| **Active / pressed** | `bg-surface-sunken-{theme}` |
| **Focus** | ring around the whole card |

### 3.4 Spacing

- Internal padding: 16 px (md) or 24 px (lg)
- Between cards in a grid: 16 px
- Header → body gap: 12 px
- Body → footer gap: 16 px
- Title → subtitle gap: 4 px

### 3.5 Accessibility

- Static cards are `<div>` with no role.
- Interactive cards are `<a>` or `<button>` (not both, not div+onclick).
- The card's accessible name comes from its title or an `aria-label`.
- The card's actions are also independently focusable for keyboard users.

### 3.6 Code — Plugin card (interactive)

```html
<a
  href="/plugins/tinkr-esp32"
  class="block rounded-lg
         bg-surface-raised-dark
         border border-border-default-dark
         hover:border-border-strong-dark hover:bg-surface-sunken-dark
         focus-visible:outline-none focus-visible:ring-2
         focus-visible:ring-brand-primary focus-visible:ring-offset-2
         focus-visible:ring-offset-surface-bg
         transition-colors duration-150"
>
  <div class="p-4 flex flex-col gap-3">
    <!-- header -->
    <div class="flex items-start justify-between gap-3">
      <div class="flex items-center gap-2">
        <!-- icon: device-chip -->
        <svg class="w-5 h-5 text-brand-primary" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <rect x="4" y="4" width="16" height="16" rx="2"/>
          <rect x="9" y="9" width="6" height="6"/>
          <line x1="9" y1="1" x2="9" y2="4"/>
          <line x1="15" y1="1" x2="15" y2="4"/>
          <line x1="9" y1="20" x2="9" y2="23"/>
          <line x1="15" y1="20" x2="15" y2="23"/>
          <line x1="20" y1="9" x2="23" y2="9"/>
          <line x1="20" y1="14" x2="23" y2="14"/>
          <line x1="1" y1="9" x2="4" y2="9"/>
          <line x1="1" y1="14" x2="4" y2="14"/>
        </svg>
        <span class="text-base font-semibold text-text-primary-dark">tinkr-esp32</span>
      </div>
      <!-- badge: stable -->
      <span class="text-caption font-medium uppercase tracking-wide px-2 py-0.5 rounded-full
                   bg-status-success-surface-dark text-status-success">
        stable
      </span>
    </div>

    <!-- subtitle -->
    <p class="text-sm text-text-secondary-dark -mt-2">
      ESP32 family support via esptool and minny
    </p>

    <!-- meta -->
    <div class="flex items-center gap-3 text-xs text-text-tertiary-dark">
      <span>v1.2.3</span>
      <span aria-hidden="true">·</span>
      <span>12.4k downloads</span>
      <span aria-hidden="true">·</span>
      <span>flash · repl · fs · plotter</span>
    </div>
  </div>
</a>
```

---

## 4. Modal

An overlay that interrupts the current task to deliver a focused action or message. Use sparingly — modals are heavy.

### 4.1 Sizes

| Size | Width | Usage |
|---|---|---|
| `sm` | 384 px | Confirmations, single-field forms |
| `md` | 512 px | Default for most modals |
| `lg` | 768 px | Multi-step forms, plugin detail preview |
| `fullscreen` | 100 vw × 100 vh | The Tauri shell's main view, the command palette |

### 4.2 Anatomy

```
       backdrop (scrim, focus trap, Esc to close)
   ┌─────────────────────────────────────┐
   │  Title                          [×] │  ← header
   ├─────────────────────────────────────┤
   │                                     │
   │  Body content.                       │  ← body (scrolls)
   │                                     │
   ├─────────────────────────────────────┤
   │       [Cancel]  [Confirm]            │  ← footer (right-aligned)
   └─────────────────────────────────────┘
```

### 4.3 States

| State | Visual change |
|---|---|
| **Open** | fade in (200 ms) + scale from 95% to 100% |
| **Closing** | fade out (150 ms) + scale to 95% |
| **Backdrop click** | closes the modal (unless `static` mode) |

### 4.4 Rules

- One primary action, one secondary (cancel). Never more.
- The primary is on the right. Cancel is on the left.
- Pressing Esc closes the modal.
- Focus is trapped inside the modal. Focus returns to the trigger on close.
- Body scroll is locked while the modal is open.
- The backdrop has `bg-surface-bg-dark opacity-60` (the `scrim` opacity).

### 4.5 Accessibility

- Uses `role="dialog"`, `aria-modal="true"`, `aria-labelledby="title-id"`, `aria-describedby="body-id"`.
- Initial focus goes to the first focusable element, or the primary action.
- The `aria-label` of the close button is "Close".
- The body content is wrapped in `<main>` for screen reader landmark navigation.

### 4.6 Code — Confirmation modal

```html
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
  aria-describedby="modal-body"
  class="fixed inset-0 z-modal
         flex items-center justify-center p-4
         bg-surface-bg-dark/60 backdrop-blur-sm"
>
  <div class="w-full max-w-md rounded-lg
              bg-surface-raised-dark
              border border-border-default-dark
              shadow-lg">
    <!-- header -->
    <div class="flex items-center justify-between p-4 border-b border-border-subtle-dark">
      <h2 id="modal-title" class="text-lg font-semibold text-text-primary-dark">
        Erase flash and deploy?
      </h2>
      <button
        type="button"
        aria-label="Close"
        class="w-7 h-7 rounded-md flex items-center justify-center
               text-text-secondary-dark hover:text-text-primary-dark
               hover:bg-surface-sunken-dark
               focus-visible:outline-none focus-visible:ring-2
               focus-visible:ring-brand-primary">
        <!-- icon: x -->
        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M18 6 6 18"/><path d="m6 6 12 12"/>
        </svg>
      </button>
    </div>

    <!-- body -->
    <div id="modal-body" class="p-4">
      <p class="text-sm text-text-secondary-dark">
        This will erase all data on the device and deploy
        <code class="font-mono text-text-primary-dark">main.py</code> to
        <code class="font-mono text-text-primary-dark">/</code>.
        The device will reboot.
      </p>
    </div>

    <!-- footer -->
    <div class="flex items-center justify-end gap-2 p-4 border-t border-border-subtle-dark">
      <button
        type="button"
        class="h-9 px-4 rounded-md text-sm font-medium
               text-text-primary-dark bg-surface-sunken-dark
               hover:bg-surface-bg-dark
               focus-visible:outline-none focus-visible:ring-2
               focus-visible:ring-brand-primary focus-visible:ring-offset-2
               focus-visible:ring-offset-surface-raised-dark">
        Cancel
      </button>
      <button
        type="button"
        class="h-9 px-4 rounded-md text-sm font-medium
               bg-status-error text-text-inverse-dark
               hover:bg-status-error-dim
               focus-visible:outline-none focus-visible:ring-2
               focus-visible:ring-brand-primary focus-visible:ring-offset-2
               focus-visible:ring-offset-surface-raised-dark">
        Erase and deploy
      </button>
    </div>
  </div>
</div>
```

---

## 5. Toast / Notification

A transient, non-blocking message about the outcome of an action. Auto-dismisses. Stack vertically in the bottom-right.

### 5.1 Variants

| Variant | Color | Icon | Usage |
|---|---|---|---|
| **Info** | `status-info` | `info` | Informational. "Plugin published to registry." |
| **Success** | `status-success` | `check-circle` | Confirmations. "Deployed. LED tinkring." |
| **Warning** | `status-warning` | `alert-triangle` | Non-blocking issues. "Plugin is in beta." |
| **Error** | `status-error` | `alert-octagon` | Failures. "Couldn't connect to device." |

### 5.2 Anatomy

```
                                          ┌──────────────────────────────────┐
                                          │ [icon]  Title             [×]     │
                                          │        Description text here.    │
                                          │        [Action]                   │
                                          └──────────────────────────────────┘
                                          ↑ bottom-right, stacked
```

- **Title**: required, 1 line, sentence case, the outcome.
- **Description**: optional, 1–2 lines, what happened / what to do.
- **Action**: optional, one button (Retry, Undo, View).
- **Close**: always present, dismisses the toast.

### 5.3 Behavior

- **Duration**: 5 s (info, success), 8 s (warning), persistent (error — requires user dismissal).
- **Stacking**: new toasts push old ones down. Max 5 visible; the oldest auto-dismisses.
- **Position**: bottom-right, 16 px from the edge.
- **Animation**: slides in from the right (200 ms), fades out (150 ms).

### 5.4 Accessibility

- Uses `role="status"` (info, success) or `role="alert"` (warning, error).
- `aria-live="polite"` (info, success) or `aria-live="assertive"` (warning, error).
- The close button has `aria-label="Dismiss"`.
- The action button is focusable; the toast itself is not in the tab order.

### 5.5 Code — Success toast

```html
<div
  role="status"
  aria-live="polite"
  class="flex items-start gap-3
         w-96 p-4 rounded-lg
         bg-status-success-surface-dark
         border border-status-success
         shadow-md"
>
  <!-- icon: check-circle -->
  <svg class="w-5 h-5 text-status-success shrink-0 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
    <polyline points="22 4 12 14.01 9 11.01"/>
  </svg>
  <div class="flex-1 min-w-0">
    <p class="text-sm font-semibold text-text-primary-dark">Deployed</p>
    <p class="text-sm text-text-secondary-dark mt-0.5">
      main.py is on esp32s3-left. LED tinkring.
    </p>
  </div>
  <button
    type="button"
    aria-label="Dismiss"
    class="shrink-0 w-6 h-6 rounded flex items-center justify-center
           text-text-secondary-dark hover:text-text-primary-dark
           focus-visible:outline-none focus-visible:ring-2
           focus-visible:ring-brand-primary">
    <!-- icon: x -->
    <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <path d="M18 6 6 18"/><path d="m6 6 12 12"/>
    </svg>
  </button>
</div>
```

---

## 6. Badge / Pill

A small, inline status indicator. Used for plugin maturity, device state, and KB entry type.

### 6.1 Variants

| Variant | Background | Text | Usage |
|---|---|---|---|
| **Default** | `bg-surface-sunken-{theme}` | `text-text-primary-{theme}` | Generic |
| **Success** | `bg-status-success-surface-{theme}` | `text-status-success` | Stable, connected, healthy |
| **Warning** | `bg-status-warning-surface-{theme}` | `text-status-warning` | Beta, slow, deprecated |
| **Error** | `bg-status-error-surface-{theme}` | `text-status-error` | Failed, broken, missing |
| **Info** | `bg-status-info-surface-{theme}` | `text-status-info` | New, experimental, update available |
| **Accent** | `bg-brand-accent` | `text-text-inverse-dark` | Featured, paid, recommended |

### 6.2 Sizes

| Size | Height | Padding (x) | Font size | Usage |
|---|---|---|---|---|
| `sm` | 18 px | 6 px | 11 px | Inline with body-sm, dense tables |
| `md` | 22 px | 8 px | 12 px | Default |
| `lg` | 26 px | 10 px | 13 px | Empty states, headers |

### 6.3 States

Badges are static. No hover, no active. They are status, not action.

### 6.4 Code

```html
<!-- stable (success) -->
<span class="inline-flex items-center gap-1
             h-5 px-2 rounded-full
             text-caption font-medium uppercase tracking-wide
             bg-status-success-surface-dark text-status-success">
  stable
</span>

<!-- beta (warning) -->
<span class="inline-flex items-center gap-1
             h-5 px-2 rounded-full
             text-caption font-medium uppercase tracking-wide
             bg-status-warning-surface-dark text-status-warning">
  beta
</span>

<!-- experimental (info) -->
<span class="inline-flex items-center gap-1
             h-5 px-2 rounded-full
             text-caption font-medium uppercase tracking-wide
             bg-status-info-surface-dark text-status-info">
  experimental
</span>

<!-- deprecated (error) -->
<span class="inline-flex items-center gap-1
             h-5 px-2 rounded-full
             text-caption font-medium uppercase tracking-wide
             bg-status-error-surface-dark text-status-error">
  deprecated
</span>
```

---

## 7. Table

Tabular data with optional sorting, selection, and pagination. The default for plugin lists, device lists, and KB search results.

### 7.1 Anatomy

```
   ┌──────────────────────────────────────────────────────────┐
   │  ☐  Name              Version   Maturity   Devices   ⋮  │  ← header
   ├──────────────────────────────────────────────────────────┤
   │  ☐  tinkr-esp32       1.2.3     stable     2/3      ⋮  │  ← row
   │  ☐  tinkr-rp2040      0.8.0     beta       0/1      ⋮  │
   │  ☐  tinkr-sniffer     0.1.2     exp.       -        ⋮  │
   └──────────────────────────────────────────────────────────┘
                  [‹ 1 2 3 … 12 ›]                              ← pagination
```

### 7.2 States

- **Row default**: transparent background, `border-subtle-{theme}` bottom border.
- **Row hover**: `bg-surface-sunken-{theme}`.
- **Row selected**: `bg-brand-primary/10` (10% opacity primary tint).
- **Row focused**: visible focus ring on the row container.
- **Header**: `bg-surface-raised-{theme}`, sortable columns have a chevron icon, sorted column has the chevron in `text-brand-primary`.
- **Empty state**: see component 12.

### 7.3 Rules

- Numbers in tables are right-aligned and use `font-variant-numeric: tabular-nums`.
- The first column is left-aligned, with a checkbox for selection.
- The last column is right-aligned (actions).
- Row height: 44 px (one line) or 60 px (two lines).
- Hovering a row reveals the actions menu (or it's always visible — pick one per table).
- Pagination is at the bottom, right-aligned.

### 7.4 Accessibility

- Uses `<table>` with proper `<thead>`, `<tbody>`, `<th>`, `<td>`.
- Sortable column headers are `<button>` inside the `<th>`, with `aria-sort="ascending"` / `"descending"` / `"none"`.
- Selection checkboxes have `<label>` associations.
- Pagination uses `<nav aria-label="Pagination">` with `<button>` for each page.
- A row can be the link target (use `<a>` wrapping the row contents, not `onclick` on `<tr>`).

### 7.5 Code — Plugin list

```html
<div class="rounded-lg border border-border-default-dark overflow-hidden">
  <table class="w-full text-sm">
    <thead class="bg-surface-raised-dark border-b border-border-default-dark">
      <tr>
        <th scope="col" class="w-10 p-3">
          <input type="checkbox" aria-label="Select all" class="..." />
        </th>
        <th scope="col" class="p-3 text-left font-medium text-text-secondary-dark">
          <button class="inline-flex items-center gap-1 hover:text-text-primary-dark">
            Name
            <!-- chevron -->
          </button>
        </th>
        <th scope="col" class="p-3 text-right font-medium text-text-secondary-dark">Version</th>
        <th scope="col" class="p-3 text-left font-medium text-text-secondary-dark">Maturity</th>
        <th scope="col" class="p-3 text-right font-medium text-text-secondary-dark">Devices</th>
        <th scope="col" class="w-10 p-3"></th>
      </tr>
    </thead>
    <tbody>
      <tr class="border-b border-border-subtle-dark hover:bg-surface-sunken-dark">
        <td class="p-3"><input type="checkbox" aria-label="Select tinkr-esp32" /></td>
        <td class="p-3 font-medium text-text-primary-dark font-mono">tinkr-esp32</td>
        <td class="p-3 text-right text-text-primary-dark tabular-nums">1.2.3</td>
        <td class="p-3"><span class="badge badge-success">stable</span></td>
        <td class="p-3 text-right text-text-primary-dark tabular-nums">2/3</td>
        <td class="p-3 text-right">
          <button aria-label="More actions" class="...">
            <!-- icon: more-horizontal -->
          </button>
        </td>
      </tr>
    </tbody>
  </table>
</div>

<nav aria-label="Pagination" class="flex items-center justify-end gap-1 p-3">
  <button class="..." aria-label="Previous page">‹</button>
  <button class="..." aria-current="page">1</button>
  <button class="...">2</button>
  <button class="...">3</button>
  <span class="text-text-tertiary-dark">…</span>
  <button class="...">12</button>
  <button class="..." aria-label="Next page">›</button>
</nav>
```

---

## 8. Tabs

Switch between related views of the same content. The default for the plugin detail page (Overview / Tools / Knowledge / Versions).

### 8.1 Variants

| Variant | Style | Usage |
|---|---|---|
| **Horizontal underline** | bottom 2 px border on the active tab | Default |
| **Vertical line** | left 2 px border on the active tab | Side panels, narrow surfaces |
| **Pill** | `bg-surface-raised-{theme}` background on the active tab | Settings pages, filter chips |

### 8.2 Anatomy (horizontal underline)

```
   Overview  Tools  Knowledge  Versions
   ─────────
   ↑ active
```

### 8.3 States

| State | Visual |
|---|---|
| **Default** | `text-text-secondary-{theme}` |
| **Hover** | `text-text-primary-{theme}` |
| **Active** | `text-text-primary-{theme}` + 2 px bottom border in `brand-primary` |
| **Focus** | ring around the tab |
| **Disabled** | `text-text-tertiary-{theme}`, no hover, `aria-disabled="true"` |

### 8.4 Accessibility

- Uses `role="tablist"` on the container.
- Each tab is a `<button>` with `role="tab"`, `aria-selected="true" | "false"`, `aria-controls="panel-id"`.
- The panel has `role="tabpanel"`, `aria-labelledby="tab-id"`, and `tabindex="0"` (so it can receive focus).
- Arrow keys move between tabs. `Home` / `End` jump to the first / last.
- The URL hash updates with the active tab (deep-linkable).

### 8.5 Code

```html
<div role="tablist" aria-label="Plugin detail" class="flex border-b border-border-default-dark">
  <button
    role="tab"
    id="tab-overview"
    aria-selected="true"
    aria-controls="panel-overview"
    class="px-4 py-2.5 text-sm font-medium
           text-text-primary-dark
           border-b-2 border-brand-primary
           hover:text-text-primary-dark
           focus-visible:outline-none focus-visible:ring-2
           focus-visible:ring-brand-primary focus-visible:ring-offset-2
           focus-visible:ring-offset-surface-bg">
    Overview
  </button>
  <button
    role="tab"
    id="tab-tools"
    aria-selected="false"
    aria-controls="panel-tools"
    class="px-4 py-2.5 text-sm font-medium
           text-text-secondary-dark
           border-b-2 border-transparent
           hover:text-text-primary-dark
           focus-visible:outline-none focus-visible:ring-2
           focus-visible:ring-brand-primary focus-visible:ring-offset-2
           focus-visible:ring-offset-surface-bg">
    Tools
  </button>
  <!-- ... -->
</div>

<div role="tabpanel" id="panel-overview" aria-labelledby="tab-overview" tabindex="0" class="p-6">
  <!-- panel content -->
</div>
```

---

## 9. Navigation / Sidebar

The persistent navigation in the Tauri shell and the docs site. Vertical, collapsible, with sections and badges.

### 9.1 Anatomy

```
   ┌──────────────────────────────┐
   │  ●  tinkr         [collapse] │  ← header (brand + collapse toggle)
   ├──────────────────────────────┤
   │  ▸ Project                   │  ← section
   │      Devices             2   │  ← item with badge
   │      Plugins             4   │
   │      Knowledge              │
   │                              │
   │  ▸ Marketplace               │  ← section
   │      Browse                  │
   │      Installed          ★ 3  │
   │                              │
   │  ▸ Help                      │
   │      Docs                    │
   │      KB                      │
   │      GitHub                  │
   ├──────────────────────────────┤
   │  [avatar]  Mira        ⌘K  │  ← footer (user + command palette)
   └──────────────────────────────┘
```

### 9.2 States (for items)

| State | Visual |
|---|---|
| **Default** | `text-text-secondary-{theme}` |
| **Hover** | `bg-surface-sunken-{theme}`, `text-text-primary-{theme}` |
| **Active** | `bg-brand-primary/10`, `text-brand-primary` |
| **Focus** | ring on the item |
| **Section header** | `text-caption`, `text-text-tertiary-{theme}`, uppercase |
| **Collapsed** | the sidebar becomes 48 px wide, only icons visible |

### 9.3 Rules

- The sidebar is 240 px expanded, 48 px collapsed.
- Sections are collapsible (state stored in localStorage).
- Badges are right-aligned, never truncated.
- The active item is highlighted. Only one active item at a time.
- Keyboard navigation: ↑/↓ moves between items, Enter activates, Space toggles sections.

### 9.4 Accessibility

- Uses `<nav aria-label="Primary">`.
- The sidebar is in the tab order; each item is a real link or button.
- The collapse toggle is a `<button>` with `aria-expanded` and `aria-controls`.
- The active item has `aria-current="page"`.
- Section headers are `<h2>` (or appropriate heading level), with the section items in a `<ul>`.

### 9.5 Code

```html
<nav aria-label="Primary" class="w-60 h-full
                            bg-surface-raised-dark
                            border-r border-border-default-dark
                            flex flex-col">
  <!-- header -->
  <div class="h-14 px-4 flex items-center justify-between
              border-b border-border-subtle-dark">
    <a href="/" class="flex items-center gap-2 font-semibold text-text-primary-dark">
      <!-- symbol mark -->
      <span class="w-5 h-5 rounded-sm bg-brand-primary flex items-center justify-center">
        <span class="w-2 h-2 rounded-full bg-brand-accent"></span>
      </span>
      tinkr
    </a>
    <button aria-label="Collapse sidebar"
            aria-expanded="true"
            class="w-7 h-7 rounded-md text-text-secondary-dark
                   hover:bg-surface-sunken-dark hover:text-text-primary-dark
                   focus-visible:outline-none focus-visible:ring-2
                   focus-visible:ring-brand-primary">
      <!-- icon: panel-left-close -->
      <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
        <rect width="18" height="18" x="3" y="3" rx="2"/>
        <path d="M9 3v18"/>
      </svg>
    </button>
  </div>

  <!-- sections -->
  <div class="flex-1 overflow-y-auto p-2">
    <div class="mb-2">
      <h2 class="px-2 py-1 text-caption font-medium uppercase tracking-wide text-text-tertiary-dark">
        Project
      </h2>
      <ul>
        <li>
          <a href="/devices" aria-current="page"
             class="flex items-center justify-between gap-2 px-2 py-1.5 rounded-md text-sm
                    bg-brand-primary/10 text-brand-primary font-medium
                    hover:bg-brand-primary/15
                    focus-visible:outline-none focus-visible:ring-2
                    focus-visible:ring-brand-primary">
            <span>Devices</span>
            <span class="text-xs tabular-nums text-text-secondary-dark">2</span>
          </a>
        </li>
        <li>
          <a href="/plugins"
             class="flex items-center justify-between gap-2 px-2 py-1.5 rounded-md text-sm
                    text-text-secondary-dark
                    hover:bg-surface-sunken-dark hover:text-text-primary-dark
                    focus-visible:outline-none focus-visible:ring-2
                    focus-visible:ring-brand-primary">
            <span>Plugins</span>
            <span class="text-xs tabular-nums text-text-secondary-dark">4</span>
          </a>
        </li>
      </ul>
    </div>
    <!-- ... more sections ... -->
  </div>

  <!-- footer -->
  <div class="h-14 px-3 flex items-center gap-2
              border-t border-border-subtle-dark">
    <div class="w-7 h-7 rounded-full bg-brand-secondary flex items-center justify-center
                text-xs font-semibold text-text-inverse-dark">M</div>
    <span class="text-sm text-text-primary-dark flex-1">Mira</span>
    <kbd class="text-caption font-mono text-text-tertiary-dark
                px-1.5 py-0.5 rounded border border-border-subtle-dark">⌘K</kbd>
  </div>
</nav>
```

---

## 10. Code block

A block of code with optional syntax highlighting, line numbers, a copy button, and a filename.

### 10.1 Anatomy

```
   ┌────────────────────────────────────────────────┐
   │  tinkr.toml                              [⧉]  │  ← header (filename + copy)
   ├────────────────────────────────────────────────┤
   │  1  [project]                                  │  ← line number gutter
   │  2  name = "kitchen-sensor"                    │
   │  3                                              │
   │  4  [plugins]                                  │
   │  5  tinkr-esp32 = "^1.2"                       │
   └────────────────────────────────────────────────┘
```

### 10.2 Variants

- **Plain** — no syntax highlighting. Used for logs, NDJSON output, raw text.
- **Highlighted** — syntax highlighted (Shiki or Prism). Used for code in docs.
- **Terminal** — monospace, no line numbers, with a prompt symbol. Used for CLI output previews in docs.

### 10.3 States

- **Default** — as shown.
- **Copy success** — the copy button briefly shows a check icon and "Copied" label (2 s).
- **Wrap** — long lines wrap (default off; toggle available).

### 10.4 Rules

- Always uses `bg-surface-sunken-{theme}` (the terminal/code surface).
- Font: JetBrains Mono, 13 px, line-height 1.54.
- Line numbers in `text-text-tertiary-{theme}`, right-aligned in a 4 ch gutter.
- The copy button is always present, top-right.
- The filename (if present) is in `text-text-secondary-{theme}`.
- Long lines are truncated by default, with a "wrap" toggle.

### 10.5 Accessibility

- The code block has `role="region"` and `aria-label="Code"`.
- The copy button is a real `<button>` with `aria-label="Copy code to clipboard"`.
- After copy, an `aria-live="polite"` region announces "Copied."
- Syntax highlighting is decorative; the code remains a single `<pre><code>` for screen readers.
- Keyboard: the block itself is not focusable, but the copy button is.

### 10.6 Code

```html
<div role="region" aria-label="Code"
     class="rounded-lg overflow-hidden
            bg-surface-sunken-dark
            border border-border-default-dark">
  <!-- header -->
  <div class="flex items-center justify-between px-4 py-2
              bg-surface-raised-dark border-b border-border-subtle-dark">
    <span class="text-xs font-mono text-text-secondary-dark">tinkr.toml</span>
    <button type="button" aria-label="Copy code to clipboard"
            class="text-text-secondary-dark hover:text-text-primary-dark
                   focus-visible:outline-none focus-visible:ring-2
                   focus-visible:ring-brand-primary rounded p-1">
      <!-- icon: copy -->
      <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <rect width="14" height="14" x="8" y="8" rx="2" ry="2"/>
        <path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>
      </svg>
    </button>
  </div>
  <!-- body -->
  <pre class="p-4 overflow-x-auto text-sm font-mono leading-snug"><code><span class="text-text-tertiary-dark select-none mr-4">1</span><span class="text-brand-secondary">[project]</span>
<span class="text-text-tertiary-dark select-none mr-4">2</span>name = <span class="text-status-success">"kitchen-sensor"</span>
<span class="text-text-tertiary-dark select-none mr-4">3</span>
<span class="text-text-tertiary-dark select-none mr-4">4</span><span class="text-brand-secondary">[plugins]</span>
<span class="text-text-tertiary-dark select-none mr-4">5</span>tinkr-esp32 = <span class="text-status-success">"^1.2"</span></code></pre>
</div>
```

The syntax highlighting colors are derived from the brand palette:

| Token | Color | Token |
|---|---|---|
| Keywords (`[section]`, `true`, `false`) | `brand-secondary` (`#A78BFA`) | violet |
| Strings | `status-success` (`#22C55E`) | green |
| Numbers | `brand-accent` (`#FB923C`) | amber |
| Comments | `text-tertiary-{theme}` | grey |
| Functions / methods | `brand-primary` (`#5EEAD4`) | cyan |
| Punctuation | `text-secondary-{theme}` | grey |
| Variables / identifiers | `text-primary-{theme}` | white/black |

This set maps to the standard 6-color dev-tool highlighting (keyword / string / number / comment / function / variable) and stays inside the brand palette. The palette works in light and dark mode without changes.

---

## 11. Status indicator

A binary state dot for hardware devices. Online / offline / syncing / error.

### 11.1 Anatomy

```
   ●  esp32s3-left           online
   ◌  rp2040-pico            offline
   ◐  esp32s3-spare          syncing
   ⨯  esp32c3-...            error
```

The dot is a 8 px filled circle (or 8 px ring for offline, 8 px half-filled for syncing, 8 px X for error). The label is to the right, sentence case, 1–3 words.

### 11.2 Variants

| State | Visual | Color | Animation |
|---|---|---|---|
| **Online / detected** | filled dot | `status-success` | none (or 1 Hz tinkr if "live") |
| **Offline** | ring (outline) | `text-tertiary-{theme}` | none |
| **Syncing / flashing** | half-filled dot | `status-info` | rotates at 2 s/rev |
| **Error** | X (cross) | `status-error` | none |
| **Idle** | filled dot, dim | `text-tertiary-{theme}` | none |

### 11.3 Rules

- The dot is 8 px in tables, 10 px in cards, 12 px in hero surfaces.
- The label is always present in tables and cards. The dot alone is allowed only in icon-only contexts.
- Color is never the only indicator — the shape (filled, ring, half, X) carries the state too.
- The "syncing" animation is suppressed under reduced motion.

### 11.4 Accessibility

- The status indicator has a meaningful accessible name via `aria-label` or visible text.
- The "syncing" state has `aria-live="polite"` so screen readers announce progress.
- The dot is not interactive (no role, no tabindex). The surrounding row is.

### 11.5 Code — Device status

```html
<!-- Online -->
<span class="inline-flex items-center gap-2">
  <span class="relative flex w-2.5 h-2.5" aria-hidden="true">
    <span class="absolute inset-0 rounded-full bg-status-success"></span>
  </span>
  <span class="text-sm text-text-primary-dark">esp32s3-left</span>
  <span class="text-xs text-text-tertiary-dark">online</span>
</span>

<!-- Syncing (with animation) -->
<span class="inline-flex items-center gap-2" aria-live="polite">
  <span class="relative flex w-2.5 h-2.5" aria-hidden="true">
    <span class="absolute inset-0 rounded-full bg-status-info animate-spin"
          style="clip-path: polygon(50% 50%, 100% 0, 100% 100%); animation-duration: 2s;"></span>
  </span>
  <span class="text-sm text-text-primary-dark">esp32s3-spare</span>
  <span class="text-xs text-text-tertiary-dark">flashing…</span>
</span>

<!-- Error -->
<span class="inline-flex items-center gap-2">
  <span class="relative flex w-2.5 h-2.5" aria-hidden="true">
    <!-- icon: x, sized to match the dot -->
    <svg class="w-2.5 h-2.5 text-status-error" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" aria-hidden="true">
      <path d="M18 6 6 18"/><path d="m6 6 12 12"/>
    </svg>
  </span>
  <span class="text-sm text-text-primary-dark">esp32c3-broken</span>
  <span class="text-xs text-status-error">error: port busy</span>
</span>
```

---

## 12. Empty state

The screen shown when there is no content yet. First-time use, no devices, no plugins, no results.

### 12.1 Anatomy

```
   ┌────────────────────────────────────────┐
   │                                        │
   │              [icon]                    │  ← illustration (24x24, brand-primary)
   │                                        │
   │         No devices connected           │  ← title (h3, sentence case)
   │                                        │
   │   Plug in an ESP32, RP2040, or other   │  ← description (body, secondary)
   │   supported board. Tinkr will detect   │
   │   it on the next scan.                 │
   │                                        │
   │          [Scan now]                    │  ← primary action
   │          Learn more →                  │  ← secondary action
   │                                        │
   └────────────────────────────────────────┘
```

### 12.2 Rules

- Centered horizontally and vertically in the available space.
- Icon: 48 px, `text-brand-primary` or `text-text-tertiary-{theme}` (when the empty state is a "no results" — not an action prompt).
- Title: 1 line, sentence case, the user-facing situation.
- Description: 1–3 lines, the next step in plain language.
- Primary action: the single most likely next step. Only one.
- Secondary action: a text link, never a button.
- For "no results" search states, the secondary action is "Clear search" or "Reset filters."

### 12.3 Accessibility

- The empty state container is a `<div>` with no role (or `role="status"` if it's a post-action confirmation).
- The icon has `aria-hidden="true"`.
- The primary action is the first focusable element when the page loads with an empty state.

### 12.4 Code — No devices

```html
<div class="flex flex-col items-center justify-center text-center py-16 px-4">
  <!-- icon: device-plug, 48px -->
  <div class="w-12 h-12 rounded-full
              bg-surface-raised-dark
              flex items-center justify-center
              text-brand-primary mb-4">
    <svg class="w-7 h-7" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <path d="M12 22v-5"/>
      <path d="M9 7V2"/>
      <path d="M15 7V2"/>
      <path d="M6 13V8h12v5a4 4 0 0 1-4 4h-4a4 4 0 0 1-4-4Z"/>
    </svg>
  </div>

  <h3 class="text-lg font-semibold text-text-primary-dark">
    No devices connected
  </h3>
  <p class="mt-1 text-sm text-text-secondary-dark max-w-sm">
    Plug in an ESP32, RP2040, or other supported board. Tinkr will detect it on the next scan.
  </p>

  <div class="mt-6 flex flex-col items-center gap-2">
    <button
      type="button"
      autofocus
      class="h-9 px-4 rounded-md text-sm font-medium
             bg-brand-accent text-text-inverse-dark
             hover:bg-brand-accent-dim
             focus-visible:outline-none focus-visible:ring-2
             focus-visible:ring-brand-primary focus-visible:ring-offset-2
             focus-visible:ring-offset-surface-bg">
      Scan now
    </button>
    <a href="/docs/devices"
       class="text-sm text-text-secondary-dark hover:text-text-primary-dark
              focus-visible:outline-none focus-visible:ring-2
              focus-visible:ring-brand-primary rounded">
      Learn more →
    </a>
  </div>
</div>
```

---

## 13. What ships in v1 vs. later

| Component | v1 (CLI + web docs) | v1.5 (Tauri shell) | v2.0 (marketplace) |
|---|---|---|---|
| Button | ✓ | ✓ | ✓ |
| Input | ✓ | ✓ | ✓ |
| Card | ✓ (web) | ✓ | ✓ |
| Modal | ✓ (web) | ✓ | ✓ |
| Toast | ✓ (CLI progress → toast in Tauri) | ✓ | ✓ |
| Badge | ✓ | ✓ | ✓ |
| Table | ✓ (web) | ✓ | ✓ |
| Tabs | ✓ (web) | ✓ | ✓ |
| Navigation / Sidebar | ✓ (docs site) | ✓ (Tauri) | ✓ |
| Code block | ✓ (web, KB, docs) | ✓ (Tauri) | ✓ |
| Status indicator | ✓ (CLI) | ✓ | ✓ |
| Empty state | ✓ (web) | ✓ | ✓ |

All 12 ship in v1 across at least one surface. Tauri adds the desktop-specific applications (toast in the window, sidebar in the shell, status indicator in the device list).

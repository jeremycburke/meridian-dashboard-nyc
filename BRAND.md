# BRAND.md

The dashboard's design rules (decision D10).
They come from `brand-guidelines.md` in the `meridianxyz_website` repo, extracted from www.meridianxyz.com on 2026-10-22.
The live site is the source of truth; if it changes, this file follows.

The tokens at the end of this file are copied into `web/src/tokens.css` in S041.
Components read tokens only; a hex value in a component is a defect.

## Principles

1. **Paper and ink.** A warm off-white ground, deep teal-black type, one muted sage accent. Color is scarce and earns its place.
2. **Hairlines, not shadows.** Structure comes from 1px rules and bordered boxes. No shadows.
3. **Mono as the engineering signal.** Labels, indices, captions and chrome are small, uppercase, letter-spaced Geist Mono. Headings and body are Geist.
4. **Numbers over adjectives.** Sections are indexed `01`, `02`, `03`. Proof is a figure with a caption, not an icon grid.
5. **Drawn, not photographed.** Graphics are diagrammatic: grid paper, axes, crosshairs, hex fields.

Not the brand: rounded cards with drop shadows, decorative icon sets, stock "smart city" imagery, gradients, em dashes, marketing adjectives, invented metrics.

## Type

| Role | Family | Weights |
|---|---|---|
| Headings and body | Geist | 300 to 700 |
| Labels, indices, captions, counters | Geist Mono | 400 to 600 |

Both are self-hosted; the dashboard loads no font from an outside host.
Instrument Serif is not used in the dashboard.

| Token | Size / line-height (px) | Weight | Tracking | Use |
|---|---|---|---|---|
| `display-stat` | 36 / 1 (28 on small screens) | 600 | -.03em | Lead number in a stat tile |
| `title-page` | 28 to 32 / 1.2 | 500 | -.025em | Page h1 |
| `title-section` | 22 to 24 / 1.2 | 500 | -.025em | h2, card group heading |
| `title-card` | 19 / 1.3 | 500 | -.025em | h3 in a card |
| `body` | 16 / 1.6 | 400 | 0 | Prose, forms |
| `body-dense` | 14 / 1.5 | 400 | 0 | Tables, lists, descriptions |
| `micro` | 12 / 1.6 | 400 | 0 | Helper text, footers |
| `label` (mono) | 12 / 1.6 | 400 to 500 | .08 to .12em, uppercase | Eyebrows, column headers, tile labels |
| `index` (mono) | 11 to 12 | 400 | 0 | `01` indices, counters `1 / 9` |
| `caption` (mono) | 11 | 400 | .06em, uppercase | Chart captions, legend labels |

Kickers read `02 / Portfolio`: a two-digit index, a slash, the section.
Indices are always two digits, in mono, in the accent color.

## Color

The full token sheet is at the end. The rules that matter most:

- **The accent swaps with the theme.** Sage `#556e65` is the accent in light mode; gold `#d2b581` is the accent in dark mode. Never both at once.
- **Gold is never text on light.** On paper it reads 2.08 : 1. Use it for marks and fills only.
- **Status colors carry status only:** `--ok-*`, `--warn-*`, `--err-*`. Screen results (pass, fail) use them; decoration never does.
- **Focus is always visible:** a 2px `#ac793b` ring.

## Surfaces

Every card, panel and table has a 1px `--line` border.
Elevation is a small tonal step, never a shadow.

| Token | Light | Dark | Use |
|---|---|---|---|
| `--bg` | `#f1f2ec` | `#182d33` | App canvas |
| `--bg-sunken` | `#e4e8df` | `#142a30` | Sidebar, table header rows, wells |
| `--bg-raised` | `#ffffff` | `#203a40` | Cards, inputs, popovers |
| `--bg-hover` | `#e8e9df` | `#28484d` | Row and button hover |
| `--bg-selected` | `#dfe5dc` | `#396366` | Selected row, active nav item |

Radius is 0 on everything; 2px at most on tiny tags.

## Spacing

A 4px rhythm: 4, 8, 12, 16, 20, 24, 32, 44, 64, 88.
Card padding 24; grid gaps 16 to 24; gutters 24.

## The app shell

- **Top bar:** 64px, `--bg` at 95% opacity with a 14px blur, a 1px `--line` bottom border. Wordmark on the left, a mono context label in the middle (`Meridian / NYC`), account and theme toggle on the right.
- **Sidebar:** 240px on `--bg-sunken` with a 1px `--line` right border. Items at 14px, the active one on `--bg-selected`. It collapses under 760px.
- **Page head:** a kicker with its index above the h1, an optional lede in `--fg-muted`, a 1px rule 24px below.
- **Tables:** a `--bg-sunken` header row with mono column labels; 14px rows with 12px vertical padding and a 1px `--line` between; numbers right-aligned in Geist Mono with tabular figures. No zebra stripes.
- **Stat tile:** a bordered panel; a mono label on top; the number in `display-stat`; a one-line mono caption below.
- **Buttons:** primary is an ink block with paper text, 1px border, padding 16px 22px, 14px text. A text link has a 1px underline in the current color.
- **Inputs:** 1px `#8e9b90` border, padding 12px 13px, radius 0, the label 7px above in `--fg-muted`.
- **Empty states:** a grid-paper well, one `title-card` line, one sentence, one text link.

## Data visualization

**Sequential ramp**, deep teal to gold, six steps:

```
#28484d  #396366  #658b80  #a4b49a  #d1b578  #e5c18b
```

- Filled areas (choropleths, heatmaps, stacked bars) may use all six steps.
- A single mark (a line, a dot, a lone bar) takes its color from the half of the ramp that clears 3 : 1 on the current ground, or carries a 1px stroke in `--fg`.
- The low end disappears on dark; the high end disappears on paper.
- Legends are a 5px ramp bar labeled `Low → High`.

**Categorical set** (proposed by the guidelines; validate any series beyond three against both grounds):

| On light | On dark |
|---|---|
| `#28484d` deep teal | `#d1b578` gold |
| `#658b80` sage | `#a4b49a` pale sage |
| `#ac793b` amber | `#658b80` sage |
| `#5b6868` slate | `#9fd3a8` mint |
| `#9d6157` clay | `#e3a79b` clay |

**Charts (Plotly).**
- The plot area sits on grid paper at 24px; axes and gridlines in `--line`; tick labels in mono `caption`, in `--fg-muted`.
- At most one gold highlight per chart.
- Figures made in Python carry data and layout, never colors. The dashboard applies one brand template, built from `web/src/tokens.ts`, so light and dark both work.

**Maps (deck.gl over MapLibre).**
- Lot and footprint fills come from the sequential ramp; the selection stroke is gold.
- Map chrome: a paper top bar with mono labels, a square ink action button, the legend in a bordered paper card.
- Every layer's colors come from `web/src/tokens.ts`.
- Every map that shows walking distances credits "© OpenStreetMap contributors".

## Motion

- Color, border and background transitions: 200ms.
- Button hover: the fill changes and the button rises 2px.
- Map layer change: a 700ms fill transition.
- Nothing animates on its own: no parallax, no carousels, no shimmering skeletons.
- With reduced motion set, every animation and transition is off.

## Voice

These rules apply to labels, empty states, errors and the docs page.

- Direct, precise, concrete. Prefer a number to an adjective.
- No em dashes. Use colons, periods or commas.
- Headings and buttons in sentence case. Labels are written in sentence case and uppercased by CSS.
- Messages address the user as "you" and say what happened in a full sentence with a period.
- Never invent a client, metric or quote. Demo or synthetic data is labeled as such. Features in progress are labeled `under development`.
- Describe associations as associations, never as causes.

## Open items for S041 (⚠)

From the guidelines' own open decisions:

1. **Wordmark casing:** `MERIDIAN XYZ` (site header) or `Meridian XYZ` (product banner). The guidelines lean to title case.
2. **Corners:** square everywhere, as the guidelines recommend, or the rounded cards of an earlier demo.
3. **Navigation icons:** text-only nav with mono indices (`01 Map`), or one thin-stroke icon set used only in the sidebar.

## Tokens

Copy this block into `web/src/tokens.css` in S041.
The `[data-theme="dark"]` block repeats the dark values so the theme toggle can override the system setting.

```css
:root {
  /* Fonts (self-hosted) */
  --font-sans: "Geist", sans-serif;
  --font-mono: "Geist Mono", monospace;

  /* Brand constants */
  --paper: #f1f2ec;
  --ink: #203237;
  --dark: #182d33;
  --sage: #556e65;
  --gold: #c3a575;
  --gold-deep: #6a7362;
  --focus: #ac793b;

  /* Light theme (default) */
  --bg: #f1f2ec;
  --bg-sunken: #e4e8df;
  --bg-raised: #ffffff;
  --bg-hover: #e8e9df;
  --bg-selected: #dfe5dc;
  --fg: #203237;
  --fg-muted: #5b6868;
  --fg-label: #556e65;
  --line: #cbd0c8;
  --line-strong: #8e9b90;
  --line-ink: #203237;
  --accent: #556e65;
  --accent-text: #556e65;
  --accent-fill: #c3a575;        /* marks and fills only; never text on light */
  --btn-bg: #203237;
  --btn-bg-hover: #35554e;
  --btn-fg: #f1f2ec;
  --grid-line: rgb(82 110 100 / 6%);
  --ok-fg: #1d5a2d;   --ok-bg: #d8ebd9;   --ok-line: #78927f;
  --warn-fg: #8a5a1f; --warn-bg: #efe3cf; --warn-line: #ac793b;
  --err-fg: #743e36;  --err-bg: #eedfd9;  --err-line: #9d6157;
  --overlay: rgb(13 28 33 / 72%);

  /* Sequential ramp, deep teal to gold */
  --viz-1: #28484d; --viz-2: #396366; --viz-3: #658b80;
  --viz-4: #a4b49a; --viz-5: #d1b578; --viz-6: #e5c18b;
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #182d33;
    --bg-sunken: #142a30;
    --bg-raised: #203a40;
    --bg-hover: #28484d;
    --bg-selected: #396366;
    --fg: #f1f2ec;
    --fg-muted: #b8c3bf;
    --fg-label: #b8c8bd;
    --line: #42565a;
    --line-strong: #758a83;
    --line-ink: #f1f2ec;
    --accent: #d2b581;
    --accent-text: #ead6ac;
    --accent-fill: #d2b581;
    --btn-bg: #e8e9df;
    --btn-bg-hover: #d2dbcc;
    --btn-fg: #182d33;
    --grid-line: rgb(255 255 255 / 6.7%);
    --ok-fg: #9fd3a8;   --ok-bg: rgb(159 211 168 / 12%);  --ok-line: rgb(159 211 168 / 40%);
    --warn-fg: #e2c894; --warn-bg: rgb(226 200 148 / 12%); --warn-line: rgb(226 200 148 / 40%);
    --err-fg: #e3a79b;  --err-bg: rgb(227 167 155 / 12%);  --err-line: rgb(227 167 155 / 40%);
    --overlay: rgb(12 20 22 / 94%);
  }
}

:root[data-theme="dark"] {
  /* The same values as the dark block above; keep the two in sync. */
}

body { background: var(--bg); color: var(--fg); font: 16px/1.6 var(--font-sans); -webkit-font-smoothing: antialiased; }
:focus-visible { outline: 2px solid var(--focus); outline-offset: 5px; }
input:focus-visible, textarea:focus-visible, select:focus-visible { outline-offset: 2px; }
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation: none !important; transition: none !important; } }
```

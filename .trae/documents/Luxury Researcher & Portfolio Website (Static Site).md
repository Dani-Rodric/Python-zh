## Objectives & Style
- Deliver a minimalist, luxury aesthetic with intentional whitespace, premium typography, and subdued motion.
- Palette: `#000000`, `#FFFFFF`, `#F5F5F5`, `#333333` with accents `#D4AF37` (gold) and `#001F3F` (navy).
- Typography: Headings in elegant serif (Playfair Display or similar), body in clean sans-serif (Inter/Montserrat). Titles uppercase, 48–72px; body 16–18px; line-height 1.6–1.8.
- Imagery: High‑res, desaturated/monochrome. Subtle parallax, fade‑in on reveal, refined hover (scale 1.02, slight shadow).

## Information Architecture
- Homepage (core hub) with curated sections:
  - Hero: Full‑viewport with centered title, subtitle, CTA.
  - Featured Insights: 3–4 highlighted articles/albums (imitates “Daily Selection”).
  - Latest Research: Recent articles list/grid with “Load More”.
  - Popular Albums: Albums ordered by views with “Load More”.
  - Footer teaser: newsletter/social.
- Sections: About, Research (archive), Albums (gallery), Contact.
- Single‑page + sub‑page hybrid: archives live as sections; single article/album opens in modal; optional dedicated sub‑pages can be added later.

## Data & Content Model
- `data/articles.json`: `{ id, slug, title, abstract, date, tags[], image, views, featured }`.
- `data/albums.json`: `{ id, slug, title, description, count, cover, images[], date, medium, views, featured }`.
- Content fed into grids with client‑side pagination (AJAX fetch, IntersectionObserver for infinite scroll or button‑based “Load More”).

## UI Layout & Components
- Grid system: 12‑column CSS Grid; content containers at 80–90% width.
- Components:
  - Navbar: fixed, logo left (initials in gold), centered menu, search icon right; fades in on scroll‑up; gold underline on hover.
  - Hero: full‑screen background image (artistic/abstract), overlay text and gold‑border CTA.
  - Cards: article/album cards with image, title (serif uppercase), meta, excerpt; hover shadow/glow.
  - Lightbox Modal: full‑screen album viewer with swipe/keyboard navigation, zoom, captions.
  - Footer: minimalist nav + copyright + social.

## Animations & Interactions
- Reveal on scroll using IntersectionObserver (opacity/translateY).
- Parallax on hero/backgrounds (translate based on scrollY, clamped for performance).
- Hover: subtle scale and shadow; button ripple kept restrained.
- “Load More” uses smooth appended grids with spinner; preserves scroll position.

## Responsiveness & Grid
- Desktop: 12‑col; Featured cards span 3–4 cols; archives 3‑col.
- Tablet: 2‑col; Mobile: 1‑col; rhythm preserved via consistent spacing scale.
- Media queries adjust font sizes and spacing proportionally.

## Accessibility & SEO
- Alt text for all images; ARIA for modal, nav, buttons; keyboard‑accessible controls.
- Contrast > 4.5:1; focus rings visible.
- SEO: meta tags, Open Graph/Twitter cards; JSON‑LD for Article; sitemap and robots.

## Performance
- Lazy loading (`loading="lazy"`), responsive `srcset` images.
- Preconnect fonts; `font-display: swap`; compress images (WebP/AVIF) and serve optimized sizes.
- Defer non‑critical JS; measure Lighthouse; target <2s LCP.

## Implementation Steps
1. Update palette and typography tokens, introduce `--gold`/`--navy`, uppercase titles, spacing scale.
2. Expand homepage sections: add Featured Insights, Latest Research, Popular Albums with load‑more.
3. Implement lightbox modal and album carousel; article modal with table of contents when long.
4. Add parallax and reveal animations (IntersectionObserver).
5. Add accessibility roles/labels, keyboard navigation.
6. Add SEO meta + JSON‑LD injection; lazy image handling.
7. Wire up data fetch from `data/*.json`, sorting (date/views), client pagination.

## Files & Edits (current structure)
- `site/index.html`: add new sections and navbar/search; enhance hero.
  - Hero edits near `site/index.html:31–41`.
  - Navbar/menu edits near `site/index.html:17–24` and actions at `site/index.html:25–28`.
  - Insert Featured/Latest/Popular sections below `site/index.html:41–64`.
- `site/styles.css`: add palette tokens and luxury styling.
  - Color/typography variables at `site/styles.css:1–8` (extend with `--gold`, `--navy`).
  - Hero, cards, grid, modal, animations styles appended after `site/styles.css:57`.
- `site/script.js`: data loader, reveal/scroll, modal, pagination.
  - Current section toggling at `site/script.js:1–4`; extend with data fetch and UI rendering.
- Add `site/data/articles.json` and `site/data/albums.json` for content.

## Validation
- Run local preview, verify layout, interactions, and performance.
- Accessibility check (keyboard, screen reader landmarks).
- SEO tags and JSON‑LD validate via Rich Results test.

## Next Extensions
- Optional dedicated sub‑pages: `site/article.html` and `site/album.html` templates rendered by `?id=...`.
- Search and filter UI for Research archive (topic/year); serverless index if needed.
- CDN integration for static assets (images/fonts) and pre‑optimized pipelines.

## Notes on Curation Flow
- Emulate clean vertical flow from curated sections like “Daily Selection”, “24‑Hour Most Popular”, and “24‑Hour Latest” with spacious grids and a restrained “Load More”, tailored to research articles and albums for an atelier‑style experience.
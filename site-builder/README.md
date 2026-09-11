# site-builder

Generates a small, launch-ready static site for a local service business
from a JSON description: a home page (hero, services & pricing, gallery,
reviews, contact, and a client-side booking flow), plus the supporting
files a real launch needs.

No backend, no login, no build step, no npm dependencies, no network
access at generation time (except the images you point it at). Only data
present in the input JSON is ever rendered — nothing is invented. Where a
business has no formal service list, the site shows their real call to
action (call, DM, email) instead of a fabricated pricing/booking flow.

## Design system

- **Type**: Playfair Display (editorial serif, headings) + Inter (body),
  loaded from Google Fonts with a system-font fallback if that request is
  blocked or offline. This pairing and the layout patterns below
  (bento-grid gallery, an editorial pull-quote for the top review, oversized
  hero type) come from querying the `ui-ux-pro-max` design-data skill
  (`--design-system`, `--domain style/typography/landing/gsap`) rather than
  being guessed — see that skill's own data for the full rule set.
- **Color**: one brand accent color on a near-black/white base (not a
  wash of tinted backgrounds everywhere) — closer to an agency/editorial
  site than a generic "beige template."
- **Motion**: a hand-rolled scroll-reveal (no GSAP/Framer Motion — both
  need a bundler or React, which would break the "one file, no install"
  point of this tool). Its timing (duration, easing, stagger cap) is
  ported from that skill's GSAP "Scroll Reveal — Standard" preset. Content
  is `opacity: 1` by default in the CSS — the script only *arms* the
  hidden-until-in-view behavior, and skips that entirely under
  `prefers-reduced-motion` — so no-JS clients, crawlers, and
  reduced-motion users always see full content immediately, never
  something stuck invisible.
- Buttons and booking choices have real press/hover feedback
  (`active:scale(0.97)`, hover lift + shadow) instead of static flat
  rectangles.

## Usage

```sh
node generate-site.js --input business.json --outdir dist/
```

- `--input, -i` — path to a JSON file describing the business (required)
- `--outdir, -o` — directory to write the generated site into (defaults to
  `./dist/<slugified-business-name>/`)

Try the two bundled examples:

```sh
node generate-site.js --input examples/hair-salon.json --outdir examples/output/hair-salon
node generate-site.js --input examples/afrodite/afrodite.json --outdir examples/output/afrodite
```

The `afrodite` example is a real one, built from a screenshot of a real
Instagram profile (`examples/afrodite/afrodite.json` only contains what was
visible in that screenshot — no services, prices, or reviews were given, so
the generator correctly skips the booking wizard and shows their actual
stated way to book: DM on Instagram).

## What gets generated

Each run writes a small static site into `--outdir`:

| File | Purpose |
|---|---|
| `index.html` | The site itself |
| `privacy.html`, `terms.html` | Legal page templates (clearly marked as templates — see below) |
| `404.html` | Branded not-found page |
| `robots.txt`, `sitemap.xml` | Only generated if `business.siteUrl` is set |
| `_headers` | Netlify/Cloudflare Pages security headers file |

Run the generator and read the printed warnings — it tells you about
anything it skipped or auto-corrected (invalid email/phone, oversized
images, missing alt text, low-contrast colors it had to darken, etc.)
rather than silently producing a broken or inaccessible page.

## Input schema

Every section is optional; it only renders if the matching data is
present.

```jsonc
{
  "business": {
    "name": "Main Street Hair Co.",   // required
    "logoText": "MAIN STREET HAIR CO.",
    "logoInitials": "MS",              // used for the auto-generated favicon; defaults to initials of name
    "tagline": "Small town salon with a big heart",
    "bio": "...",                      // renders an "About" section
    "metaDescription": "...",          // for <meta name="description">; falls back to bio/tagline
    "siteUrl": "https://example.com",  // enables canonical link, OG:url, robots.txt, sitemap.xml
    "socialImage": "https://example.com/social.jpg", // absolute URL only — needed for link-preview images
    "primaryColor": "#8a6240",         // buttons/accents — auto-darkened if it fails contrast on white
    "accentColor": "#f6efe4",          // section backgrounds; derived from primaryColor if omitted
    "inkColor": "#20201d",             // body text color — auto-darkened if it fails contrast
    "contact": {
      "address": "123 Main St, Anytown, USA",
      "phone": "+15551234567",         // validated; dropped with a warning if malformed
      "email": "hello@example.com",    // validated; dropped with a warning if malformed
      "instagram": "@handle",
      "hours": "Tue–Sat, 9am–6pm"
    },
    "booking": {
      "availableDays": ["Tue","Wed","Thu","Fri","Sat"],
      "startHour": 9, "endHour": 18, "slotMinutes": 60, "daysAhead": 10
    }
  },
  "hero": { "headline": "...", "subheadline": "...", "image": "photos/hero.jpg" },
  "services": [
    { "category": "Cuts", "name": "Women's Haircut", "price": "From $45", "description": "..." }
  ],
  "gallery": [ { "src": "photos/1.jpg", "alt": "Required — describe the photo", "tag": "Before" } ],
  "reviews": [ { "rating": 5, "quote": "...", "author": "Balayage Client" } ],
  "analytics": { "provider": "plausible", "domain": "example.com" }
  // or: { "provider": "ga4", "id": "G-XXXXXXX" }
}
```

- Local image paths are inlined as base64 `data:` URIs so `index.html`
  stays self-contained; `https://` URLs are left as direct links. Local
  images over 400KB get a compress-this-first warning.
- If neither `contact.phone` nor `contact.email` is set, the booking
  step's final button just shows a summary to call in with; if `services`
  is empty entirely, there's no booking wizard at all — the site shows a
  Call/DM/Email button using whatever real contact info exists instead.
- `analytics` is optional and off by default (no third-party requests, no
  cookies). Plausible is cookieless, so no consent banner is added. GA4
  uses cookies, so enabling it adds an accept/decline banner, and the GA
  script itself only loads after the visitor accepts.

## Accessibility (WCAG-minded)

- Semantic landmarks (`header`/`main`/`section`/`footer`), a skip-to-content
  link, and one `<h1>` per page with a proper heading hierarchy under it.
- Every content section is labelled (`aria-labelledby`) for screen readers.
- Brand colors are checked against WCAG AA (4.5:1) and automatically
  darkened if they'd fail — you'll see this as a warning, not a silent
  guess.
- The booking widget is fully keyboard-operable, announces step changes to
  screen readers via a live region, and its form fields have real
  `<label for>` associations, inline validation errors tied via
  `aria-describedby`, and `aria-invalid` state.
- Visible focus outlines everywhere (`:focus-visible`), 44px minimum touch
  targets, decorative icons marked `aria-hidden`, and all motion is
  disabled under `prefers-reduced-motion`.
- `gallery[].alt` is required in spirit — omitting it prints a warning and
  falls back to a generic (not truly descriptive) caption.

## Security

- **CSP via hashing, not `unsafe-inline`.** The page's inline `<style>`
  and `<script>` are hashed (SHA-256) at generation time and the exact
  hash is put in the `Content-Security-Policy` meta tag — so inline code
  runs, but nothing else does. There are no inline `style="..."`
  attributes or inline event handlers anywhere in the output. The only
  extra hosts allowed are `fonts.googleapis.com`/`fonts.gstatic.com`
  (the display font) and, only if you turn on `analytics`, that one
  provider's domain — nothing else can load.
- Every phone number, email, and Instagram handle is validated before
  being written into a `tel:`/`mailto:`/`https://instagram.com/...` link;
  anything malformed is dropped (with a warning) instead of emitted.
- The booking form has real client-side validation (can't submit
  empty/garbage name or contact info) and a honeypot field to silently
  drop naive bot submissions.
- `_headers` (Netlify/Cloudflare Pages format) sets
  `Strict-Transport-Security`, `X-Content-Type-Options`, `X-Frame-Options`,
  `Referrer-Policy`, and a locked-down `Permissions-Policy`. A `<meta>` CSP
  can't set these — if you're hosting elsewhere, configure your host to
  send equivalent headers.
- All user-supplied text (business name, bio, reviews, etc.) is HTML-escaped
  everywhere it's rendered.

## What this deliberately does not do

- **It does not scrape.** There's no Instagram/Facebook/Google scraping
  here, and there won't be — all three explicitly prohibit automated
  scraping in their terms of service, it risks the scraping account(s)
  getting banned, and it's the ingredient that turns "make a nice site for
  a business you found" into mass unsolicited outreach. Feed it data you
  already have permission to use (a screenshot you took, info the
  business gave you). If you want to *legitimately* automate finding
  candidate businesses, the compliant option is the Google Places API,
  which returns public business listings (name/address/phone/website
  status) through an official, ToS-compliant endpoint — ask if you want
  that built; it needs your own API key.
- **It does not send anything.** The booking flow opens the customer's own
  mail/SMS app; nothing is transmitted to a server anywhere.
- **The legal pages are templates, not legal advice.** `privacy.html` and
  `terms.html` say so at the top. Have someone qualified review them
  before a business relies on them.
- **It doesn't measure real-world page speed or fix broken links.** Those
  need the page actually deployed. What it does do: no external requests
  by default, lazy-loaded images, and a warning for any local image over
  400KB.

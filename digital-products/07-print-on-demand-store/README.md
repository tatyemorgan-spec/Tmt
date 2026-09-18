# Print-on-Demand Merch Store — "Small Business Big Energy"

A real, working storefront landing page plus 3 print-ready apparel
designs, for a print-on-demand (POD) merch business. This is the
category shown via the MrBeast merch store example in the reference
video — except that store runs on Shopify + a fulfillment partner with
years of infrastructure behind it. This package gives you the
front-end and the artwork; the honest missing piece (below) is the
part that genuinely requires your own accounts.

## What's in the box

- `index.html` — a complete, tested storefront landing page: hero,
  3-product grid, "how it works" explainer, and an email capture form
  (wired to demo behavior — swap in a real email tool before launch).
- `designs/01-small-business-big-energy.svg`,
  `02-built-this-myself.svg`, `03-est-badge.svg` — three print-ready,
  single/two-color typographic tee designs, plus a rendered PNG
  preview of each on a shirt-colored background. Vector SVGs scale to
  any print resolution.

## What genuinely needs your own accounts (can't be automated here)

Real checkout, payment processing, and physical fulfillment require
your own store on a platform. This isn't a gap in the build — it's how
POD works everywhere; nobody generates a live Shopify store from
outside Shopify. The real setup, once you're ready to actually sell:

1. Create a free [Printful](https://www.printful.com) or
   [Printify](https://www.printify.com) account (this is your
   fulfillment partner — they print and ship each order, you never
   touch inventory).
2. Upload the SVGs from `designs/` (or export them as PNG at 300dpi
   for print — open the SVG in a browser and print/export at a large
   size, or use any vector editor).
3. Printful/Printify auto-generates real product photos (mockups) on
   actual shirts — this replaces the placeholder color-block cards in
   `index.html`.
4. Connect Printful/Printify to a free Shopify trial, or to Etsy
   (Printify has a direct Etsy integration) — this gives you real
   checkout.
5. Replace this page's product images and "Shop the drop" link with
   your live store URL, and connect the email form to a real tool
   (Mailchimp free tier, Klaviyo, ConvertKit) instead of the current
   demo JS.

## Selling it as a product (vs. running it as a store)

Two ways to monetize this package:

- **Run it** — actually launch the merch store (follow the setup
  above). Margin is typically $8–$15/shirt after Printful's base cost.
- **Sell the starter kit** — package `index.html` + `designs/` as a
  "POD store starter kit" digital product ($15–$25 on Gumroad) for
  other people who want to skip the design/landing-page work and go
  straight to connecting Printful. See `marketing/` for listing copy.

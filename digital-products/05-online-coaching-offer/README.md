# Online Coaching Offer — "Momentum Coaching"

A real, working coaching sales page and booking flow — generated with
this repo's own `site-builder` tool. This is the strongest proof this
repo can walk its own talk: the same generator built for local service
businesses (salons, etc.) works just as well for a 1:1/group coaching
offer, because coaching is structurally the same thing — services with
prices, a booking flow, and social proof.

## What's in the box

- `coaching-offer.json` — the offer definition: free discovery call,
  a $450/mo 1:1 "Sprint", a $1,200/quarter "Quarter" package, and a
  $150/mo group program, plus 3 testimonials.
- `site/` — the generated, ready-to-deploy landing page (`index.html`
  + legal page templates + `_headers`). Verified in a headless browser:
  hero, offer stack, testimonials, and the full click-through booking
  wizard all render and work with zero console errors.

## Why a coaching offer needs this structure

The reference video's "online coaching" product usually just means "a
Calendly link and a Stripe payment link," which converts badly because
there's no offer stack, no proof, and no path from stranger to booked
call. This page fixes that: it leads with the *problem* ("stop planning
to start"), shows a free low-commitment first step (discovery call),
then ladders into paid tiers, backed by testimonials — the actual
structure a $450+/mo offer needs to convert cold traffic.

## Make it yours

1. Edit `coaching-offer.json` — swap the niche (fitness, career,
   dating, finance, whatever you coach), rename the packages, adjust
   pricing.
2. Regenerate:
   ```sh
   node ../../site-builder/generate-site.js --input coaching-offer.json --outdir site
   ```
3. Set `business.siteUrl` once you have a domain, to also generate
   `robots.txt`/`sitemap.xml`.
4. Deploy `site/` to Netlify/Vercel/Cloudflare Pages (drag-and-drop the
   folder — it's fully static, no build step).
5. Swap the booking wizard's final step for a real payment link
   (Stripe Payment Links or Calendly) if you want to take money
   automatically instead of following up manually — the current wizard
   opens the visitor's email/SMS app with a prefilled summary, which is
   enough to start taking bookings on day one with zero setup.

## Selling it

This "product" *is* the sales page for a service, not a file you
deliver to a buyer — the thing you're selling is 1:1 or group coaching
time. See `marketing/` for the positioning, discovery-call script, and
launch content to fill this offer with actual clients.

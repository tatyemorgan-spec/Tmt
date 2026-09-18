# 100 AI Prompts for Local Service Businesses

A finished, sellable digital product: 100 copy-paste-ready AI prompts
across 10 categories (Google Business Profile, social media, email/SMS,
sales conversations, website copy, paid ads, reviews, operations,
seasonal campaigns, and strategy), written specifically for local
service businesses — salons, contractors, cleaners, trainers, and every
`site-builder` client this repo already targets.

This is the "AI Prompt Pack" product category from the reference video
(shown selling via Gumroad's "No-Code Prompt Pack"). It plugs directly
into this repo's existing audience: anyone using `../../site-builder`
to build a local business a website is exactly who needs this pack —
natural upsell/bundle.

## Files

- `prompt-pack.md` — source content (100 prompts, editable)
- `100-ai-prompts-local-service-businesses.pdf` — the finished,
  designed PDF deliverable (cover page + formatted sections), generated
  from the markdown via a headless-Chromium print-to-PDF pipeline (no
  paid design tool needed). Verified to render correctly.

## Regenerating the PDF after edits

```sh
# from this directory
python3 -c "
import markdown
src = open('prompt-pack.md').read()
lines = src.split('\n')
title = lines[0].lstrip('# ').strip()
i = 1
while lines[i].strip() == '': i += 1
sub = []
while lines[i].strip() != '': sub.append(lines[i].strip()); i += 1
subtitle = ' '.join(sub).strip('*').strip()
body = markdown.markdown('\n'.join(lines[i:]), extensions=['extra'])
# ...wrap in the styled HTML template, see git history of this file for the full script
"
```
(See the commit that added this product for the full HTML-template
script — the short version: convert `prompt-pack.md` to HTML with the
`markdown` package, wrap it in a styled cover + content template, then
`page.pdf()` it with Playwright's bundled Chromium.)

## Selling it

- **Price:** $9 (launch) → $17 (standard). This category sells in the
  $7–$25 range on Gumroad/Etsy; 100 prompts across 10 categories is on
  the higher end of what's typically offered, which supports the top of
  that range.
- **Platforms:** Gumroad (best for instant PDF delivery + easy
  checkout), Etsy (bigger built-in search traffic for "notion/planner/
  template" adjacent buyers), or bundle as a bonus with the Life OS
  Notion template (`../01-notion-life-os/`) or the coaching offer
  (`../05-online-coaching-offer/`).
- See `marketing/` for listing copy and launch scripts.

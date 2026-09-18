# Budget Tracker — self-contained web app

A real, working personal finance dashboard: log income/expenses, see a
live category breakdown chart, set monthly budget goals with progress
bars, and export/import your data as CSV. It's a single `index.html`
file — no build step, no npm install, no backend, no account, no
tracking. Data is stored in the visitor's own browser via
`localStorage`, styled after the same "no dependencies, ship one file"
philosophy as `../../site-builder`.

This is the same product category as the "Personal Budget Tracker"
vibe-coded app and the Etsy "Ultimate Budget" spreadsheet shown in the
reference video — except this one is a real, tested, working app, not a
mockup.

## Try it

Open `index.html` directly in a browser — no server needed:

```sh
open digital-products/02-budget-tracker-app/index.html   # macOS
xdg-open digital-products/02-budget-tracker-app/index.html  # Linux
```

Verified with an automated headless-browser smoke test (add a
transaction → shows in the list, updates balance, no console errors).

## What it does

- Add income/expense transactions with category, date, description
- Live monthly summary: income, expenses, net, all-time balance
- Donut chart of spending by category (pure Canvas, zero dependencies)
- Editable monthly budget goals per category with over-budget warnings
- Export all transactions to CSV; re-import a CSV to restore/merge
- Fully responsive, keyboard-accessible form controls

## How to sell this

**Option A — Sell the file directly** (Gumroad/Etsy), like a template:
buyer downloads `index.html`, double-clicks it, it just works. Zero
setup. This matches how budget spreadsheet templates already sell on
Etsy for $5–$15 — except yours is an interactive app, not a static
spreadsheet, which supports a higher price ($12–$25).

**Option B — Host it yourself as a free lead magnet** (Netlify/Vercel/
GitHub Pages, all free static hosting) and use it to capture an email
list before pitching a paid template pack or coaching offer — see
`../05-online-coaching-offer/`.

**Option C — White-label it** for a niche (freelancers, students,
couples budgeting together) by editing the categories array in the
`<script>` tag and re-skinning the CSS variables at the top of the
`<style>` block — this takes under 10 minutes and lets you sell the
"same" app multiple times to different audiences under different
names/branding.

## Customizing

Everything lives in one file. The parts you'll actually want to touch:

- `:root { ... }` at the top of `<style>` — brand colors
- `CATEGORY_COLORS` and the `<option>` list in the category `<select>`
  — rename/add categories
- `DEFAULT_BUDGETS` — starting budget goals shown to a new user

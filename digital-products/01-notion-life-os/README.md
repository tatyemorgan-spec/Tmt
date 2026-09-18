# Life OS — Notion Template

A one-page personal operating system: tasks, habits, goals, finances,
projects, learning, and journaling, cross-linked into one dashboard.
This is the same category of product shown selling for $149 in the
"Top 7 AI digital products" reference video (a Notion "Life OS" template).

Notion templates can't be generated through the Notion API without the
buyer's own workspace/integration token, so this package ships as
**import-ready CSVs + a page-by-page build script** — you assemble the
real Notion template once (15–20 minutes), then duplicate-link it forever
after. That one-time build is normal for every Notion template seller;
nobody in this niche ships a literal `.notion` file because the format
doesn't exist publicly.

## What's in the box

| File | Becomes this Notion database |
|---|---|
| `tasks.csv` | Daily Tasks |
| `habit-tracker.csv` | Habit Tracker |
| `goals.csv` | Goals |
| `finance-tracker.csv` | Finance Tracker |
| `projects.csv` | Projects |
| `learning-log.csv` | Learning Log (books/courses) |
| `journal-log.csv` | Daily Journal |

## Build it in Notion (one-time, ~20 min)

1. Create a new page called **Life OS**, add a cover + emoji icon.
2. For each CSV above: `/table` → **Import** → choose the CSV. Notion
   auto-creates the database with columns already named.
3. Fix property types after import (CSV import defaults everything to
   text):
   - `Priority`, `Status`, `Type`, `Category`, `Account` → **Select**
     (color-code the options)
   - `Due Date`, `Target Date`, `Deadline`, `Date` → **Date**
   - `Progress` → **Select** or switch to a **Number** formatted as %
   - `Amount` → **Number** (currency format)
   - `Mon`–`Sun` in the habit tracker → **Checkbox**
   - `Current Streak` → **Number**, or replace with a `Formula` that
     counts consecutive checked days
4. On the Finance Tracker, add a formula property:
   `Signed Amount = if(prop("Type") == "Expense", -prop("Amount"), prop("Amount"))`
   then add a **linked view** at the top of the Life OS page showing
   `Sum(Signed Amount)` grouped by month — this is the "dashboard" number
   buyers screenshot for their sales page.
5. On the main **Life OS** page, add linked database views for each
   table (`/Linked view of page` → pick each database), and arrange them
   in a 2–3 column layout using Notion's drag-to-columns. Suggested
   layout:
   - Row 1: Today's Tasks (filtered `Status != Done`) | This Week's Habits
   - Row 2: Active Goals | Finance summary
   - Row 3: Projects | Learning + Journal
6. Turn on **Templates** inside the Tasks and Journal databases (the
   `+ New` button dropdown → "New template") so buyers get a pre-filled
   row when they click add — this is the detail that makes a template
   feel premium instead of a bare database.
7. Duplicate the finished page, strip your personal entries back out
   (keep 1–2 example rows per database so it doesn't look empty), and
   that duplicate is your **sellable master copy** — get its public
   share link (Share → publish to web → "Duplicate as template" toggle
   on) and that link is the product you deliver.

## Selling it

- List price anchor from the reference video: **$149** for a full paid
  tier. A realistic starter price for a first launch is **$19–$29**,
  with a $49–$79 "Pro" tier that adds a Weekly/Monthly Review database
  and an automation walkthrough (Notion API + Zapier/Make).
- Deliver by emailing the Notion share link after purchase (Gumroad and
  Etsy both support this natively — see `marketing/` for the listing
  copy).

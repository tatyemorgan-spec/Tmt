---
description: Log a call to Close + calls.csv, update commission, trigger follow-up
argument-hint: [lead name] [outcome] [notes]
---
Input: $ARGUMENTS
Outcome must be one of: no_answer | voicemail | callback | not_interested | disqualified | booked | closed. If missing or unclear, ask.

1. Find the lead in Close. If no match or several, ask.
2. If I didn't give it and it's needed, ask for:
   - closed: product, full price, payment (full / split — how many payments and amounts / deposit only)
   - booked: product it's likely to be + day/time of the call
   - callback: callback date and time
3. Close: add a note (create_note) "<outcome> — <notes> — next: <next_step>". Apply the mapping in close-map.md, including the no-reply rule for no_answer/voicemail (count this lead's call attempts in the last 3 days via activity_search). Show me the status change before making it.
4. Append a row to logs/calls.csv: date,time (Europe/London),lead,company,outcome,ticket,deal_value,next_step,callback_date,notes. deal_value = full price. Quote fields containing commas.
5. If closed: commission is on the FULL price. Ticket from offer/offer.md (Airbnb Management = low 10%, 3-Month / Gold = high 7%).
   Add one row to earnings/commission.csv per payment: lead as "Name (1/2)", "Name (2/2)" etc for splits, deal_value = that payment, commission = payment × rate, status pending. Paid in full = one row.
6. Run follow-up-writer for every outcome except disqualified (and never for DNC). It picks the template from library/follow-up-playbook.md.
7. Confirm briefly: what went to Close, what went to CSV, then the finished text ready to send.

Shorthand is fine, e.g. `/log sarah callback thurs 6pm said needs to think, budget 7k` or `/log john no_answer`.

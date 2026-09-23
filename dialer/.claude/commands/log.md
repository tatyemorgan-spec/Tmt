---
description: Log a call to Close + calls.csv, update commission, trigger follow-up
argument-hint: [lead name] [outcome] [notes]
---
Input: $ARGUMENTS
Outcome must be one of: no_answer | voicemail | callback | not_interested | disqualified | booked | closed. If missing or unclear, ask.

1. Find the lead in Close. If no match or several, ask.
2. If I didn't give it and it's needed, ask for: ticket (high/low) and deal_value for closed/booked; callback_date for callback; next_step.
3. Close: add a note (create_note) "<outcome> — <notes> — next: <next_step>". Apply the status/opportunity/task mapping in close-map.md. Show me the status change before making it.
4. Append a row to logs/calls.csv: date,time (Europe/London),lead,company,outcome,ticket,deal_value,next_step,callback_date,notes. Quote fields containing commas.
5. If closed: append to earnings/commission.csv with rate 0.07 (high) / 0.10 (low), commission = deal_value × rate, status pending.
6. If outcome is callback, booked, not_interested or voicemail: run follow-up-writer.
7. Confirm in 3 lines: what went to Close, what went to CSV, what's drafted.

# Follow-up playbook: which text to send, when

All templates live in Close (Inbox → Templates → SMS). `/log` picks the right one from the outcome + my notes, fills in the name, day/time and one detail from the call, and gives me the finished text. I don't type anything.

## Situation → template
| Situation (from /log) | Template in Close | When | Then |
|---|---|---|---|
| New application, called, no answer | Tye — Speed to Lead (New Application) | straight after the first missed call | enrol in no-answer chase |
| No answer, attempt 1–2 (day 1) | No Answer #1 | after the 1st missed call if not new | call again same day PM |
| No answer, day 2 | No answer #2 | after the 3rd missed call | call again PM |
| No answer, day 3 (6th attempt) | Tye — No Answer #3 (Day 3 last try) | after the 6th missed call | Setter Pipeline (good lead) or NGMI |
| Voicemail left | Tye — Voicemail Left | straight away | same as no answer |
| Spoke, bad time / callback | Tye — Spoke: Callback Confirmed | straight away | call task on the agreed time |
| Spoke, booked with Freeman | Tye — Spoke: Booked With Freeman | straight away | then "Our Reviews" the same day |
| Booked, day before | Booked Call — Upcoming Reminder | day before | – |
| Booked, day of | Booked Call — Today's Reminder | morning of | – |
| Booked, didn't answer pre-call | Booked Call — Missed You | after the missed pre-call | – |
| No show | Tye — No Show Rebook | same day | status No Show, call next day |
| Spoke, "need to think" | Tye — Spoke: Thinking About It | straight away | callback in 2 days |
| Spoke, busy with work / time | Tye — Spoke: Busy With Work | straight away | callback in 2–3 days |
| Spoke, budget under £5k (£2.5k+) | Management Pitch | straight away | callback in 2 days |
| Spoke, wants proof | Our Reviews / Student Review or Case Study | straight away | callback next day |
| Spoke, not ready / wants to learn more | Airbnb Training Asset | straight away | callback after they've watched |
| Not interested | Tye — Not Interested (Door Open) | straight away | NGMI |
| Setter Pipeline, 2 weeks quiet | Tye — Nurture Check-in (2 weeks) | 14 days after last touch | – |
| Old webinar sign-ups | Pipeline Leads | on first call attempt | – |
| Disqualified (under £2.5k / not UK) | none | – | DQ |
| DNC | NEVER message | – | – |

## Antoinette's VSL no-answer sequence (how it's actually done)
0. Out of hours / can't call now → acknowledgement SMS straight away ("thanks for taking the time to watch, I'll be in touch shortly") + task for 9–10am.
1. Call → no answer → **VSL follow-up 1**: tried you about your application, quick call to understand your situation and goals and how Freeman can support you, when can I call? + task.
2. Call → no answer → **VSL follow-up 2**: "have I got the right person?" + task next day.
3. Call → no answer → **Last message**: reached out several times, no worries if not for you, if you are interested let me know and we'll pick up where we left off. + task to check next day.
4. No response → NGMI (door left open).
Her templates are coming. Swap the wording in once she sends them.

## Reminder cadence (Antoinette, softer than the SOP)
Freeman's ideal is morning, afternoon and 5 mins before, but leads have complained about being chased. Do: morning SMS + one call later (or the other way round), then ~15 mins before: "You're on in 15, check in early and make sure the link works." If the call is a week+ away, touch base every 2–3 days (e.g. call on Monday → contact Friday with videos for the weekend → Monday morning check).

## After a sale
Congratulate on WhatsApp (log it in Close). Task a few days before each instalment: "Call to see how they're enjoying the programme + remind about next payment".

## Show-rate sequence after booking (from the SOPs)
1. On the call: invite accepted while on the phone, Meet ready, quiet place, decision maker attending.
2. Straight after: booking confirmation text + prep asset (VSL / case study / training).
3. 24 hours before: "Hey [Name], just confirming you're still good for your strategy call tomorrow at [time]. Make sure you've watched the video I sent, accepted the invite and you're joining from somewhere quiet."
4. Morning of: Booked Call — Today's Reminder.
5. 1–2 hours before (if the call's later in the day): "Quick reminder, your call with Freeman is coming up shortly. Make sure you're somewhere quiet and ready to go through your goals properly."
Don't over-contact. Keep it clean.

## Webinar leads
**Correction from Antoinette:** after the webinar, leads book a **discovery video call with you**, not Freeman. You qualify them on a 20–30 min video call (camera on), then book them with Freeman.
- Booked after webinar → call within 1 hour, 3–5 min touchpoint, no answer = voicemail + text + try next working day.
- Attended, didn't book → "Did you get value from it? Any reason you didn't book at the end?"
- Registered, didn't attend → offer the free training asset, then lightly qualify.
- Whole list worked within 3 working days (2–3 attempts + a text each). Shout early if that's not realistic.

## Rules
- One text per call attempt. Never two texts in a row without a call in between.
- Fill in every [DAY] / [TIME]. Never send a template with brackets left in.
- Add one specific thing from the call if there's room ("you mentioned Manchester…").
- Texts are sent from Close by me (one click from the lead page). Claude can't send SMS directly through the Close connector.

## No-answer chase workflow (to build in Close: Automations → Workflows)
Needs the "manage email sequences" permission (Freeman can grant it, or build it himself).
Name: Tye — No Answer 3-Day Chase · Trigger: manual enrol on contact · Start straight after the 1st missed call.
1. SMS: No Answer #1 — immediately
2. Call (assigned to Tye) — 4 hours later
3. Call — next morning
4. SMS: No answer #2 — straight after
5. Call — 5 hours later
6. Call — day 3 morning
7. Call — 5 hours later
8. SMS: Tye — No Answer #3 (Day 3 last try) — straight after
9. Task: "6 attempts, no reply → Setter Pipeline if good lead, otherwise NGMI"
Stop when: they reply by text/email, call in, book a meeting, or the lead moves to New Opportunity / NGMI / DQ / DNC / Signed Up / Deposit Paid / Signed Up - Balance Owed.

## Automation plan (once Tye is Super User)
Close has no call outcomes set up. The Sales opportunity pipeline tracks deals, not what happened on a call. So workflows are triggered by lead status:
| Trigger | Workflow |
|---|---|
| New lead created (New Lead / New Webby Opt ins / New Webby Sign Ups) | Speed to Lead text + call task now |
| Tye clicks "enrol" after a missed call | No Answer 3-Day Chase (above) |
| Lead moves to New Opportunity (booked) | Booked confirmation text + day-before and day-of reminders |
| Lead moves to No Show | No Show Rebook text + call task next day |
| Lead moves to Setter Pipeline | Nurture Check-in text after 14 days |
Sales pipeline stages (Call Booked → Pending Close → Signed Up / Deposit Paid) stay as the deal tracker, and /eod and /weekly read them for bookings and closes.

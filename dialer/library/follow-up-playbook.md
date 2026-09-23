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

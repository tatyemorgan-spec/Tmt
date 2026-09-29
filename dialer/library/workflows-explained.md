# Close workflows: how they work behind the scenes + how to edit them

## The 3 parts of every workflow
1. **Trigger (what starts it)**
   - **Manual enrol:** you click "Enrol in workflow" on a lead/contact. Nothing happens unless you do.
   - **Lead status change:** starts automatically when a lead moves into a status (e.g. No Show). Changing the status *is* the trigger.
2. **Steps (what it does, in order)**
   - **SMS:** sends a saved Close text template from your number.
   - **Call:** puts a call in your Close inbox to make (it doesn't dial for you).
   - **Task:** a reminder in your inbox.
   - Each step has a **delay** (wait X hours/days after the previous step).
3. **Goals (what stops it early)**
   - They reply by text/email, call in, book a meeting, or the lead moves to a "finished" status (New Opportunity, NGMI, DQ, DNC, Signed Up…). Then the rest of the steps are cancelled automatically, so nobody gets chased after replying.

## The workflows (all built as drafts)
| Workflow | Trigger | Steps | Stops when | Status |
|---|---|---|---|---|
| **Tye — VSL No Answer (Antoinette rhythm)** | Manual: enrol after a missed call on a new VSL lead | Text FU1 now → call ~5h later → text FU2 → call next day → text FU3 (last try) → next day: task "move to NGMI" | Reply, call-in, booking, status change | **Switch ON** |
| **Tye — No Show Rebook** | Lead status → **No Show** | 30 min later: rebook text → next day: call → task "try once more, then Setter Pipeline or NGMI" | Reply, call-in, booking, status change | **Switch ON** |
| **Tye — Setter Pipeline Nurture + Video** | Lead status → **Setter Pipeline** | 14 days later: check-in text + "How to Start an Airbnb 2026" video → 2 days later: call task | Reply, call-in, booking, status change | **Switch ON** |
| Tye — Booked With Freeman | Lead status → **New Opportunity** | Team "Upcoming Reminder" text now + task "send prep video, set reminders" | NGMI / DQ / DNC | Optional (see note) |
| Tye — New Application Speed to Lead | New lead created | Call task + text after 15 min | – | **OFF** (would hit Ray's leads) |
| Tye — No Answer 3-Day Chase | Manual | 6 calls + 3 texts | – | **OFF**, replaced by Antoinette rhythm. Delete. |
| Tye — Setter Pipeline Nurture (plain) | Setter Pipeline | Text after 14 days | – | **OFF**, replaced by + Video. Delete. |

Note on Booked With Freeman: VSL self-bookings go to New Opportunity automatically, so the text fires straight away. That works as an instant acknowledgement. But it also fires when *you* book someone after a call, so they'd get a generic text on top of your confirmation. Keep it off unless Freeman wants the auto-text.

## How to edit a workflow (Close → Workflows)
1. Open the workflow. You'll see the trigger at the top and the steps below.
2. **Change a message:** either pick a different template on the SMS step, or edit the **template itself** (Templates → SMS). Editing the template changes it everywhere it's used, including workflows.
3. **Change timing:** click a step and change its delay.
4. **Add/remove steps:** + between steps / the step's menu → delete.
5. **Change the trigger / stop rules:** edit the trigger block and the "Goals" section.
6. **Turn on/off:** Activate / Pause at the top. Pausing stops new enrolments. Check what happens to people already in it before pausing.
7. Leads already in a workflow may keep the old version, so test on a test lead after big edits.

Claude can create workflows and edit templates, but can't edit or delete an existing workflow. Timing/trigger edits are done in Close by Tye or Freeman.

## Settings to check before switching on
- **No re-enrolment:** a lead shouldn't be able to go through the same workflow twice.
- **Sending number:** texts go from Tye's Close number.
- **Quiet hours / business hours:** if available, stop texts going out at night.

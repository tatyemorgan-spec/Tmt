---
description: Write "Next call plan" notes in Close for a lead, or for all of today's tasks
argument-hint: [lead name | "today" | "week"]
---
Write Next call plan notes in Close.

Target: $ARGUMENTS
- A lead name: that one lead.
- "today" or blank: every open task assigned to Tye (user_ozxlLsH3saSC5svO2cIwyBP51QJ6GQFic86CgA1heR8) due today or overdue, PLUS every lead in New Lead or New Opportunity status that has no open task (fresh or handed-over applications that would otherwise be missed). Skip test leads (Tye, Freeman Richards Test, Freeeman).
- "week": open tasks due in the next 7 days.

For each lead:
1. Skip it if it already has a note titled "Next call plan" created in the last 3 days, unless there's been new activity since (a call, SMS or note after the plan).
2. Read everything: fetch_lead (application answers, Calendly info), activity_search for the lead (calls, notes, SMS, status changes), and the task text.
3. Read offer/icp.md (routing) and library/vsl-script-freeman.md (flow + objection handling).
4. Write the note with create_note in exactly the format in library/call-plan-format.md. Freeman can see these notes, so keep it professional.
5. Never send texts or emails, and never change statuses. Notes and task times only.

## Then time and prioritise the tasks (every "today" run)
After the plans are written, give every task in the run a real time slot with update_task, so Close shows them in call order:
1. **Keep fixed times.** Leave alone any time a lead agreed ("6pm", "after 6:30"), any time Tye set himself today, and pre-call check-ins tied to a Freeman call (they must land before the call).
2. **Find when each lead picks up.** Use activity_search (calls + SMS + WhatsApp, direction inbound) for the leads in the run, and note the times they replied or called back, plus anything in notes or task text ("at work", "construction", "after class", "nurse", "evenings", "Wednesdays"). Close times are UTC; BST = UTC+1.
3. **Slot them** using library/daily-workflow.md (times BST):
   - 09:00–10:30: new apps and booked/New Opportunity pre-calls first, then same-day Freeman check-ins and payment checks.
   - 10:30–12:30: anything else with a reason to be early, plus timed tasks.
   - 13:00–16:00: untimed follow-ups in this order: New Opportunities → VSL follow-ups → "watched the videos?" check-ins → under £5k → webinar → no-shows → nurture.
   - 17:00–19:00: 9–5 workers, no-shows who work days, and anyone whose replies come in after work.
   - If a lead's pickup times clearly differ from their block, use their times.
4. **Spread them out.** 10–15 minutes apart, never two tasks at the same minute (except two tasks on the same lead, which share a slot). Don't set a time that has already passed: the earliest slot is the next quarter hour.
5. **Priority:** set `high` on booked/New Opportunity pre-calls, same-day Freeman check-ins, payment checks and brand-new apps. Leave everything else `medium`.
6. Date-only tasks ("Follow up" with no time) always get a time.

Finish with a short list in chat, in time order: time (BST) · lead · aim in a few words, with high-priority ones marked.

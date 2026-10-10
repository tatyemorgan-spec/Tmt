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
5. Never send texts or emails, and never change statuses. Notes only.

Finish with a short list in chat: lead · aim in a few words · call order (hottest first).

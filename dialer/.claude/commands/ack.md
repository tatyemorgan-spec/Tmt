---
description: Pick the right VSL acknowledgement text (New App vs Booked Call) for new apps and get it ready to send
argument-hint: [lead name | "new" for all unacknowledged apps in #1-new-apps]
---
Close has no send-SMS tool here, and CLAUDE.md says texts are never sent without Tye. So this command picks the template and renders it. Tye sends it in Close (SMS → Templates → the named template) or pastes the rendered text.

1. Leads:
   - With a name: find that lead in Close (`lead_search`).
   - With "new" or nothing: read #1-new-apps (C0AR1EBGVMG, see slack-map.md) for NEW APP posts from the last 24h and use the Close link in each.
   - Skip test or junk entries ("TEST" answers, fake emails like ff@gmail, Freeman, the agency) and DNC leads. List what you skipped and why.
2. For each lead, `fetch_lead` and decide:
   - **Already acknowledged**: an outbound SMS starting "Hey <name>, thank you so much for taking the time to watch our Airbnb video" exists. Skip it and say so.
   - **Booked Call**: status is New Opportunity (a Calendly booking moves it there automatically) OR it has an opportunity "New Deal - Call Booked". Use template **Tye — Acknowledgement: Booked Call** (smstmpl_5157pyEZoYTfdYxIteysW0).
   - **New App**: anything else. Use template **Tye — Acknowledgement: New App** (smstmpl_40N2Eeda74Nr4RQLGIb1Vh).
   - Fetch the template text live (`fetch_sms_template`) so wording changes in Close are picked up. Swap `{{ contact.first_name }}` for the contact's first name (tidy the capitalisation; if the name is a company or blank, use "Hey there").
3. Output one block per lead:
   `Name · phone · status · TEMPLATE: <name>`
   then the rendered text, ready to paste.
4. Don't change statuses, don't create tasks, don't touch Slack (claiming ✅ only if Tye says "claim").

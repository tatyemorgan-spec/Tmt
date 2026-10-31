# Airtable lead notes (daily, 8pm, or when I ask)

Keeps the **Notes** field in Freeman's Airtable up to date for every lead I'm working, so Freeman can see where each one is at a glance.

## Where
- Base `apprRWnDaokPRsGbA` (Freeman's lead tracker), table `tbllJDxYx7RoXq0qt`.
- Notes field: `fldeTX3CWNSOIwwPf` (long text). Name `fldoKta54jH7DfFhT`, email `fld0QUZ2sgPWC5J9Q`, phone `fldzRL50J8FNVxHi9`, date `fldnk1QbCYDSg7wOc`.
- Only the Notes field gets written. Never touch any other field (status, outcome, revenue).

## Which leads
- Every row dated **24 Sep 2026 onwards** (my start date). Skip test rows ("TEST PAYLOAD", "test lead", "Test"), agency rows (mentormedia) and "Spare".
- On the daily run, only rewrite a note when something has changed in Close since the last run (new call, SMS, note, status change, or the row has no proper note yet). Leave the rest alone.
- Match each row to Close by name, then email or phone if the name doesn't match. Known odd matches: Toyosi Omojayogbe = Close "Tatiana"; Olayinka Bello = Close "Ola"; Highrands Group = "Hyron"; Airtable "Kenzy" = Close "K" (Kenzie, kmaafi07@).

## Which format
**Had a full qualifying call** (a real conversation that covered money, goals and work: usually 6+ minutes, or Antoinette's qualifying notes) → the full note:

```
Qualified:
Journey:
Result wanted:
Working:
Vision:
Timeframe:
Blocker:
Funding:
Location: (if known)
```

**Not qualified yet** (not reached, a short call, DNC, DQ, NGMI) → a basic summary:

```
Status:
Where we are:
Next step:
```

Both formats:
- Written by me, in the first person ("I called", "my call"), never "Tye".
- Facts only from Close (application, calls, transcripts, SMS, notes). Unknown = say it's unknown.
- Professional: Freeman reads these. No prices, payment plans or discounts in my words.
- Keep the existing `Source: ... | Page: ATA1` line at the bottom if the row has one.
- If the row already had a handwritten note from me or Antoinette, keep it underneath as `Previous note: ...`.
- Short. One or two lines per heading.

## Freeman's meeting notes (Tye, 25 Oct): every lead Freeman has had a call with
Freeman writes his own note in Close after each call (by Freeman Richards: "CRM Summary", "CRM Note", "Meeting Purpose", "Next Steps"). Ignore his notes that are only the copied application answers ("Where are you on your property journey…").
- On every run, check for new Freeman notes (`find_notes` with Freeman's user ID `user_biI7njoZpqjJ7jKTFxZyoPyOqd1Ey75s6BsQAHYkXn1`, created since the last run) and add them to that lead's row, including Ray's leads.
- Add a `Freeman's call notes (D Mon):` section above `Next step:`, one dated line or two per call: what was agreed, the outcome, key facts about them (background, goal, who decides, concerns), first session date and the actions for me or Ray. Update `Next step:` to match.
- Leave out prices, payment plans, instalments, discounts and interest even though Freeman's note has them. "Signed up (Management)" or "first payment by Mon 8pm" is fine; the amounts are not.
- Check his dates against the calendar (e.g. "Monday 27 Oct" when 27 Oct is a Tuesday) and flag any that don't match.
- Rows with no Airtable entry (some DM/Instagram leads): mention them in the chat reply instead.

## After the run
Reply in chat with: how many rows updated, who moved forward today (booked, qualified, closed), and anything that needs my attention (payment not confirmed, Freeman outcome missing, wrong numbers).

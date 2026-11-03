# Airtable map: FREEMAN RICHARDS base (apprRWnDaokPRsGbA)

Connected 2026-09-25. **Tye has READ-ONLY access**, so Claude can read but not write. Tye updates rows by hand (or ask Freeman for editor access and Claude can do it).

## Tables
| Table | ID | Used for |
|---|---|---|
| CRM (to use) | tbllJDxYx7RoXq0qt | VSL / organic leads + booked calls |
| WEBINAR AIRBNB | tbleGeadQVXxjqDhJ | Webinar leads, has **Host** column |
| KPI | tblZ8WQFffrr7xLag | Ad spend, CPM, CPC, CTR, clicks by date/ad. Use this to see how consistently ads are running |

## Fields to update after every booked call
| Field | Values |
|---|---|
| Call Outcome | Scheduled · Qualified \| In Progress · Qualified \| Long term · Cancelled \| No-show · Not interested (CRM) / Not interested / not ready (Webinar) · DQ - Not A Fit · Closed - Won · Closed - Lost |
| Notes | e.g. "No show after confirming", "Booked with Freeman for [date]" |
| Date Call | date of the call |
| Date Closing | date the money was paid |
| Revenue | full price **incl. VAT** |
| Cash Collected | amount paid so far **ex VAT** (first instalment only if split, update when the next one lands) |
| Host (Webinar table only) | Freeman · Antoinette (Tye to be added by marketing) |
| Setting status | Contacted · Fake number |
| Status (CRM) | Optin · Application · Call Booked · Repeat Lead |

## How Claude uses it
- /log tells Tye exactly which row + values to set in Airtable after booked / cancelled / no-show / closed.
- /eod and /weekly can read Call Outcome counts (cancellations, show rate) and the KPI table (ad spend / consistency).

# Close map (pulled live from Close on 2026-09-23)

Org: F Rich Consulting · currency GBP · me: Tye Morgan (`user_ozxlLsH3saSC5svO2cIwyBP51QJ6GQFic86CgA1heR8`), timezone Europe/London.

## Lead statuses
| Label | ID |
|---|---|
| New Lead | stat_iVYDtUSWDKP4SHBrfWS9o4RurikYw2W6EEOxuG4ZPX1 |
| New Opportunity | stat_9j1C1NhtRZZIRIgzWt5PJhuGSQbWvVtIbQxartAhSu6 |
| Setter Pipeline | stat_kszuXEcrLZmai6Jr1V6zz4F82H7KDqSNfXcSL8KHLB8 |
| Closer Follow Up | stat_LIhyRBtPmdUfgKQNH1veZ1HwX62csa4R0AUTcEUMNNi |
| No Show | stat_eRigetiPeo1oRaUD8I5A5DR5BL6X5P3tpl3i66gbPsT |
| Signed Up | stat_kS2MjBIgY1oiE11Ub15x9DxU0EL15hrY34sTXc49vGd |
| Signed Up - Balance Owed | stat_RgKckg6wNYHM160BmaHDJdSgQUe6I3Xm18iqoPeil8Y |
| Deposit Paid | stat_TxMguK0S3UUn0fjxZp5NcCQGuI2uIyl9zoI32yFuXYU |
| NGMI | stat_9OY9ByBWXd9Qc3C3l4gyJ8RDL7WzXHFhU3clKXpTwpt |
| DQ | stat_qJSHOTYVCIpGbfQkqAc10Cvji4u9fWvZCTRhIHBHQpj |
| DNC | stat_YhdeK8Ib71gmvB3OxhUtzHToX1ZEDf5mdvxPn1WJW4J |
| New Webby Opt ins | stat_LEGarBVBIp0FJweaOZMXevROIn2DgmdYxEuQ1lCcHAu |
| New Webby Sign Ups | stat_KSiB7bITJIPVWVSDbroSY6kR0QP0AJaaJEXYZu3gSkC |
| Old Webby Sign ups | stat_5sZcbaSl8JM6nsaRttOVk1UbLAb1NKdDwLQ76CIC3pZ |
| Webby Sign ups - No Book | stat_vp0TJCmLGGSaepCcgCkvTpZWmTMuurZNwIoV3dsatnw |
| Calendly Import | stat_wxFCPPFO1IrbaS5elVRVe3yDJ4vxzRan9VWAJ9zlaeg |
| Calendly Import Follow Up | stat_ttNAJz7R0loX2UY0i74tEfucjKw1EaLChv4vnIoXDfB |
| Refunds | stat_CbGYE2o1FnkTFqkjrTkzaCZjNDFafwjQI7NVzXzOrSO |
| Withdrawn | stat_Ms7uwWWkRtDfhpHUmM9aTiDtRMyNQcLNHEFOVyOKjGB |
| event | stat_aauD9hOOrEKaIDzg1lYaWhUsFVceIy5oFoMcTIffa03 |

## Opportunity pipeline: Sales (`pipe_2D0Pst2BdH5WAd1KAVzymV`)
| Label | Type | ID |
|---|---|---|
| New Deal - Call Booked | active | stat_naA7WoafcONPyOp73uIzBCxVpZUDeGnHM8BA5GsrrER |
| New Deal - Pending Close | active | stat_tvl0H81ZwS9fHzjnHjgspIHahThz3efiv4ZXyofB6h5 |
| Instalment Pending | active | stat_u4aSiITWw8Bu0cmWNxAZi8rJLZfyWnpQP8YqSAnspRi |
| Signed Up | won | stat_tzpZlkWpPwjwb3w2vGE6Zr0z0k2GJr0hoXqnbcRdwhg |
| Deposit - Paid | won | stat_tWSMvSJ5z6JPMYqg5CojdPohRwmTuHFnfHXNVQOs0N5 |
| Instalment Paid | won | stat_8BPSslgSJbotUCsuhEUYtptv4GqIxTiGNQzOiFL70Hl |
| New Deal Lost | lost | stat_TuLB9b4rHxuDJYCpNlr9untsbhZD9IAyNhfpB2pYqKp |

Opportunity values in Close are in pence (£1 = 100).

## /log outcome → Close (confirmed by Tye 2026-09-23)
| Outcome | Lead status | Task |
|---|---|---|
| no_answer | unchanged until the no-reply rule kicks in | call task: next slot (same day PM or next day AM) |
| voicemail | same as no_answer | same as no_answer |
| callback | unchanged | call task on callback_date |
| not_interested | NGMI | – |
| disqualified | DQ | – |
| booked | New Opportunity **+ add opportunity "New Deal - Call Booked" with the call date** (VSL self-books do this automatically) | – |
| closed | Signed Up (paid in full) / Signed Up - Balance Owed (split, balance due) / Deposit Paid (deposit only) | – |

**No-reply rule:** count call attempts on the lead in Close over the last 3 days. At 6 attempts (2 a day, 3 days in a row) with no connect:
- fit score 6+ (from the brief, or funding £5k+ with a timeframe) → Setter Pipeline
- otherwise → NGMI
Always show Tye the status change before making it.

On booked: if you booked it (webinar discovery / qualified lead), set lead status New Opportunity AND create the opportunity with the call date. Antoinette: skip it and the booking doesn't show properly.

**Cancelled / no-show:** lead → Setter Pipeline (or NGMI after 3+ failed contacts), opportunity → **New Deal Lost** with note "no show after confirming" / "cancelled: info only". Set a follow-up task (~2 weeks).
**Closed:** opportunity → Signed Up / Deposit - Paid (won). Then update Airtable (see library/antoinette-training.md).
**Duplicates:** merge leads with the same email/phone. Note if funding answers differ.

Rule: DNC status = never dial, never draft follow-up.

## Lead source form (seen on inbound leads' description)
Q1 property journey stage · Q2 90-day goal · Q3 work situation · Q4 name · Q5 email · Q6 dream life in 1 year · Q7 timeframe to start · Q8 biggest blocker · Q9 UK mobile · Q10 funding available.

## Workflows (created as DRAFTS 2026-09-25, Tye is Super User)
| Workflow | ID | Trigger |
|---|---|---|
| Tye — No Answer 3-Day Chase | seq_4Xx86tRrpRO9cWy2ucQLzU | manual enrol on contact |
| Tye — New Application Speed to Lead | seq_2QTW5NYNd4IuK12ocLwKlq | **KEEP OFF (Tye, 25 Sep): would hit Ray's leads too.** Send the acknowledgement text by hand instead. |
| Tye — Booked With Freeman | seq_6x6TnD840vIGNk1WOjcmHp | lead moves to New Opportunity |
| Tye — No Show Rebook | seq_6A0SGQ6uJ8XYzH2Ipn1OVJ | lead moves to No Show |
| Tye — Setter Pipeline Nurture | seq_6ZMObidJY6M5tK0HC4TuRP | lead moves to Setter Pipeline |
All stop on reply / inbound call / booking / move to a closing status. Nothing runs until switched on in Close.
| Tye — VSL No Answer (Antoinette rhythm) | seq_6lf5CtBmykRENhAdvGNsAl | manual enrol: VSL FU1 → call → FU2 → call next day → FU3 → task: NGMI. **Use this one instead of the 3-Day Chase.** |
| Tye — Setter Pipeline Nurture + Video | seq_61it7J56wrHHDOCOSrQG3o | lead moves to Setter Pipeline: after 14 days sends "How to Start an Airbnb in 2026" video, call task 2 days later. **Use this instead of the plain Nurture one.** |

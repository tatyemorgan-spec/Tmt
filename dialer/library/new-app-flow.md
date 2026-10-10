# New app flow (ads → #1-new-apps → call)

Used by the hourly watcher routine, `/ack` and `/callplan` for fresh VSL applications.

## 1. Slack → Close
1. Read the NEW APP post in #1-new-apps (C0AR1EBGVMG). Note the funnel (ASA2, ATA1, …), name, phone, financial qual and Close link.
2. Open the Close link (`fetch_lead`). Read the form answers in the lead description, the status, opportunities and any activity.

## 2. Which offer? (the funnel decides)
* **ASA2 = rent-to-rent.** £5k+: rent-to-rent only (£7k+: never mention Management). Under £5k: Management via the 2-in-1 on the call.
* **ATA1 = Airbnb Management.** Management only, whatever the funds.
* Send ONE video, for the route you're leading with. Never both.
Coaching detail (intro, soft money question, management breakdown, asset ladder): library/vsl-script-freeman.md, "Freeman's coaching, 8 Oct".

## 2c. Unqualified apps ("under £5,000, no credit"): Freeman's opener
These people didn't get the booking link. Don't open like a normal app. Tell them straight that they didn't qualify to book in, then offer to see what we can still do. It makes the Freeman call feel earned, not automatic.

> "Hi [Name], it's Tye from Freeman Richards' team. I can see you filled in an application to work with Freeman. Looking at your application, unfortunately you didn't qualify to book straight in for a one-to-one strategy session with Freeman. That's either because, from your answers, we felt you might not be looking for one-to-one mentorship and guidance, or because you might not have the capital to get started right now. But I wanted to see how I could still help you, or how we could still get Freeman to help you hit the goal you set out on your application, which is [their Q6, in their words]. Have you got 5 minutes to explore that, if it's still something you're interested in?"

Then straight into money:
> "Great, let's get straight into it. What have you actually got set aside that you've committed to, where you've said: this is me, I'm happy to invest this into my education, my training and getting my first property? What does that look like exactly?"

Then:
> "OK, that's not bad at all. I can see from your application you really tried, so I'm going to see what we can do. Let's see how this conversation goes, and at the end I'll let you know if you're eligible to be booked in with Freeman."

Run the normal discovery (work, pain, goal, location, who's involved), then route: about £2.5k+ → Management (2-in-1 on ASA2) and book Freeman ("Good news, you're eligible"); less → offer/icp.md (Deal Sourcing, Blueprint or YouTube). Applies to both ASA2 and ATA1.

## 2b. What kind of lead?
| Check | Means | Do |
|---|---|---|
| Status **New Opportunity** or opp "New Deal - Call Booked" | Booked a Freeman call themselves (Calendly moves them automatically) | Ack: **Tye — Acknowledgement: Booked Call**. Plan = pre-call before Freeman: qualify, confirm the slot, video + one rule. |
| Status **New Lead**, no booking | Applied, no call booked | Ack: **Tye — Acknowledgement: New App**. Plan = first call: qualify, route, book. |
| Earlier DNC / NGMI / old webinar history | Re-applied | Flag to Tye before calling. Check why it was closed. |
| "TEST" answers, fake email, agency domain | Test | Skip. |

Already sent an ack (outbound SMS starting "Hey <name>, thank you so much for taking the time to watch our Airbnb video")? Don't send another.

## 3. The three answers that shape the call
The Q numbers differ by funnel, so go by the question, not the number.

| ASA2 | ATA1 | Question | What it decides |
|---|---|---|---|
| **Q6** | Q5 | Dream life in 1 year / 12 months | **The hook.** Open with it, use it to book, use it to answer "think about it" and "not now". |
| **Q3** | Q4 | Current working situation | **The approach and the time objection.** |
| **Q7** | Q6 | How soon to start | **Urgency and the "not now" objection.** |
| Q8 | Q7 | Biggest thing stopping you | Bonus: the first objection they'll raise. Answer it before they do. |
| Q10 | Q8 | Funding | Route (offer/icp.md). "Under £5k" = ask the exact figure. |

### Q6: dream life → hook
| Answer type | Approach |
|---|---|
| Specific (quit job, £X a month, family, travel) | Repeat it back in their words early: "You said … What does that look like day to day?" |
| Vague ("fulfilment", "estate", one word) | Dig: "When you wrote [word], what did you mean? What would be different in your life?" Get a real goal before money. |
| Ownership or portfolio | Freeman's story: Airbnb cash flow funded his first home. R2R/Management is the fast route to buying. |
| Joke, blank or "TEST" | Likely low intent or a test. Qualify hard and early. |

### Q3: work situation → approach + time objection
| Answer | Approach | Pre-empt |
|---|---|---|
| Full-time, building alongside | Respect their time. Short calls at the times they pick (lunch, evenings). | Raise time yourself: "Most of Freeman's students have full-time jobs. Most of the work is upfront set-up, then systems. Could you give it 3–5 hours a week?" |
| Part-time / flexible | Lean into speed: "You've got more flexibility than most, so you could move quickly." | Pre-empt "maybe later": flexibility is the advantage now. |
| Self-employed / business owner | Peer to peer. Talk systems, ROI and the business case. Less hand-holding. | "Is this another thing on your plate?" → it's systemised, a separate income stream. |
| Unemployed / student | Check funds carefully. Be kind. | Money objection is likely. Confirm liquid funds early. Under £1k = free content. |
| Shift worker | Amara's story (12-hour shifts, still runs it). | Time objection, same as full-time. |

### Q7: how soon → urgency + "not now"
| Answer | Approach | Pre-empt |
|---|---|---|
| Immediately / ASAP | Match their energy. Book the soonest Freeman slot (this week). | "Think about it" at the booking stage: "You said ASAP. The call with Freeman is the next step, so let's get it in this week." |
| Within 30 days | Book this week or next. Anchor on their date. | "Not yet": "You said within 30 days. Freeman's call is how you hit that." |
| 1–3 months+ / just researching | Find out why that date. Is it real (money, move, visa) or fear? | "What will be different in 3 months?" If it's real: agree a date and set a task. If vague, Freeman's "same spot, three months later". |

### Q8: blocker → first objection
| Blocker | Pre-empt with |
|---|---|
| No clear step-by-step plan | "That's exactly what Freeman maps out with you, a plan for your situation." |
| Don't know how to find or assess properties / landlords | Deal-analysis and sourcing are core to the mentorship; mention a student story. |
| Knowledge / confidence | 1:1 support, not just a course. |
| Money | Confirm the real figure early; credit-card offset; route correctly. Never payment plans. |
| Time | See Q3. |

## 4. The plan note
Use library/call-plan-format.md. In WHERE THEY'RE AT, quote their Q6, Q3, Q7 and Q8 answers. APPROACH comes from Q3 + Q6. CONVERSATION FLOW opens with the Q6 hook. LIKELY CONCERNS lists the Q3/Q7/Q8 objections with the pre-empt line. Then the task due now and the ack text for Tye to send.

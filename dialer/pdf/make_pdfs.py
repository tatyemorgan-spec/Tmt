from reportlab.lib.pagesizes import A4
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                KeepTogether, ListFlowable, ListItem)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

pdfmetrics.registerFont(TTFont("DV", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("DV", normal="DV", bold="DVB", italic="DV", boldItalic="DVB")

INK = colors.HexColor("#1f2933")
MUTED = colors.HexColor("#52606d")
ACCENT = colors.HexColor("#0b6e4f")
SAYBG = colors.HexColor("#eef7f2")
TIPBG = colors.HexColor("#fff6e5")
WARNBG = colors.HexColor("#fdecec")
LINE = colors.HexColor("#d9e2ec")

S = {
    "title": ParagraphStyle("title", fontName="DVB", fontSize=20, leading=24, textColor=INK, spaceAfter=4),
    "sub": ParagraphStyle("sub", fontName="DV", fontSize=10, leading=14, textColor=MUTED, spaceAfter=10),
    "h2": ParagraphStyle("h2", fontName="DVB", fontSize=13, leading=17, textColor=ACCENT, spaceBefore=12, spaceAfter=5, keepWithNext=1),
    "h3": ParagraphStyle("h3", fontName="DVB", fontSize=10.5, leading=14, textColor=INK, spaceBefore=6, spaceAfter=3, keepWithNext=1),
    "p": ParagraphStyle("p", fontName="DV", fontSize=9.5, leading=13.5, textColor=INK, spaceAfter=4),
    "say": ParagraphStyle("say", fontName="DV", fontSize=9.5, leading=13.5, textColor=INK),
    "cell": ParagraphStyle("cell", fontName="DV", fontSize=8.8, leading=12, textColor=INK),
    "cellb": ParagraphStyle("cellb", fontName="DVB", fontSize=8.8, leading=12, textColor=colors.white),
    "foot": ParagraphStyle("foot", fontName="DV", fontSize=7.5, textColor=MUTED),
}

W = A4[0] - 36 * mm


def box(text, bg, label=None):
    inner = (f"<b>{label}</b><br/>" if label else "") + text
    t = Table([[Paragraph(inner, S["say"])]], colWidths=[W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEBEFORE", (0, 0), (0, -1), 3, ACCENT if bg == SAYBG else (colors.HexColor("#d97706") if bg == TIPBG else colors.HexColor("#c0392b"))),
    ]))
    return [t, Spacer(1, 5)]


def render(blocks):
    out = []
    for kind, val in blocks:
        if kind == "title":
            out.append(Paragraph(val, S["title"]))
        elif kind == "sub":
            out.append(Paragraph(val, S["sub"]))
        elif kind == "h2":
            out.append(Paragraph(val, S["h2"]))
        elif kind == "h3":
            out.append(Paragraph(val, S["h3"]))
        elif kind == "p":
            out.append(Paragraph(val, S["p"]))
        elif kind == "say":
            out += box("“" + val + "”", SAYBG)
        elif kind == "tip":
            out += box(val, TIPBG, "Tip")
        elif kind == "warn":
            out += box(val, WARNBG, "Don't")
        elif kind == "bullets":
            out.append(ListFlowable([ListItem(Paragraph(b, S["p"]), leftIndent=10) for b in val],
                                    bulletType="bullet", start="•", leftIndent=12, bulletFontName="DV"))
            out.append(Spacer(1, 3))
        elif kind == "steps":
            out.append(ListFlowable([ListItem(Paragraph(b, S["p"]), leftIndent=12) for b in val],
                                    bulletType="1", leftIndent=14, bulletFontName="DVB", bulletFontSize=9))
            out.append(Spacer(1, 3))
        elif kind == "table":
            header, *rows = val
            n = len(header)
            data = [[Paragraph(h, S["cellb"]) for h in header]] + [[Paragraph(c, S["cell"]) for c in r] for r in rows]
            t = Table(data, colWidths=[W / n] * n, repeatRows=1)
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
                ("GRID", (0, 0), (-1, -1), 0.5, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7f9fb")]),
                ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
            out += [t, Spacer(1, 6)]
        elif kind == "space":
            out.append(Spacer(1, val))
    return out


def build(path, title, blocks):
    def footer(c, d):
        c.saveState()
        c.setFont("DV", 7.5)
        c.setFillColor(MUTED)
        c.drawString(18 * mm, 10 * mm, f"Tye · F Rich Consulting dialler pack · {title}")
        c.drawRightString(A4[0] - 18 * mm, 10 * mm, f"Page {d.page}")
        c.restoreState()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                            topMargin=16 * mm, bottomMargin=18 * mm, title=title, author="Tye Morgan")
    doc.build(render(blocks), onFirstPage=footer, onLaterPages=footer)


LOCK_SHOW = [
    ("h2", "Lock in the show (don't hang up until every box is ticked)"),
    ("bullets", [
        "✓ Invite accepted <b>while you're on the phone</b>",
        "✓ Google Meet: app downloaded if they're on their phone",
        "✓ Quiet place, not driving, not at work without privacy, enough time set aside",
        "✓ Partner / decision maker joining if they're involved",
        "✓ Prep video sent and they've agreed to watch it",
    ]),
    ("say", "Can you see the invite? Could you accept it now while I'm on, so the slot's secured? Unconfirmed calls can get cancelled."),
    ("say", "It's on Google Meet. If you're joining on your phone, download the Meet app before so there's no faff."),
    ("say", "I'm sending you a short video from Freeman. Watch it before the call and jot down any questions, so he can focus on your situation rather than the basics."),
    ("say", "Perfect. So that's [day] at [time] on Google Meet. Invite accepted, somewhere quiet, video watched. It's a proper next-step conversation with Freeman, so I want you to get the most out of it."),
]

REMINDERS = [
    ("h2", "After booking: reminder sequence"),
    ("table", [
        ["When", "What to send"],
        ["Straight after the call", "Booking confirmation text + prep video"],
        ["24 hours before", "“Hey [Name], just confirming you're still good for your call with Freeman tomorrow at [time]. Make sure you've watched the video I sent, accepted the invite and you're joining from somewhere quiet.”"],
        ["Morning of", "“Morning [Name], looking forward to your call with Freeman today at [time]. Have you had a chance to watch the video?”"],
        ["1–2 hours before", "“Quick reminder, your call with Freeman is coming up shortly. Make sure you're somewhere quiet and ready to go through your goals properly.”"],
    ]),
    ("tip", "Don't over-contact. Four clean touches is plenty. Log each one in Close."),
]

# ---------------------------------------------------------------- 1. VSL
vsl = [
    ("title", "VSL Leads: Call Script"),
    ("sub", "They watched Freeman's training and applied or booked. Call within <b>5 minutes</b> (15 max). Call length 8–15 minutes. You're not selling: confirm fit, route, prepare, lock in the show."),
    ("h2", "Before you dial (30 seconds)"),
    ("bullets", [
        "Open the lead in Close. Read all 10 form answers, especially Q6 (dream life), Q7 (timeline), Q8 (blocker), Q10 (funding).",
        "Check notes and past calls. Never re-ask something they've already told you. Confirm and dig instead.",
        "Pick your hook: the one thing from their answers you'll open with.",
    ]),
    ("h2", "1. Opener"),
    ("say", "Hi [Name], it's Tye from Freeman's team. I saw you booked a call after watching Freeman's training on building an Airbnb / rent-to-rent business. I just wanted to introduce myself, make sure you're all set for the call, and get to know where you're at a bit. Have I caught you at an OK time?"),
    ("p", "<b>Bad time?</b> “No worries. When's better, later today or tomorrow morning?” Lock a specific time, log it, hang up."),
    ("h2", "2. Rapport (1–2 mins, keep it short)"),
    ("say", "What made you book in?"),
    ("say", "What stood out to you from the training?"),
    ("say", "How long have you been looking into property?"),
    ("h2", "3. Application check (2–4 mins)"),
    ("say", "I've got your application in front of me. I'll just run through a couple of bits so we know the call's the right next step for you."),
    ("p", "Confirm: where they live · job / situation · experience · goal · timeline."),
    ("h2", "4. Money (with tact)"),
    ("say", "You put around [Q10 amount] on the form. Is that sitting there ready, or would you look at a payment plan or credit if it was the right fit?"),
    ("say", "And if Freeman can genuinely help you and it makes sense, is that something you'd be comfortable investing in?"),
    ("p", "If they put <b>“under £5,000”</b>: “Roughly how much, ballpark?” Then route them using the Routing sheet."),
    ("h2", "5. Go one level deeper (this is what makes people show up)"),
    ("say", "You wrote [their Q6 answer]. What does that actually look like for you day to day?"),
    ("say", "Why now? What's changed?"),
    ("say", "What's stopped you starting before?"),
    ("say", "If nothing changed in the next 12 months, how would you feel about that?"),
    ("tip", "Listen more than you talk. If they say “I'm not ready”, “I need to think” or “I don't have enough money”, don't accept it straight away. Find out <b>why</b>."),
    ("h2", "6. Decision maker"),
    ("say", "Is it just you making the decision, or is a partner or family member involved? If they are, it's best they join so you both hear the same thing."),
    ("h2", "7. Position the call"),
    ("say", "Just so you know, it's not a general chat. Freeman looks at your situation, what you want to achieve, and whether he can actually help. If it's a fit, he'll show you exactly how."),
] + LOCK_SHOW + [
    ("h2", "If they don't answer"),
    ("steps", ["Call once", "Leave a voicemail", "Send a text", "Log the attempt in Close", "Set a follow-up task"]),
    ("say", "Voicemail: Hey [Name], it's Tye from Freeman's team. I saw you booked a call and just wanted to confirm the details and send over some prep before your session. I'll drop you a text now."),
    ("say", "Text: Hey [Name], it's Tye from Freeman's team. I saw you booked a call after watching Freeman's training. Just want to quickly confirm it and send over some prep. Let me know when you're free for a quick call."),
] + REMINDERS + [
    ("h2", "Close note after the call"),
    ("p", "Lead source · situation/job · experience · goal · why now · timeline · capital · liquid y/n · payment plan needed y/n · decision maker · main pain · route · video sent/watched · invite accepted y/n · Meet ok y/n · quiet place y/n · rapport notes · next action."),
    ("p", "<b>If it's not in Close, it didn't happen.</b>"),
]

# ---------------------------------------------------------------- 2. Webinar
webinar = [
    ("title", "Webinar Leads: Call Scripts"),
    ("sub", "Three types of webinar lead, three scripts. Work the whole list within <b>3 working days</b> (2–3 calls + a text each)."),
    ("h2", "Order to work them (day after the webinar)"),
    ("steps", ["Booked calls happening today", "Booked calls not yet confirmed", "Booked but not reached after the webinar",
               "Attended but didn't book", "Registered but didn't attend", "Long-term nurture"]),
    ("h2", "A. Booked a call on the webinar"),
    ("p", "Call <b>within 1 hour</b> of the webinar ending. 3–5 minutes. Light touch, not a sales call."),
    ("say", "Hey [Name], it's Tye from Freeman's team. First of all, thanks so much for staying on tonight and booking in. I just wanted to thank you properly and make sure the call's the right next step for you."),
    ("say", "What stood out to you from the webinar?"),
    ("say", "What made you want to book in?"),
    ("h3", "Light application check (2–3 mins)"),
    ("say", "I've got your application here, so I'll just confirm a couple of things so the call's aligned and we're not wasting your time or Freeman's."),
    ("p", "Goal · timeline · money (liquid?) · comfortable investing if it's right · payment plan needed? · decision maker · understands it's a next-step call, not a general chat."),
    ("say", "You mentioned around [X]. Is that ready to go, or would you look at a payment plan if it was the right fit?"),
    ("p", "Then send the prep video and lock in the show (checklist below)."),
    ("h3", "No answer after the webinar"),
    ("say", "Voicemail: Hey [Name], it's Tye from Freeman's team. Saw you booked in after tonight's webinar. Just wanted to confirm your call and send some prep. I'll text you now and try you again tomorrow."),
    ("say", "Text: Hey [Name], it's Tye from Freeman's team. Thanks again for joining the webinar and booking your call. Just want to confirm it and send over some prep. I'll try you again tomorrow, but feel free to reply here."),
    ("h2", "B. Attended but didn't book"),
    ("p", "5–8 minutes. Find out why they didn't book, then only book if they're serious."),
    ("say", "Hey [Name], it's Tye from Freeman's team. I saw you joined Freeman's webinar on [topic], so I just wanted to check in. Did you get value from it?"),
    ("say", "Was there any particular reason you didn't book a call at the end?"),
    ("say", "Was there anything you were unsure about?"),
    ("say", "Are you still keen on getting support with [rent-to-rent / Airbnb]?"),
    ("p", "If yes → light qualify (why, goal, timeline, money, liquid, decision maker) → then:"),
    ("say", "Based on what you've said, a call with Freeman could be really useful. It's to look at your situation and see if he's the right fit. I only want to book it in if you're serious about taking action and happy to watch a short video beforehand. Does that sound fair?"),
    ("h2", "C. Registered but didn't attend"),
    ("say", "Hey [Name], it's Tye from Freeman's team. I saw you registered for Freeman's webinar on [topic], but I'm not sure if you managed to make it live. Did you get a chance to join?"),
    ("p", "If no:"),
    ("say", "No worries at all. You missed a really useful one, he broke down [topic]. I'll send you the training so you can catch up. Are you still interested in how [rent-to-rent / Airbnb] could work for you?"),
    ("p", "If interested → light qualify → book or route (see Routing sheet). If not → YouTube nurture, no pressure."),
] + LOCK_SHOW + REMINDERS + [
    ("h2", "Close note for webinar leads"),
    ("p", "Webinar topic · attended y/n · booked y/n · reason for booking / not booking · goal · timeline · capital · liquid y/n · payment plan needed y/n · decision maker · video sent/watched · confirmed y/n · nurture or DQ reason if applicable."),
]

# ---------------------------------------------------------------- 3. Old / warm / no-show
old = [
    ("title", "No-Shows, Callbacks & Old Leads"),
    ("sub", "Warmer, lower-pressure leads. Good for practice and your follow-up bank. Recovering 40%+ of no-shows is basically free bookings."),
    ("h2", "1. No-show (didn't turn up to Freeman's call)"),
    ("p", "Act <b>immediately</b>: call → text → email if needed."),
    ("say", "Hey [Name], looks like you weren't able to make the call with Freeman. Is everything OK? Let me know if you'd still like to reschedule and I'll see what availability we've got."),
    ("p", "If they pick up:"),
    ("say", "No worries, life happens. Before I rebook you, is this still something you genuinely want to move forward with? Freeman keeps those slots for people who are serious."),
    ("bullets", [
        "Only rebook if they're still qualified. Re-check timeline and money briefly.",
        "Re-confirm commitment, resend the video, lock in the show again.",
        "No reply → status No Show → nurture with a dated follow-up task.",
    ]),
    ("h2", "2. Cold feet before Freeman's call"),
    ("say", "Totally get it. It's normal to have second thoughts before a big step. Can I ask what's changed since you booked?"),
    ("say", "Is it the money, the timing, or not being sure it'll work for you?"),
    ("p", "Dig into the real reason. Remind them of <b>their own why</b> (from notes): “You told me you want [goal] because [reason]. Has that changed?” The call is just to see if it's a fit, with no obligation."),
    ("h2", "3. Callback you agreed"),
    ("say", "Hey [Name], it's Tye from Freeman's team. You said [day/time] was good to pick up where we left off. Still a good time?"),
    ("p", "Start from where you left off. Use your notes: “Last time you mentioned [thing]. Where are you at with that now?”"),
    ("h2", "4. Old leads (webinar sign-ups, old Calendly, never progressed)"),
    ("say", "Hi [Name], it's Tye from Freeman Richards' team. You showed interest in property / Airbnb a while back, so I just wanted to check in. Is it still something you're looking to get into?"),
    ("say", "What's changed since then? Are you in a better position to start now?"),
    ("p", "Then qualify as normal and route. If not now → dated follow-up task (follow-up bank)."),
    ("h2", "5. No reply after 3 days"),
    ("table", [
        ["Day", "What to do"],
        ["Day 1", "Call AM + PM. Text: No Answer #1"],
        ["Day 2", "Call AM + PM. Text: No answer #2"],
        ["Day 3", "Call AM + PM. Text: No Answer #3 (last try)"],
        ["After 6 attempts", "Good lead (fit 6+) → Setter Pipeline. Otherwise → NGMI"],
    ]),
    ("tip", "Setter Pipeline leads get a check-in text after 2 weeks. That's your follow-up bank, next month's bookings."),
]

# ---------------------------------------------------------------- 4. Routing & offer
routing = [
    ("title", "Routing, Offer & Objections Cheat Sheet"),
    ("sub", "Every lead ends in one of four decisions: <b>Book · Route · Nurture · Disqualify</b>. Current offer structure wins over old training prices."),
    ("h2", "Route by budget"),
    ("table", [
        ["Budget available", "Route", "Next step"],
        ["£5k–£7k+", "Airbnb / R2R Mentorship (3-Month or 6-Month Gold)", "Book strategy call with Freeman"],
        ["Already has properties", "Scaling conversation", "Book strategy call with Freeman"],
        ["£2.5k–£5k", "Airbnb Management / Co-hosting (+ R2R guidance)", "Book strategy call with Freeman"],
        ["~£1k–£2.5k", "Deal Sourcing (DIY ~£495–£995 / Done-With-You ~£1,495)", "Deal sourcing call (confirm still active)"],
        ["Under £1k", "Deal Sourcing Blueprint", "Send self-checkout link. No call"],
        ["No budget / just researching", "YouTube nurture", "Send Freeman video. Don't force a call"],
    ]),
    ("h2", "The offers"),
    ("table", [
        ["Product", "Price", "Your commission"],
        ["Airbnb Management / Co-hosting<br/>3 months + basic lifetime support", "£2,500–£3,000", "10% (£250–£300)"],
        ["3-Month Fast Track Mentorship", "£3,000–£5,000", "7% (£210–£350)"],
        ["6-Month Gold Mentorship<br/>includes 90-day guarantee", "£4,000+ (usually £5,000)", "7% (~£350)"],
    ]),
    ("p", "Payment plans: max 3 instalments, always offer 2 first. Commission is on the full price."),
    ("h2", "Green / yellow / red"),
    ("table", [
        ["Green: book", "Yellow: nurture", "Red: disqualify"],
        ["Genuine interest, clear goal, 0–3 month timeline, money available or realistic payment option, decision maker there, will watch the video",
         "6+ months away, funds not ready, still researching, needs to ask someone, better suited to self-study",
         "Booked by accident, no intention, unrealistic, hostile, repeated no contact, no budget + no plan, won't watch prep"],
    ]),
    ("h2", "Airbnb vs deal sourcing in one breath"),
    ("say", "Airbnb / rent-to-rent is where you take on and run your own property, so it needs more startup capital. Deal sourcing is where you find opportunities and package them for investors. It's lower capital, and the skills carry over to getting your own units later."),
    ("h2", "Objections"),
    ("table", [
        ["They say", "You say"],
        ["“How much is it?”", "It depends which route fits. For Airbnb the main thing is having around £5–7k to start the first unit properly. Where are you at budget-wise?"],
        ["“I don't have £5–7k.”", "That's fine. Airbnb might not be the first step then. [£2.5k+ → Management] [£1k+ → deal sourcing]"],
        ["“I've only got about £500.”", "Full support might not be the best fit yet, but the Deal Sourcing Blueprint is a good self-paced start."],
        ["“I need to think about it.”", "Fair. What is it you want to think over: the money, the time, or whether it'll work for you?"],
        ["“I'm not ready.”", "What would ‘ready’ look like for you? Most students start before they feel fully ready."],
        ["“I'll contact you later.”", "No problem. So I'm not chasing you, what day and time works for 10 minutes?"],
        ["“Can you just explain it all now?”", "I can give you the overview, but the right breakdown depends on your goals, budget and timeline. If you're a fit, Freeman goes through it properly."],
        ["“Is it guaranteed?”", "Nothing in property is guaranteed. It depends on the area, the deal, the setup and your effort. The call's there to assess your situation."],
        ["“I've done another programme.”", "Useful to know. What did you learn, and where are you still stuck?"],
        ["“I already have properties.”", "Then it's more of a scaling conversation. What are you trying to improve: units, bookings, systems or profit?"],
        ["“Just browsing.”", "Curious, or something you genuinely want to start soon? (still cold → YouTube)"],
    ]),
    ("h2", "Never say"),
    ("warn", "“You'll make £1,500 a month per property” · “guaranteed property / income” · “passive income” · “you don't need compliance” · “start with no money” · “you can definitely quit your job” · “Freeman will do everything” · “the call's just for info” · “everyone gets a deal from the investor network”."),
    ("p", "<b>Say instead:</b> “target example, not a guarantee” · “depending on the area and deal” · “the call is to assess fit” · “the programme supports you, but you still need to take action”."),
    ("p", "<b>Gold guarantee:</b> “Gold comes with a guarantee Freeman will walk you through on the call.” Never promise a property yourself."),
    ("p", "<b>Profit example (target only):</b> “Some units target around £800–£1,500 a month profit depending on area, demand and setup. No guarantees, which is why Freeman assesses your situation properly.”"),
    ("p", "<b>Visa / immigration:</b> no legal advice. “There may be an option to source under Freeman's company framework, subject to approval, usually with around a 30% operational fee.”"),
]

# ---------------------------------------------------------------- 5. Follow-up texts
texts = [
    ("title", "Follow-Up Texts: Which One, When"),
    ("sub", "All saved in Close as SMS templates. One text per call attempt. Fill every [DAY]/[TIME]. Never message DNC or DQ leads."),
    ("table", [
        ["Situation", "Template in Close", "Then"],
        ["New application, no answer", "Tye — Speed to Lead (New Application)", "No-answer chase"],
        ["No answer, day 1", "No Answer #1", "Call again PM"],
        ["No answer, day 2", "No answer #2", "Call again PM"],
        ["No answer, day 3", "Tye — No Answer #3 (Day 3 last try)", "Setter Pipeline or NGMI"],
        ["Voicemail left", "Tye — Voicemail Left", "As no answer"],
        ["Spoke, call back later", "Tye — Spoke: Callback Confirmed", "Call task at agreed time"],
        ["Booked with Freeman", "Tye — Spoke: Booked With Freeman", "+ Our Reviews same day"],
        ["Day before call", "Booked Call — Upcoming Reminder", "–"],
        ["Morning of call", "Booked Call — Today's Reminder", "–"],
        ["Didn't answer pre-call", "Booked Call — Missed You", "–"],
        ["No-show", "Tye — No Show Rebook", "Call next day"],
        ["“Need to think”", "Tye — Spoke: Thinking About It", "Callback in 2 days"],
        ["Busy with work", "Tye — Spoke: Busy With Work", "Callback in 2–3 days"],
        ["Budget £2.5k–£5k", "Management Pitch", "Callback in 2 days"],
        ["Wants proof", "Our Reviews / Student Review or Case Study", "Callback next day"],
        ["Wants to learn more", "Airbnb Training Asset", "Callback after watching"],
        ["Not interested", "Tye — Not Interested (Door Open)", "NGMI"],
        ["Setter Pipeline, 2 weeks quiet", "Tye — Nurture Check-in (2 weeks)", "–"],
        ["Old webinar sign-ups", "Pipeline Leads", "–"],
    ]),
    ("h2", "Proof links to drop in"),
    ("bullets", [
        "Trustpilot: uk.trustpilot.com/review/freemanrichards.com",
        "Case studies (YouTube): youtube.com/playlist?list=PLGJk2MFJv52gjtVvAfJd8LB1yFOUU2215",
        "Airbnb Management explainer (Loom): loom.com/share/fe5beaf39a5e45aa994919570915949f",
    ]),
    ("tip", "After every call, run <b>/log [name] [outcome] [notes]</b> and Claude picks the right template, fills it in and creates the Close task. You just press send."),
]

# ---------------------------------------------------------------- 6. Handover questions + earnings
handover = [
    ("title", "Questions for the Previous Dialler + Earnings Plan"),
    ("sub", "Ask these in your handover. Money questions first, so you get paid on everything you're owed."),
    ("h2", "Your pay"),
    ("steps", [
        "Do I get commission on every close from a call I booked, or only ones I close myself?",
        "How are Ray and I split if we both worked the lead?",
        "Is commission paid on signing or as each instalment lands? What happens on a refund?",
        "Do I earn on Deal Sourcing, Blueprint or Management sales? At what rate?",
        "What did you earn in a good month, and what did that month look like (bookings, shows, closes)?",
    ]),
    ("h2", "The offer right now"),
    ("steps", [
        "What are the current prices and payment options for each route?",
        "What's the exact wording for Gold's 90-day guarantee, and when can I mention it?",
        "Where do I get the prep video, case studies, Blueprint link and YouTube links?",
        "Which videos actually get watched and lead to shows?",
    ]),
    ("h2", "Leads"),
    ("steps", [
        "Which lead source books and closes best: VSL, webinar, Instagram or Calendly?",
        "How many new applications come in a day, and when do they usually land?",
        "Which old lists are worth working?",
        "What do Setter Pipeline and Closer Follow Up actually mean day to day?",
        "How do new-app claims work with Ray?",
    ]),
    ("h2", "Calls"),
    ("steps", [
        "What are the top 3 objections, and what do you say that actually works?",
        "Why do people no-show, and what fixed it?",
        "What's your show rate and booked-to-close rate?",
        "What's the best time of day to reach people?",
        "What red flags does Freeman hate seeing on his calendar?",
        "Can I listen to 3 of your best calls and 1 bad one?",
    ]),
    ("h2", "Freeman"),
    ("steps", [
        "What does he want in the notes before a call?",
        "What annoys him most: no-shows, weak leads, messy notes?",
        "When is his calendar busiest? Should I leave gaps?",
    ]),
    ("h2", "What Freeman measures you on"),
    ("table", [
        ["KPI", "Target"],
        ["Speed to lead", "Under 15 mins (under 5 = strong)"],
        ["Contact rate", "70%+"],
        ["Qualification accuracy", "85%+"],
        ["Prep video watched", "70%+"],
        ["Appointment confirmation", "90%+"],
        ["Show rate", "80% minimum, 90%+ excellent"],
        ["No-show recovery", "40%+"],
        ["CRM compliance", "100%"],
    ]),
    ("p", "<b>Primary KPI: qualified show rate.</b> Fewer, stronger, prepared prospects beat a full calendar of people who won't show."),
    ("h2", "How to earn more"),
    ("bullets", [
        "<b>Shows are where your money is.</b> A booking that no-shows earns £0. Invite accepted on the phone + video + reminders = pay.",
        "<b>Book fewer, stronger leads.</b> Freeman's close rate is your commission.",
        "<b>Speed to lead.</b> Call within 5 minutes. Answer rates drop fast after that.",
        "<b>Route, don't bin.</b> £2.5–5k → Management = £250–£300 per close.",
        "<b>Win back no-shows.</b> 40% recovery is free bookings.",
        "<b>Build the follow-up bank.</b> Today's “not now” is next month's booking.",
    ]),
    ("h2", "The maths for £2,000 a month"),
    ("table", [
        ["Step", "Number"],
        ["Base", "£500"],
        ["Commission needed", "~£1,500 = 5–6 closes"],
        ["Shows needed (if 1 in 4 buys, a guess: check with the previous dialler)", "~22–24"],
        ["Bookings needed (at 80% show rate)", "~28–30 a month"],
        ["Per working day", "~1.5 bookings"],
    ]),
    ("p", "Replacing Sainsbury's (£700) = just 1 close on top of base."),
]

OUT = "/home/user/Tmt/dialer/pdf"
os.makedirs(OUT, exist_ok=True)
docs = [
    ("1-VSL-Leads-Script.pdf", "VSL Leads", vsl),
    ("2-Webinar-Leads-Script.pdf", "Webinar Leads", webinar),
    ("3-No-Shows-Callbacks-Old-Leads.pdf", "No-Shows, Callbacks & Old Leads", old),
    ("4-Routing-Offer-Objections.pdf", "Routing, Offer & Objections", routing),
    ("5-Follow-Up-Texts.pdf", "Follow-Up Texts", texts),
    ("6-Handover-Questions-Earnings.pdf", "Handover Questions & Earnings", handover),
]
for fn, title, blocks in docs:
    build(os.path.join(OUT, fn), title, blocks)
    print("built", fn)

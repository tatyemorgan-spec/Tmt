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
        "<b>New app just landed?</b> Claim it with a tick in #1-new-apps, then give it a few minutes: many book a call straight after. Check if they've booked before you dial.",
        "<b>Out of hours?</b> Send the acknowledgement text now (“thanks for taking the time to watch, I'll be in touch shortly”) and set a task for 9–10am.",
        "<b>Booked calls come first.</b> They need videos and a fit check before Freeman's slot.",
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
    ("h2", "8. Ready now or window shopping? (most VSL bookings fail here)"),
    ("say", "Once you're on the call with Freeman, if everything makes sense, is this something you're ready to take action on now, or are you more looking for information at this stage?"),
    ("p", "<b>Info only?</b> Don't keep the booking. Protect Freeman's diary:"),
    ("say", "No problem at all. The call with Freeman is very much a strategy call to move forward, so let's pause that booking for now. I'll send you some info first. How long do you need to watch it? Then I'll give you a ring."),
    ("p", "Cancel the booking → opportunity to <b>New Deal Lost</b> (note “cancelled: info only”) → send videos → task to reconnect → qualify before rebooking."),
    ("warn", "Overwhelm them. £7k+ leads: talk <b>rent-to-rent only</b>. Only bring in management if funds are lower or they're nervous about investing. Don't downsell if you don't need to."),
    ("h3", "If they push back: “I've already booked, why all the questions?”"),
    ("say", "Totally get it. Freeman's only one person and can't take everyone's call, so this is just to check the call's the right next step for you and share some info so you get the most out of it."),
] + LOCK_SHOW + [
    ("h2", "If they don't answer (Antoinette's sequence)"),
    ("table", [
        ["Attempt", "Text after the missed call", "Then"],
        ["Out of hours", "Acknowledgement: thanks for watching, I'll be in touch shortly", "Task 9–10am"],
        ["Call 1", "VSL follow-up 1: tried you about your application, quick call to understand your situation and goals and how Freeman can support you. When can I call?", "Task later today / tomorrow"],
        ["Call 2", "VSL follow-up 2: “Have I got the right person?”", "Task next day"],
        ["Call 3", "Last message: I've reached out a few times. No worries if it's not for you, but if you are interested let me know and we'll pick up where we left off.", "Task to check next day"],
        ["No reply", "–", "NGMI (door left open)"],
    ]),
    ("p", "Wrong number? Email them asking for another number."),
    ("say", "Voicemail: Hey [Name], it's Tye from Freeman's team. I saw you booked a call and just wanted to confirm the details and send over some prep before your session. I'll drop you a text now."),
    ("say", "Text: Hey [Name], it's Tye from Freeman's team. I saw you booked a call after watching Freeman's training. Just want to quickly confirm it and send over some prep. Let me know when you're free for a quick call."),
] + REMINDERS + [
    ("h2", "Close note after the call"),
    ("p", "Lead source · situation/job · experience · goal · why now · timeline · capital · liquid y/n · payment plan needed y/n · decision maker · main pain · route · video sent/watched · invite accepted y/n · Meet ok y/n · quiet place y/n · rapport notes · next action."),
    ("p", "<b>If it's not in Close, it didn't happen.</b> WhatsApp chats too: paste them in as a note."),
    ("h2", "Before Freeman's call: “Notes for Freeman”"),
    ("p", "Copy your notes into a <b>new</b> note titled “Notes for Freeman”. Put <b>funds and goals</b> at the top, then add personal rapport bits (e.g. new baby, family in property) and remove your own opinions. Or run <b>/freeman-notes [name]</b>."),
    ("h2", "Close + Airtable after the call"),
    ("table", [
        ["What happened", "Close", "Airtable (CRM tab)"],
        ["Booked (self-booked VSL)", "New Opportunity (automatic)", "Outcome: Qualified in progress"],
        ["You booked them", "Lead → New Opportunity + add opportunity with call date", "Outcome: Qualified in progress, Host set"],
        ["Cancelled / no-show", "Lead → Setter Pipeline (or NGMI), opp → New Deal Lost + note, task ~2 weeks", "Outcome: Cancelled / No-show + note"],
        ["Closed", "Opp → Signed Up / Deposit Paid", "Closed won, date, Revenue (incl VAT), Cash collected (ex VAT)"],
    ]),
]

# ---------------------------------------------------------------- 2. Webinar
webinar = [
    ("title", "Webinar Leads: Call Scripts"),
    ("sub", "Three types of webinar lead, three scripts. Work the whole list within <b>3 working days</b> (2–3 calls + a text each)."),
    ("h2", "Order to work them (day after the webinar)"),
    ("steps", ["Booked calls happening today", "Booked calls not yet confirmed", "Booked but not reached after the webinar",
               "Attended but didn't book", "Registered but didn't attend", "Long-term nurture"]),
    ("h2", "A. Booked a call on the webinar: they book with YOU"),
    ("p", "Webinar bookings are a <b>discovery video call with you</b> (not Freeman). Watch the webinar yourself, because Freeman sometimes changes the pitch. These are your best leads: they sat through 2 hours and know they need £6–8k."),
    ("h3", "Straight after the webinar: quick thank-you call"),
    ("say", "Hey [Name], it's Tye from Freeman's team. Thanks so much for staying on tonight and booking in. I just wanted to say thank you properly. I'll see you on our call on [day]."),
    ("p", "No answer → acknowledgement text: thank you for joining the webinar and booking a call, I'll be in touch soon."),
    ("h3", "Day of your discovery call"),
    ("p", "Reminder text with the video link. Laptop is fine. On a phone they need the Google Meet app."),
    ("h3", "The discovery video call (20–30 mins, camera on)"),
    ("say", "Hi [Name]! Could you pop your camera on? I like to see who I'm talking to."),
    ("say", "What did you think of the webinar? What was your biggest takeaway?"),
    ("say", "What's got you interested in property, and why now?"),
    ("p", "Then the same qualification as VSL: location · work · experience · goal (go deeper) · pain points · funds + liquid · decision maker · “ready to take action if it makes sense, or window shopping?”. Title your note “Discovery video call notes”. Don't record these calls."),
    ("h3", "Qualified → book with Freeman"),
    ("bullets", [
        "Lead → New Opportunity <b>and add an opportunity</b> with the call date.",
        "If his call is days away, check in every 2–3 days: Trustpilot, testimonials, “are you getting excited?”. E.g. call on Monday → message Friday with videos for the weekend → Monday morning check.",
        "Before his call: “Notes for Freeman” note.",
        "After a sale: congratulate on WhatsApp + task a few days before the next instalment.",
    ]),
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
    ("sub", "Antoinette's proven texts, saved in Close in your name. Fill every [DAY] / [TIME] / [LINK] before sending. Never message DNC or DQ leads."),
    ("h2", "VSL leads"),
    ("table", [
        ["Situation", "Template in Close"],
        ["New app, can't call now", "Tye — Acknowledgement: New App"],
        ["New app + booked a call", "Tye — Acknowledgement: Booked Call"],
        ["Missed call 1", "Tye — VSL Follow Up 1"],
        ["Missed call 2", "Tye — VSL Follow Up 2 (“right person?”)"],
        ["Missed call 3 → then NGMI", "Tye — VSL Follow Up 3 (last try)"],
        ["Booked themselves, need to chat first", "Tye — Booked Call: Quick Chat First"],
        ["Booked, still can't reach", "Tye — Booked Call: Still Trying"],
        ["Booked, ignoring calls + texts", "Tye — Booked Call: Not Answering (Slot Warning)"],
        ["Still nothing → cancel the slot", "Tye — Cancelling Call (Couldn't Reach)"],
        ["Spoke, sending videos (£7k+)", "Tye — Videos: Airbnb Only"],
        ["Spoke, sending videos (lower funds)", "Tye — Videos: Airbnb + Management"],
        ["Missed call after sending videos", "Tye — Check In After Videos"],
        ["Booked, chasing after videos", "Tye — Booked Call: Chase After Videos"],
    ]),
    ("h2", "Booked with Freeman"),
    ("table", [
        ["When", "Template in Close"],
        ["Straight after you book them", "Tye — Booked: Call Confirmation"],
        ["Day before", "Tye — Reminder: Call Tomorrow"],
        ["Morning of", "Tye — Reminder: Call Today"],
        ["A few minutes before", "Tye — Reminder: Few Minutes"],
        ["No-show", "Tye — No Show Rebook"],
    ]),
    ("h2", "Webinar leads"),
    ("table", [
        ["When", "Template in Close"],
        ["They booked your discovery call", "Tye — Webinar: Discovery Call Booked"],
        ["Morning of your discovery call", "Tye — Webinar: Discovery Call Today"],
        ["Never reached", "Tye — Webinar: No Contact (YouTube)"],
    ]),
    ("h2", "After the sale + extras"),
    ("table", [
        ["When", "Template in Close"],
        ["Instalment due, no answer", "Tye — Instalment Check-in"],
        ["Wants proof", "Our Reviews / Student Review or Case Study"],
        ["Needs time to think / busy", "Tye — Spoke: Thinking About It / Busy With Work"],
        ["Not interested", "Tye — Not Interested (Door Open)"],
        ["Disqualified", "Email: Tye — DQ: Thank You + YouTube"],
        ["Setter Pipeline, 2 weeks quiet", "Tye — Nurture Check-in (2 weeks)"],
    ]),
    ("tip", "Automation: enrol a missed VSL lead in <b>Tye — VSL No Answer (Antoinette rhythm)</b>. It sends Follow Ups 1–3 around your calls and stops the moment they reply."),
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

training = [
    ("title", "Antoinette's Training: How the Job Really Runs"),
    ("sub", "From the 25 Sep handover call with the previous dialler. Where this differs from the SOPs, follow this."),
    ("h2", "The 10 things that matter most"),
    ("steps", [
        "<b>Speed to lead, even out of hours.</b> Acknowledgement text straight away, task for 9–10am. Other mentors are hitting their feeds too.",
        "<b>Wait a few minutes</b> after a new app. Many then book a call, and it merges into the same lead.",
        "<b>Booked calls are urgent.</b> Videos out + fit check before Freeman's slot.",
        "<b>Most VSL bookings are info-seekers.</b> Ask “ready to take action, or looking for info?”. Cancel if info only, educate, then rebook.",
        "<b>Don't overwhelm.</b> £7k+ → rent-to-rent only. Management for lower funds / nervous investors.",
        "<b>Webinar leads are the best</b> and they book a discovery call with you first.",
        "<b>Go deeper on pain.</b> “What would that mean for you?” Anchor back to it when cold feet hit.",
        "<b>Don't over-remind.</b> Morning text + one call + 15-min heads-up. People have complained about being chased.",
        "<b>Notes for Freeman</b> before every call. Funds + goals on top, plus personal rapport bits.",
        "<b>Close + Airtable always up to date.</b> Freeman tracks cancellations in Airtable.",
    ]),
    ("h2", "Objections her way"),
    ("table", [
        ["They say", "You say"],
        ["12-hour shifts / no time", "Share Amara's video: full 12-hour shifts, still does it part-time. About 3–5 hours a week is enough."],
        ["Not enough money", "Don't give up on the dream, save up, this business can break even quickly. ~£3k → management."],
        ["“Already booked, why the questions?”", "Freeman's one person and can't take everyone's call. This checks it's the right next step and gets you prepared."],
        ["“Booked with another mentor”", "Jump on a call with Freeman too so you can compare like for like. (She won one this way.)"],
        ["80% sure", "Anchor to their pain points. Tell Freeman they're 80%, not 100%."],
    ]),
    ("h2", "Watch out for"),
    ("bullets", [
        "Under £5k applicants sometimes have more (family money). Don't write them off.",
        "Leads often ghost <b>after</b> watching the videos, once they see the work involved. Follow up 3 times, last message leaves the door open, then NGMI.",
        "Don't let Setter Pipeline fill up with hundreds of dead leads (check with Freeman whether he wants NGMI sooner).",
        "Close tasks sometimes disappear. Double-check your list.",
        "Merge duplicate leads (same email/phone), but note if the funding answers changed.",
        "VSL lead flow is lumpy: 0–5 a day, often overnight. Plan your day around follow-up tasks.",
    ]),
    ("h2", "Still to sort"),
    ("table", [
        ["Item", "Who"],
        ["Accept the Airtable invite + tell Antoinette", "You"],
        ["Get added as Host in Airtable", "Marketing team"],
        ["Her SMS templates + instalment spreadsheets", "Antoinette"],
        ["Good / bad calls to review together", "Antoinette"],
        ["Can we sell deal sourcing again?", "Freeman"],
        ["£7k+ VSL leads: rent-to-rent only, or mention management too?", "Freeman"],
        ["Setter Pipeline vs NGMI after 3 failed contacts?", "Freeman"],
    ]),
]

links = [
    ("title", "Links: Calendars, Videos & Proof"),
    ("sub", "From Antoinette's links doc. Match the testimonial to the lead. Examples, not guarantees."),
    ("h2", "Videos to send"),
    ("table", [
        ["Video", "When", "Link"],
        ["How to Start an Airbnb in 2026 (34 min)", "Main prep / nurture", "youtu.be/yPR2TeyNx7Y"],
        ["Airbnb Management Accelerator (Loom)", "Lower funds / nervous", "loom.com/share/fe5beaf39a5e45aa994919570915949f"],
        ["Deal sourcing (YouTube)", "Deal sourcing leads (check still sold)", "youtube.com/watch?v=i9MvFzIni9k"],
        ["Deal Sourcing Blueprint & Guide", "Under £1k", "drive.google.com/file/d/1WutyA52DFpBr-Y9_plSX3nXmoogopwfd/view"],
    ]),
    ("h2", "Testimonials: match the story to the lead"),
    ("table", [
        ["Lead is…", "Send", "Link"],
        ["Worried about time / shifts", "Amara: 12-hour shifts", "youtube.com/watch?v=muBhcvK1z68"],
        ["Young / starting from nothing", "19-year-old, £1k/month", "youtube.com/watch?v=3Y_Sg4-A-MA"],
        ["Doubts it works fast", "1st booking in 24 hrs", "youtube.com/watch?v=hIcU0i0kS3M"],
        ["Wants speed", "2 Airbnbs in 30 days", "youtube.com/watch?v=2TUM34M6mRM"],
        ["London-based", "£2k–£5k profit, one London Airbnb", "youtube.com/watch?v=j7naAr2w0IA"],
        ["Couple deciding together", "Couple's £1k/month London deal", "youtube.com/watch?v=h2uPrO6SEOo"],
        ["General", "Megan", "youtube.com/watch?v=7fHjsy1TZlw"],
        ["Bigger ambitions", "BRRR: deal sourcing, £13k → £330k", "youtube.com/watch?v=I7eWNB7PEkY"],
        ["Wants lots of proof", "All testimonials (playlist)", "youtube.com/playlist?list=PLGJk2MFJv52gjtVvAfJd8LB1yFOUU2215"],
    ]),
    ("h2", "“Is this legit?”"),
    ("bullets", [
        "Trustpilot: uk.trustpilot.com/review/freemanrichards.com",
        "Companies House, mentorship company: company 16359356",
        "Companies House, property company: company 13594162",
        "“We have an office but we're remote, and the education is mainly remote too. Freeman personally meets his mentees at their properties.”",
    ]),
    ("h2", "Community + socials"),
    ("bullets", [
        "Skool: skool.com/freemans-property-academy-8462",
        "YouTube: @FreemanRichards · Instagram / TikTok: @freeman_richards",
        "Website: freeman.propertywealthacademy.co.uk",
    ]),
    ("tip", "Close texts that already include links: <b>Tye — Proof: Amara</b>, <b>Tye — Proof: Is It Legit</b>, <b>Tye — Videos: Airbnb Only / + Management</b>."),
]

daily = [
    ("title", "Daily Workflow & How to Structure Your Chats"),
    ("sub", "From Antoinette's notes and model calls. Her rules: check tasks + new VSL leads first · new leads and booked calls first · <b>tasks cleared every day</b>."),
    ("h2", "Your day"),
    ("table", [
        ["When", "What"],
        ["Before 9am (15 min)", "Slack #1-new-apps → claim it (tick) → <b>Acknowledgement</b> text to overnight apps + task for 9am · check today's tasks · Freeman's calls today: confirmed? videos watched? Notes for Freeman? · /queue"],
        ["9:00–10:30", "<b>Speed to lead:</b> new VSL leads not contacted yet. Booked calls / New Opportunities first. Morning check-in for anyone on Freeman's calendar today."],
        ["10:30–12:30", "Qualify booked leads → videos → confirm or cancel. Timed tasks. /freeman-notes for today + tomorrow."],
        ["Midday (30 min)", "Admin: notes, statuses, opportunities (booked = opp with date, no-show = New Deal Lost), Airtable rows."],
        ["13:00–16:00", "Untimed tasks: New Opps → VSL FU1/2/3 → “watched the videos?” → under £5k → webinar → no-shows → nurture."],
        ["Around Freeman's calls", "15 min before: Few Minutes reminder. After: showed? No-show → Rebook text + call, New Deal Lost, Setter Pipeline, task in 2 weeks."],
        ["17:00–19:00", "Second attempts: 9–5 workers answer now. Webinar discovery video calls."],
        ["End of day", "<b>Every task cleared</b> (done or rescheduled). /eod. Send tomorrow's “call tomorrow” reminders."],
    ]),
    ("tip", "At uni or work? Keep #1-new-apps notifications on. Can't call → Acknowledgement text within minutes + task for your next free slot."),
    ("p", "<b>Weekly:</b> Friday → videos to Monday's bookings for the weekend, then /weekly. Booked a week+ out → a touchpoint every 2–3 days."),
    ("h2", "The call: a conversation, not a questionnaire"),
    ("table", [
        ["Stage", "Easy way in"],
        ["Open it up", "“I just wanted to get a better idea of where you're at, what's got you interested in property and why now.” Then listen."],
        ["Their story", "“How long have you been looking into it? Done any courses or webinars?” “What do you do for work?”"],
        ["Goal + pain", "“What would that actually mean for you?” Write their words down."],
        ["Money", "“You put [X] on the form. Ready to go, or would you look at a payment plan?”"],
        ["Who decides", "“Is this just you, or is someone doing it with you?”"],
        ["Ready?", "“If it makes sense on the call with Freeman, ready to act now or looking for info?”"],
        ["Route + next step", "£5k+ → rent-to-rent only. £3–5k / nervous → Management. Book + confirm, or videos + a callback day."],
    ]),
    ("h2", "The note: Antoinette's format"),
    ("bullets", [
        "Headline (e.g. “Great convo”)",
        "Age / family · how long researching · other webinars or mentors (paid or free)",
        "Why they want mentorship",
        "Based · Work (job, hours) · career goal",
        "<b>Goals: their words</b>",
        "<b>Funds: £ + liquid / credit</b>",
        "Decision maker (alone / partner / friend + name)",
        "Knows about R2R / Management · Next step",
    ]),
    ("say", "Example (Lurelle, closed): 27, single mum, 7-yr-old daughter · researching ~1 yr, free webinars incl. Samuel Leeds · Based East London · Law grad, probation prosecutor, WFH · <b>Goals: financial stability, choices, better life for her and her daughter</b> · <b>Funds: ~£5k liquid + credit</b> · doing it with friend Nathaniel · only knew R2R, also discussed Management"),
    ("h2", "Texts"),
    ("bullets", [
        "First name, say who you are, one ask per message. Trim Antoinette's longer templates for quick back-and-forths.",
        "One text per call attempt. No double-texting.",
        "Paste WhatsApp chats into Close as a note.",
        "DQ → status DQ → <b>Tye — DQ: Thank You + YouTube</b> email.",
    ]),
    ("h2", "Model calls to listen to (in Close)"),
    ("bullets", [
        "<b>Lurelle Edwin</b> (14 min, closed): every qualifier gathered through casual chat.",
        "<b>Tolulope Saseyi</b> (9 min): £3k → Management, videos sent, callback Friday.",
    ]),
    ("h2", "Handed over to you"),
    ("p", "<b>Chante Hemans:</b> hot lead, keen, researching lots. Waiting on voluntary severance pay. Discussed R2R + shown Management video. Follow up around <b>11 Oct</b>."),
]

flow = [
    ("title", "VSL Call Script: Freeman's Way"),
    ("sub", "Tye's version of Freeman's role-plays (29 Sep + 8 Oct). <b>Only PIFs. Move forward, minimal back and forth. You're their best friend through the process.</b> Freeman should never have to educate someone on his call."),
    ("h2", "Before you dial"),
    ("bullets", [
        "Read all 10 answers: funds (the X–Y range) · timeline · blocker · dream · work.",
        "Freeman's calendar open, 2 slots in mind.",
        "Which funnel? <b>ASA2 = rent-to-rent</b> (under £5k: Management via the 2-in-1). <b>ATA1 = Management only.</b>",
        "Pick the testimonial that matches them, ready for the end.",
        "<b>Stand up. Energy up, and keep it up to the last line.</b>",
    ]),
    ("h2", "1. Open"),
    ("say", "Hi [Name], it's Tye from Freeman Richards' team. You made an application about starting your Airbnb business. Have I got the right person? Got five minutes?"),
    ("warn", "Say “rent-to-rent”, “management” or “serviced accommodation” in the opener. Fresh leads won't remember the jargon."),
    ("h2", "2. Frame it"),
    ("say", "Have you got five minutes? I want to make sure this is a good fit for you, and explain a bit about how we could support you."),
    ("h2", "3. The video"),
    ("say", "Thank you for filling out the application first of all. Alongside that there was a video to watch. Did you manage to watch it through, so you've got a basic understanding of what the business model looks like?"),
    ("h2", "4. The model"),
    ("say", "So rent-to-rent: you take a property from a landlord, then let it out night by night on Airbnb. All make sense?"),
    ("p", "Never say “VSL”. Need more? Use <b>Explaining the model</b> below."),
    ("h2", "5. How long + the hold-up"),
    ("say", "So how long have you been looking to get started in property? Just started researching, been interested for a while, or already started?"),
    ("say", "What's been the hold-up? (New to it: Why now?)"),
    ("h2", "6. Work"),
    ("say", "If you don't mind me asking, what do you do for work? How long have you been doing that? What are the shifts like, 8, 10, 12 hours? Is that something you see yourself doing long term?"),
    ("p", "Dig into the pain. Without the job you can't feel the pain, and without the pain the goal is just a number."),
    ("h2", "7. Goals"),
    ("say", "What are you looking to achieve out of this?"),
    ("p", "Write their words down. You'll use them at booking, the check-in and on objections."),
    ("h2", "8. Location"),
    ("say", "Whereabouts are you based?"),
    ("p", "Rapport (“we've helped someone near there”) + <b>Scotland doesn't work for rent-to-rent.</b>"),
    ("h2", "9. Who's involved"),
    ("say", "Are you doing this alone, or with a life partner or business partner?"),
    ("p", "<b>Alone:</b> “So you'd be making the final decision yourself?”"),
    ("say", "Partner: How serious is that conversation? Is it more that you'd go all in with or without them, or very much something you'd do together? Are they aware of this application, or have you done this on your own?"),
    ("h2", "10. Money: soft, not a bank manager"),
    ("p", "Finance is sensitive, and a lot of leads are sceptical of strangers on the phone. Keep it light and use the form."),
    ("say", "I can see on the form you've put about [X–Y] aside. Is that just sitting in your bank doing nothing right now?"),
    ("p", "Playful. They'll usually laugh and say yes."),
    ("say", "Are you closer to [X] or [Y]?"),
    ("h3", "Bring in credit"),
    ("say", "Freeman always recommends being creative with cash flow, so you're not putting all your hard cash in. Do you have access to any credit, like a credit card with an extra £1–2k on it?"),
    ("say", "So about [£cash] in cash plus [£credit] in credit. That's roughly [£total] in total you're prepared to invest. Have I got that right?"),
    ("p", "Said they can “raise” it? Ask what that means: savings, credit, family?"),
    ("h3", "If they push back on credit"),
    ("table", [
        ["They say", "You say"],
        ["“I don't want to pay credit card interest”", "“Totally fair, nobody wants to be paying interest. It's not about borrowing for the whole thing. It's a buffer for the set-up bits, so your cash goes on what matters. Freeman will go through the numbers with you on the call.”"],
        ["“I don't like debt”", "“Respect that. Then we work with the [£X] you've got. That's exactly why the Management route exists: you don't pay the rent, bills or set-up.”"],
        ["“I don't have any credit”", "“No problem at all. Let's work with the [£X]. Is that all savings, or is anything else tied up, like family helping out?”"],
        ["“Is it worth it with the interest?”", "“Good question to ask, and it's the right one for Freeman. He'll show you the numbers for your situation so you can decide. What I need to know now is what you're comfortable putting in.”"],
    ]),
    ("say", "So just to confirm, you've got [£X] that you're comfortable investing?"),
    ("warn", "Mention payment plans. That's Freeman's card to play on his call."),
    ("h2", "11. Why now"),
    ("say", "Now, just out of curiosity, why did you apply? Why now?"),
    ("h2", "12. Book"),
    ("say", "I think you'd be a great fit for the programme. Your characteristics, you're more than qualified, and I'm sure Freeman will take a really good liking to you. I've got his calendar in front of me, and he does have some availability this week for you. When works?"),
    ("p", "Fit it round their life → <b>pencil the slot in Freeman's calendar</b> (remove it if it falls through)."),
    ("h2", "13. Position the call"),
    ("say", "I really want to make sure this call with Freeman is the best use of your time, and that you have all the information to make a decision. Because the call isn't a consultation, it's not a chit-chat. It's the next step."),
    ("h2", "14. The video + “one rule”"),
    ("say", "So I've got a free training video that gives you a real insight into the Airbnb business: how you can start profiting, and how Freeman can help you. Does that sound like something that'll help you make that decision and actually take the next step?"),
    ("say", "One rule though. Before you get on that call with Freeman, I want to make sure you've watched that video. It's about 25 minutes. When do you think you could give it a watch?"),
    ("h2", "15. Book the check-in"),
    ("say", "OK, great. So let's say [time]. I'm going to give you a call, and a bit of homework, haha, to make sure you understand the video. I'll ask a few questions and make sure you're the right fit. You might say “this isn't for me”, or “this is the right fit, I love the business model”. How does that sound?"),
    ("p", "Check-in <b>outside work hours</b> (not their lunch break)."),
    ("h2", "16. Confirm the call"),
    ("p", "“I'll book that in now.” Confirm date, time and link: <b>Google Meet</b>. On a phone, download the Meet app. On a laptop, click the link in the email."),
    ("h2", "17. Tease the proof"),
    ("say", "Actually, I'll do you one better. I'll also send you [testimonial that fits them] so you can see their results. Sound good? Great, I'll reach out at [time]."),

    ("h2", "Explaining the model (when they need more than one line)"),
    ("p", "Keep checking in (“does that make sense so far?”). Don't lecture."),
    ("h3", "Rent-to-rent"),
    ("say", "There are two different ways to get into this. Rent-to-rent needs about £6–8k. That covers all your set-up costs, with the mentorship included. When I say set-up costs, I mean signing the lease with the landlord: first month's rent, deposit, furnishing, and any minor maintenance you do yourself. Then you let it out night by night on Airbnb, and you keep the difference between the landlord's rent and what you bring in on Airbnb. Does that make sense so far?"),
    ("h3", "Be honest about the risk, then bring in Freeman"),
    ("say", "That's the model where you earn the most. But if you've got no idea, it can be a lot of stress, because you've got that rent to pay every month. You need to know how to keep it full, make a profit, scale. That's where the mentorship comes in. He teaches you the right proposal, the right wording and pitch for landlords, and how to get landlords coming to you instead of you going to them."),
    ("h3", "Management: Freeman's simple breakdown (8 Oct)"),
    ("p", "Most people don't watch the full video (it's an emotional video, not an education one), so educate as you sell. Three beats, check in after each."),
    ("say", "1. The traditional way of running an Airbnb is you pay the landlord a fixed rent and you're responsible for the bills. Say guests pay you £4,000 in a month, and rent and bills are £2,000. The £2,000 difference is your profit. Make sense?"),
    ("say", "2. With management, you go into partnership with the landlord instead. You don't pay the rent, the bills or the set-up. You still run it on Airbnb, and you take a percentage of what it makes."),
    ("say", "3. So it's all the perks of Airbnb without being financially responsible for the property. You learn exactly the same skills, and when you're ready you can move into rent-to-rent with the profit. Does that make sense?"),
    ("h3", "Why would a landlord say yes?"),
    ("say", "Because they get a professionally run property and usually more than a normal let, without doing any of the work. Freeman gives you the pitch and the proposal to take to them."),
    ("h3", "The 2-in-1 (ASA2 leads under £5k)"),
    ("say", "Right now I'd be doing you a disservice getting you started in rent-to-rent, where you're financially responsible for everything. Management gets you all the perks of Airbnb without that. And in the mentorship Freeman teaches you both anyway. How does that sound?"),
    ("table", [
        ["Funnel / funds", "Route"],
        ["ASA2, £7k+", "Rent-to-rent only. Never mention Management"],
        ["ASA2, £5–7k", "Rent-to-rent. Management only if they're nervous about the lease"],
        ["ASA2, under £5k", "Management via the 2-in-1"],
        ["ATA1, any funds", "Management only. Under-funded: be more direct"],
        ["Scotland", "Management only"],
        ["Under ~£2.5k", "See ICP routing (Deal Sourcing / Blueprint / YouTube)"],
    ]),
    ("h3", "Send ONE asset"),
    ("p", "Only the video for the route you're leading with. Two videos is 30–40 minutes and confuses people. Then: call back same day (“How did you find it? Why do you think it's a good fit?”) → a relatable student story (Amara, Victoria) → Trustpilot → Megan's number (Hail Mary only)."),

    ("h2", "Objection handling: Freeman's way (challenge, don't fold)"),
    ("steps", [
        "<b>Never accept the first answer.</b> “I need to think about it” is a cover. Find the real reason.",
        "<b>Question, don't argue.</b> Challenge with a question, then shut up.",
        "<b>Use their own words.</b> Their goal, pain and “why now” from earlier.",
        "<b>Isolate it.</b> “Apart from [X], anything else stopping you?” No? Solve X and book.",
        "<b>Always move forward.</b> End with a booked slot, a booked check-in, or a clear no. Never “I'll get back to you”.",
        "<b>Challenge with respect.</b> “Can I be honest with you?” Genuine no (no funds, Scotland + R2R only, not UK)? Let them go nicely: DQ + YouTube.",
    ]),
    ("p", "<b>First call</b>"),
    ("table", [
        ["They say", "You say"],
        ["“I need to think about it”", "“What is it you want to think over? The money, the time, or whether it'll work?” Vague? “Can I be honest? You've been looking at this for [a year] and want [goal]. What'll be different after you've thought about it? Freeman's call is where you get those answers. Let's pencil it in.”"],
        ["“I need to speak to my partner”", "“Love that. Are they aware you've applied? Let's get them on the call with Freeman so they hear it first-hand. What time works for you both?” → WhatsApp group. “Even if they weren't keen, would you still do it?”"],
        ["“I haven't got the money”", "“You put [X–Y] on the form. Has that changed?” → credit card for set-up → still short of R2R? Route to Management. “If money's the only thing, anything else stopping you?” <b>Never a payment plan or discount.</b>"],
        ["“How much is it?”", "“Depends which route fits, and that's what Freeman works out with you. What I need to know is you've got the [£X] to get set up. Still right?” Don't quote prices."],
        ["“I haven't got time”", "“Most of Freeman's people work full-time. Could you give it 3–5 hours a week?” “You said [goal]. If nothing changes, where are you in a year?” Shift workers: Amara."],
        ["“Maybe in a few months”", "“What'll be different then?” Real reason (visa, health, move)? Date + task. Vague? “Can I be honest? In three months you'll be in the same spot, just three months later.”"],
        ["“Just send me info”", "“I'll send the video. But info isn't the problem. You've done the research. Freeman's call is the next step. Let's get it in the diary.”"],
        ["“Is this legit / a scam?”", "“Good question. Don't take my word for it: Trustpilot and student stories coming now. Freeman runs Airbnbs himself, and you can ask him anything on the call. Can I book you in while I send them?”"],
        ["“I'll learn it on YouTube”", "“How long have you been watching? What's it got you so far? The difference is someone checking your deals and contracts before you sign a lease. That's where people lose money.”"],
        ["“Done a course before”", "“What did you learn, and where did it fall down? So you're missing [gap]. A course gives you info. Freeman holds your hand doing it.”"],
        ["“Booked another mentor”", "“Smart. Before you decide, jump on with Freeman too so you can compare like for like.”"],
        ["“R2R's risky / winter?”", "“Right question. That's why you don't do it without a mentor: the right area, pricing, year-round guests (contractors, NHS, families).” Still nervous? Management."],
        ["“Landlords won't say yes”", "“Until they see the numbers. They get their rent, or more, and someone looking after their place. Freeman gives you the proposal and pitch, and gets landlords coming to you.”"],
        ["“I'd rather own first”", "“Owning ties up a mortgage deposit and stamp duty. R2R gets you earning now. Buy later with the profit.”"],
    ]),
    ("h3", "The check-in (after the video)"),
    ("table", [
        ["They say", "You say"],
        ["“Haven't watched it yet”", "“No stress. Remember the one rule? When can you sit down with it today?” Rebook the check-in. Still not watched by call day? Move Freeman's call."],
        ["“Not sure it's for me”", "“Appreciate the honesty. What part made you unsure?” Answer it, route it, or a polite no."],
        ["Gone cold / 80% there", "“When we spoke you said [goal]. Has that changed?” Flag ~80% to Freeman in the Notes for Freeman."],
    ]),
    ("warn", "Say: guaranteed income, passive income, start with no money, quit your job, Freeman does it all, or “the call is just for info”."),

    ("h2", "The check-in call"),
    ("say", "How'd you find the video? What did you like about the business model? About Freeman? Why do you think he's a good fit? So how excited are you for [the day]?"),
    ("say", "Here's [client], who reminds me of you: same position this time last year, a job they didn't like, long hours. They made the change. I want that to be you."),
    ("p", "Partner on the call? Check: “Even without them, is this something you'd do?” and “When you start seeing results, what do you think they'll say?”"),
    ("h2", "Freeman's fixes from your first run"),
    ("table", [
        ["Don't", "Do"],
        ["Say “VSL”", "“the video on the page”"],
        ["Skip checking they watched", "Steps 3–4 every call"],
        ["Slow to get to money", "“I can see on the form you put X…”"],
        ["Offer payment plans", "Never. Freeman's card"],
        ["Full sentences, robotic", "Short, casual, react to them"],
        ["Energy fades", "Keep it up to the end"],
        ["Check in on their lunch", "After work / free time"],
        ["No dates", "Provisional slot on the first call"],
        ["Forget location", "Always ask (Scotland!)"],
        ["Same style for all", "Basic and warm with an auntie, “bro” with a young guy"],
    ]),
    ("h2", "After the call"),
    ("steps", ["Pencil Freeman's calendar", "WhatsApp group with the partner + send video and testimonial", "Close task: check-in at the agreed time", "Close note → /log", "Airtable row"]),
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
    ("7-Antoinette-Training-Notes.pdf", "Antoinette's Training", training),
    ("8-Links-Calendars-Proof.pdf", "Links", links),
    ("9-Daily-Workflow-Chat-Structure.pdf", "Daily Workflow", daily),
    ("10-VSL-Call-Script-Freeman.pdf", "VSL Call Script (Freeman)", flow),
]
for fn, title, blocks in docs:
    build(os.path.join(OUT, fn), title, blocks)
    print("built", fn)

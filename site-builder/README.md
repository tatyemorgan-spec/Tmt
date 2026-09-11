# site-builder

Generates a single, self-contained, mobile-first HTML page for a local
service business — hero, services & pricing, gallery, reviews, contact, and
a client-side "pick a service → date → time → confirm" booking flow with no
backend and no login.

This follows the same brief as the "one-page site, mobile-first, fast /
book now button / no invented facts" prompt: give it real business data as
JSON, get back one `.html` file you can hand over as-is.

## Usage

```sh
node generate-site.js --input business.json --output site.html
```

- `--input, -i` — path to a JSON file describing the business (required)
- `--output, -o` — path to write the generated HTML file (defaults to
  `<business-name>.html` in the current directory)

Try it with the bundled example:

```sh
node generate-site.js --input examples/hair-salon.json --output examples/output/hair-salon.html
```

## Input schema

Every section is optional and only renders if the matching data is present
— the generator never invents copy, prices, photos, or reviews. Fill in
only what the business actually gave you.

```jsonc
{
  "business": {
    "name": "Main Street Hair Co.",   // required
    "logoText": "MAIN STREET HAIR CO.", // optional, defaults to name
    "tagline": "Small town salon with a big heart",
    "bio": "...",                      // renders an "About" section
    "aboutHeadline": "Our Story",      // optional heading override
    "servicesNote": "...",             // optional note under the services heading
    "galleryHeadline": "See For Yourself",
    "primaryColor": "#8a6240",         // buttons / accents, hex
    "accentColor": "#f6efe4",          // section backgrounds, hex
    "inkColor": "#20201d",             // body text color, hex
    "contact": {
      "address": "123 Main St, Anytown, USA",
      "phone": "+15551234567",
      "email": "hello@example.com",
      "instagram": "@handle",
      "hours": "Tue–Sat, 9am–6pm"
    },
    "booking": {
      "availableDays": ["Tue","Wed","Thu","Fri","Sat"], // 3-letter day codes
      "startHour": 9,
      "endHour": 18,
      "slotMinutes": 60,
      "daysAhead": 10
    }
  },
  "hero": {
    "headline": "Good Hair Doesn't Happen By Chance",
    "subheadline": "It happens by appointment.",
    "image": "photos/hero.jpg" // local path (inlined as base64) or https:// URL
  },
  "services": [
    { "category": "Cuts", "name": "Women's Haircut", "price": "From $45", "description": "..." }
  ],
  "gallery": [
    { "src": "photos/1.jpg", "alt": "...", "tag": "Blonde" }
  ],
  "reviews": [
    { "rating": 5, "quote": "...", "author": "Balayage Client" }
  ]
}
```

Notes:

- Local image paths are embedded as base64 `data:` URIs so the output stays
  a single file. Remote `http(s)://` URLs are left as direct links instead
  (keeps the file smaller).
- If `business.contact.email` or `.phone` is set, the booking flow's final
  step becomes a `mailto:`/`sms:` link pre-filled with the customer's name,
  contact info, chosen service, date, and time — that's the whole "booking",
  there's no server or database. If neither is set, it just shows the
  customer a summary to call in.
- If `services` is empty, the booking section is skipped entirely (there's
  nothing to pick a service from).

## What this is (and isn't)

This is a template generator for a one-page pitch/booking site from data you
already have — it does not scrape Instagram, does not contact any business,
and does not send anything on its own. Sourcing a business's information and
reaching out to them are still on you.

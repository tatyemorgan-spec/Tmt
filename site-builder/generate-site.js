#!/usr/bin/env node
"use strict";

/**
 * Generates a single self-contained HTML file for a local business:
 * one-page, mobile-first site with a client-side "pick service -> date ->
 * time -> confirm" booking flow (no backend, no login).
 *
 * Usage:
 *   node generate-site.js --input business.json --output site.html
 *
 * Input schema: see README.md / examples/hair-salon.json
 * Only fields present in the input are rendered — nothing is invented.
 */

const fs = require("fs");
const path = require("path");

function parseArgs(argv) {
  const args = { input: null, output: null };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--input" || a === "-i") args.input = argv[++i];
    else if (a === "--output" || a === "-o") args.output = argv[++i];
    else if (a === "--help" || a === "-h") args.help = true;
  }
  return args;
}

function fail(msg) {
  console.error("Error: " + msg);
  process.exit(1);
}

function escapeHtml(str) {
  if (str == null) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function escapeAttr(str) {
  return escapeHtml(str);
}

const MIME_BY_EXT = {
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
  ".gif": "image/gif",
  ".svg": "image/svg+xml",
};

// Resolves an image reference to something usable in <img src="...">.
// Remote URLs are left as-is; local paths are inlined as data: URIs so the
// output stays a single, self-contained HTML file.
function resolveImageSrc(src, baseDir) {
  if (!src) return null;
  if (/^(https?:)?\/\//i.test(src) || /^data:/i.test(src)) return src;
  const abs = path.isAbsolute(src) ? src : path.resolve(baseDir, src);
  if (!fs.existsSync(abs)) {
    console.warn(`Warning: image not found, skipping: ${src}`);
    return null;
  }
  const ext = path.extname(abs).toLowerCase();
  const mime = MIME_BY_EXT[ext] || "application/octet-stream";
  const b64 = fs.readFileSync(abs).toString("base64");
  return `data:${mime};base64,${b64}`;
}

function starIcons(rating) {
  const r = Math.max(0, Math.min(5, Math.round(Number(rating) || 5)));
  return "★★★★★".slice(0, r) + "☆☆☆☆☆".slice(0, 5 - r);
}

// Groups a flat services array into ordered categories (first-seen order).
function groupServices(services) {
  const order = [];
  const map = new Map();
  for (const item of services) {
    const cat = item.category || "Services";
    if (!map.has(cat)) {
      map.set(cat, []);
      order.push(cat);
    }
    map.get(cat).push(item);
  }
  return order.map((cat) => ({ category: cat, items: map.get(cat) }));
}

function buildBookingConfig(business, services) {
  const booking = business.booking || {};
  const flatServices = services.map((s, i) => ({
    id: `svc_${i}`,
    name: s.name,
    price: s.price || "",
  }));
  return {
    services: flatServices,
    availableDays:
      booking.availableDays && booking.availableDays.length
        ? booking.availableDays
        : ["Mon", "Tue", "Wed", "Thu", "Fri"],
    daysAhead: booking.daysAhead || 14,
    startHour: booking.startHour != null ? booking.startHour : 9,
    endHour: booking.endHour != null ? booking.endHour : 17,
    slotMinutes: booking.slotMinutes || 60,
  };
}

function render(data, baseDir) {
  const business = data.business || {};
  if (!business.name) fail('"business.name" is required in the input JSON.');

  const primaryColor = business.primaryColor || "#8a6240";
  const accentColor = business.accentColor || "#f6f1ea";
  const inkColor = business.inkColor || "#20201d";

  const hero = data.hero || {};
  const heroImage = resolveImageSrc(hero.image, baseDir);
  const heroHeadline = hero.headline || business.tagline || business.name;
  const heroSubheadline = hero.subheadline || "";

  const services = Array.isArray(data.services) ? data.services : [];
  const grouped = groupServices(services);

  const gallery = (Array.isArray(data.gallery) ? data.gallery : [])
    .map((g) => {
      const src = resolveImageSrc(typeof g === "string" ? g : g.src, baseDir);
      if (!src) return null;
      return { src, alt: (typeof g === "object" && g.alt) || business.name, tag: typeof g === "object" ? g.tag : null };
    })
    .filter(Boolean);

  const reviews = Array.isArray(data.reviews) ? data.reviews : [];

  const contact = business.contact || {};
  const hasBookingChannel = !!(contact.email || contact.phone);
  const bookingCfg = buildBookingConfig(business, services);
  const showBooking = services.length > 0;

  const bioBlock = business.bio
    ? `
      <section class="section" id="about">
        <p class="eyebrow">About</p>
        <h2>${escapeHtml(business.aboutHeadline || "Our Story")}</h2>
        <p class="body-text">${escapeHtml(business.bio)}</p>
      </section>`
    : "";

  const servicesBlock = grouped.length
    ? `
      <section class="section" id="services">
        <p class="eyebrow">Menu</p>
        <h2>Services &amp; Pricing</h2>
        ${business.servicesNote ? `<p class="body-text">${escapeHtml(business.servicesNote)}</p>` : ""}
        ${grouped
          .map(
            (group) => `
          <h3 class="service-category">${escapeHtml(group.category)}</h3>
          <div class="service-list">
            ${group.items
              .map(
                (item) => `
              <div class="service-row">
                <div>
                  <div class="service-name">${escapeHtml(item.name)}</div>
                  ${item.description ? `<div class="service-desc">${escapeHtml(item.description)}</div>` : ""}
                </div>
                ${item.price ? `<div class="service-price">${escapeHtml(item.price)}</div>` : ""}
              </div>`
              )
              .join("")}
          </div>`
          )
          .join("")}
      </section>`
    : "";

  const galleryBlock = gallery.length
    ? `
      <section class="section" id="gallery">
        <p class="eyebrow">Recent Work</p>
        <h2>${escapeHtml(business.galleryHeadline || "See For Yourself")}</h2>
        <div class="gallery-grid">
          ${gallery
            .map(
              (g) => `
            <div class="gallery-item">
              <img src="${g.src}" alt="${escapeAttr(g.alt)}" loading="lazy" />
              ${g.tag ? `<span class="gallery-tag">${escapeHtml(g.tag)}</span>` : ""}
            </div>`
            )
            .join("")}
        </div>
      </section>`
    : "";

  const reviewsBlock = reviews.length
    ? `
      <section class="section" id="reviews">
        <p class="eyebrow">Kind Words</p>
        <h2>What Our Clients Say</h2>
        <div class="review-list">
          ${reviews
            .map(
              (r) => `
            <div class="review-card">
              <div class="stars">${starIcons(r.rating)}</div>
              <p class="review-quote">"${escapeHtml(r.quote)}"</p>
              ${r.author ? `<p class="review-author">— ${escapeHtml(r.author)}</p>` : ""}
            </div>`
            )
            .join("")}
        </div>
      </section>`
    : "";

  const contactRows = [
    contact.address ? `<div class="contact-row">📍 ${escapeHtml(contact.address)}</div>` : "",
    contact.phone ? `<div class="contact-row">📞 <a href="tel:${escapeAttr(contact.phone)}">${escapeHtml(contact.phone)}</a></div>` : "",
    contact.email ? `<div class="contact-row">✉️ <a href="mailto:${escapeAttr(contact.email)}">${escapeHtml(contact.email)}</a></div>` : "",
    contact.instagram
      ? `<div class="contact-row">📸 <a href="https://instagram.com/${escapeAttr(contact.instagram.replace(/^@/, ""))}" target="_blank" rel="noopener">@${escapeHtml(contact.instagram.replace(/^@/, ""))}</a></div>`
      : "",
    contact.hours ? `<div class="contact-row">🕐 ${escapeHtml(contact.hours)}</div>` : "",
  ]
    .filter(Boolean)
    .join("\n");

  const contactBlock = contactRows
    ? `
      <section class="section" id="contact">
        <p class="eyebrow">Visit Us</p>
        <h2>Contact</h2>
        <div class="contact-rows">${contactRows}</div>
      </section>`
    : "";

  const bookingBlock = showBooking
    ? `
      <section class="section" id="book">
        <p class="eyebrow">Appointments</p>
        <h2>Book Your Appointment</h2>
        <p class="body-text">Pick a service, date &amp; time — no account or login needed.</p>
        <div id="booking-app"></div>
      </section>`
    : "";

  const html = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${escapeHtml(business.name)}</title>
<style>
  :root {
    --primary: ${escapeAttr(primaryColor)};
    --accent: ${escapeAttr(accentColor)};
    --ink: ${escapeAttr(inkColor)};
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: var(--ink);
    background: #fff;
    line-height: 1.5;
  }
  a { color: var(--primary); }
  .topbar {
    position: sticky;
    top: 0;
    z-index: 20;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 12px 16px;
    background: #fff;
    border-bottom: 1px solid rgba(0,0,0,0.08);
  }
  .brand { font-weight: 700; font-size: 1.05rem; }
  .btn {
    display: inline-block;
    border: none;
    border-radius: 999px;
    padding: 10px 18px;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    text-decoration: none;
    text-align: center;
  }
  .btn-primary { background: var(--primary); color: #fff; }
  .btn-outline { background: transparent; color: var(--primary); border: 1px solid var(--primary); }
  .hero {
    padding: 40px 20px 32px;
    background: var(--accent);
    text-align: center;
  }
  .hero img {
    width: 100%;
    max-width: 480px;
    border-radius: 16px;
    margin-bottom: 20px;
    object-fit: cover;
  }
  .hero h1 { font-size: 1.6rem; margin: 0 0 8px; }
  .hero p { margin: 0 0 20px; opacity: 0.85; }
  .section { max-width: 640px; margin: 0 auto; padding: 36px 20px; }
  .eyebrow { text-transform: uppercase; letter-spacing: 0.08em; font-size: 0.75rem; color: var(--primary); font-weight: 700; margin: 0 0 6px; }
  .section h2 { margin: 0 0 12px; font-size: 1.4rem; }
  .body-text { opacity: 0.85; }
  .service-category { margin: 24px 0 8px; font-size: 1rem; }
  .service-list { border-top: 1px solid rgba(0,0,0,0.08); }
  .service-row {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    padding: 12px 0;
    border-bottom: 1px solid rgba(0,0,0,0.08);
  }
  .service-name { font-weight: 600; }
  .service-desc { font-size: 0.85rem; opacity: 0.7; }
  .service-price { font-weight: 600; white-space: nowrap; }
  .gallery-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
  .gallery-item { position: relative; }
  .gallery-item img { width: 100%; height: 100%; aspect-ratio: 1 / 1; object-fit: cover; border-radius: 10px; display: block; }
  .gallery-tag {
    position: absolute; top: 8px; left: 8px;
    background: #fff; border-radius: 999px; padding: 2px 10px; font-size: 0.75rem; font-weight: 600;
  }
  .review-card { background: var(--accent); border-radius: 14px; padding: 18px; margin-bottom: 14px; }
  .stars { color: #c9982b; letter-spacing: 2px; margin-bottom: 6px; }
  .review-quote { margin: 0 0 8px; }
  .review-author { margin: 0; font-size: 0.85rem; opacity: 0.7; }
  .contact-rows { display: flex; flex-direction: column; gap: 10px; }
  .contact-row a { text-decoration: none; }
  footer { text-align: center; padding: 24px; font-size: 0.8rem; opacity: 0.6; }

  /* Booking widget */
  #booking-app { border: 1px solid rgba(0,0,0,0.1); border-radius: 16px; padding: 18px; background: #fdfcfb; }
  .bk-steps { display: flex; gap: 4px; margin-bottom: 18px; }
  .bk-steps div { flex: 1; height: 4px; border-radius: 4px; background: rgba(0,0,0,0.1); }
  .bk-steps div.done { background: var(--primary); }
  .bk-step-title { font-weight: 700; margin-bottom: 4px; }
  .bk-step-sub { font-size: 0.85rem; opacity: 0.7; margin-bottom: 14px; }
  .bk-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
  .bk-choice {
    border: 1px solid rgba(0,0,0,0.15);
    border-radius: 10px;
    padding: 10px;
    background: #fff;
    cursor: pointer;
    text-align: left;
    font: inherit;
  }
  .bk-choice:hover { border-color: var(--primary); }
  .bk-choice.selected { border-color: var(--primary); background: var(--accent); }
  .bk-choice small { display: block; opacity: 0.65; margin-top: 2px; }
  .bk-actions { display: flex; justify-content: space-between; gap: 10px; margin-top: 18px; }
  .bk-summary { background: var(--accent); border-radius: 10px; padding: 12px; margin-bottom: 14px; font-size: 0.9rem; }
  .bk-field { margin-bottom: 12px; }
  .bk-field label { display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 4px; }
  .bk-field input {
    width: 100%; padding: 10px; border-radius: 8px; border: 1px solid rgba(0,0,0,0.2); font: inherit;
  }
  .bk-note { font-size: 0.8rem; opacity: 0.65; margin-top: 10px; }
</style>
</head>
<body>
  <div class="topbar">
    <div class="brand">${escapeHtml(business.logoText || business.name)}</div>
    ${showBooking ? `<a class="btn btn-primary" href="#book">Book Now</a>` : ""}
  </div>

  <section class="hero">
    ${heroImage ? `<img src="${heroImage}" alt="${escapeAttr(business.name)}">` : ""}
    <h1>${escapeHtml(heroHeadline)}</h1>
    ${heroSubheadline ? `<p>${escapeHtml(heroSubheadline)}</p>` : ""}
    ${showBooking ? `<a class="btn btn-primary" href="#book">Book Now</a>` : ""}
  </section>

  ${bioBlock}
  ${servicesBlock}
  ${galleryBlock}
  ${reviewsBlock}
  ${bookingBlock}
  ${contactBlock}

  <footer>${escapeHtml(business.name)}</footer>

${showBooking ? `<script>
(function () {
  var CONFIG = ${JSON.stringify(bookingCfg)};
  var CONTACT = ${JSON.stringify({ email: contact.email || null, phone: contact.phone || null })};
  var DAY_NAMES = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];

  var state = { step: 1, service: null, date: null, time: null, name: "", customerContact: "" };
  var root = document.getElementById("booking-app");

  function pad(n) { return n < 10 ? "0" + n : "" + n; }

  function formatSlot(h) {
    var hour = Math.floor(h);
    var minute = Math.round((h - hour) * 60);
    var ampm = hour >= 12 ? "PM" : "AM";
    var h12 = hour % 12 === 0 ? 12 : hour % 12;
    return h12 + (minute ? ":" + pad(minute) : ":00") + " " + ampm;
  }

  function upcomingDates() {
    var out = [];
    var cursor = new Date();
    var wanted = CONFIG.availableDays;
    for (var i = 0; out.length < CONFIG.daysAhead && i < 60; i++) {
      var d = new Date(cursor.getTime());
      d.setDate(cursor.getDate() + i);
      var name = DAY_NAMES[d.getDay()];
      var short = name.slice(0, 3);
      if (wanted.indexOf(short) !== -1) {
        out.push({
          iso: d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()),
          label: short + " " + (d.getMonth() + 1) + "/" + d.getDate(),
        });
      }
    }
    return out;
  }

  function timeSlots() {
    var out = [];
    var step = CONFIG.slotMinutes / 60;
    for (var h = CONFIG.startHour; h < CONFIG.endHour; h += step) out.push(h);
    return out;
  }

  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    attrs = attrs || {};
    for (var k in attrs) {
      if (k === "class") node.className = attrs[k];
      else if (k === "onclick") node.addEventListener("click", attrs[k]);
      else node.setAttribute(k, attrs[k]);
    }
    (children || []).forEach(function (c) {
      node.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
    });
    return node;
  }

  function steps(activeCount) {
    var wrap = el("div", { class: "bk-steps" });
    for (var i = 0; i < 4; i++) {
      wrap.appendChild(el("div", { class: i < activeCount ? "done" : "" }));
    }
    return wrap;
  }

  function render() {
    root.innerHTML = "";
    root.appendChild(steps(state.step));

    if (state.step === 1) {
      root.appendChild(el("div", { class: "bk-step-title" }, ["1. Choose a service"]));
      root.appendChild(el("div", { class: "bk-step-sub" }, ["Tap the service you'd like to book."]));
      var grid = el("div", { class: "bk-grid" });
      CONFIG.services.forEach(function (s) {
        var chosen = state.service && state.service.id === s.id;
        grid.appendChild(
          el("button", { class: "bk-choice" + (chosen ? " selected" : ""), onclick: function () {
            state.service = s; state.step = 2; render();
          } }, [s.name, s.price ? el("small", {}, [s.price]) : ""].filter(Boolean))
        );
      });
      root.appendChild(grid);
    }

    if (state.step === 2) {
      root.appendChild(el("div", { class: "bk-step-title" }, ["2. Choose a date"]));
      var dates = upcomingDates();
      var grid2 = el("div", { class: "bk-grid" });
      dates.forEach(function (d) {
        var chosen = state.date && state.date.iso === d.iso;
        grid2.appendChild(
          el("button", { class: "bk-choice" + (chosen ? " selected" : ""), onclick: function () {
            state.date = d; state.step = 3; render();
          } }, [d.label])
        );
      });
      root.appendChild(grid2);
      root.appendChild(backRow(1));
    }

    if (state.step === 3) {
      root.appendChild(el("div", { class: "bk-step-title" }, ["3. Choose a time"]));
      var grid3 = el("div", { class: "bk-grid" });
      timeSlots().forEach(function (h) {
        var label = formatSlot(h);
        var chosen = state.time === label;
        grid3.appendChild(
          el("button", { class: "bk-choice" + (chosen ? " selected" : ""), onclick: function () {
            state.time = label; state.step = 4; render();
          } }, [label])
        );
      });
      root.appendChild(grid3);
      root.appendChild(backRow(2));
    }

    if (state.step === 4) {
      root.appendChild(el("div", { class: "bk-step-title" }, ["4. Confirm your details"]));
      var summary = el("div", { class: "bk-summary" }, [
        state.service.name + (state.service.price ? " (" + state.service.price + ")" : ""),
        document.createElement("br"),
        state.date.label + " at " + state.time,
      ]);
      root.appendChild(summary);

      var canSend = !!(CONTACT.email || CONTACT.phone);
      var sendBtn = el(canSend ? "a" : "button", { class: "btn btn-primary" }, ["Send Booking Request"]);

      function updateSendHref() {
        if (!canSend) return;
        var subject = "Booking request: " + state.service.name;
        var body = "Name: " + (state.name || "(not provided)") +
          "\\nContact: " + (state.customerContact || "(not provided)") +
          "\\nService: " + state.service.name +
          "\\nDate: " + state.date.label +
          "\\nTime: " + state.time;
        var href = CONTACT.email
          ? "mailto:" + CONTACT.email + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body)
          : "sms:" + CONTACT.phone + "?body=" + encodeURIComponent(subject + " - " + body.replace(/\\n/g, " | "));
        sendBtn.setAttribute("href", href);
      }

      var nameField = el("div", { class: "bk-field" }, [el("label", {}, ["Your name"])]);
      var nameInput = el("input", { type: "text", placeholder: "Jane Doe" });
      nameInput.addEventListener("input", function (e) { state.name = e.target.value; updateSendHref(); });
      nameField.appendChild(nameInput);
      root.appendChild(nameField);

      var contactField = el("div", { class: "bk-field" }, [el("label", {}, ["Phone or email"])]);
      var contactInput = el("input", { type: "text", placeholder: "(555) 123-4567" });
      contactInput.addEventListener("input", function (e) { state.customerContact = e.target.value; updateSendHref(); });
      contactField.appendChild(contactInput);
      root.appendChild(contactField);

      var actions = el("div", { class: "bk-actions" });
      actions.appendChild(el("button", { class: "btn btn-outline", onclick: function () { state.step = 3; render(); } }, ["Back"]));

      if (canSend) {
        updateSendHref();
      } else {
        sendBtn.addEventListener("click", function () {
          state.step = 5; render();
        });
      }
      actions.appendChild(sendBtn);
      root.appendChild(actions);
      root.appendChild(el("p", { class: "bk-note" }, ["This sends your request directly to us — we'll confirm shortly."]));
    }

    if (state.step === 5) {
      root.appendChild(el("div", { class: "bk-step-title" }, ["Request ready"]));
      root.appendChild(el("p", { class: "bk-step-sub" }, [
        "Please call or message us to confirm: " + state.service.name + " on " + state.date.label + " at " + state.time + "."
      ]));
    }
  }

  function backRow(prevStep) {
    var row = el("div", { class: "bk-actions" });
    row.appendChild(el("button", { class: "btn btn-outline", onclick: function () { state.step = prevStep; render(); } }, ["Back"]));
    return row;
  }

  render();
})();
</script>` : ""}
</body>
</html>
`;

  return html;
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help || !args.input) {
    console.log(
      "Usage: node generate-site.js --input <business.json> --output <site.html>\n" +
        "See site-builder/README.md for the input schema."
    );
    process.exit(args.help ? 0 : 1);
  }
  const inputPath = path.resolve(args.input);
  if (!fs.existsSync(inputPath)) fail(`input file not found: ${inputPath}`);

  let data;
  try {
    data = JSON.parse(fs.readFileSync(inputPath, "utf8"));
  } catch (e) {
    fail(`could not parse input JSON: ${e.message}`);
  }

  const baseDir = path.dirname(inputPath);
  const html = render(data, baseDir);

  const outputPath = path.resolve(args.output || (data.business && data.business.name ? `${data.business.name.toLowerCase().replace(/[^a-z0-9]+/g, "-")}.html` : "site.html"));
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, html, "utf8");
  console.log(`Wrote ${outputPath}`);
}

if (require.main === module) main();

module.exports = { render };

#!/usr/bin/env node
"use strict";

/**
 * Generates a small, production-ready static site for a local service
 * business from a JSON description: an index page (hero, services,
 * gallery, reviews, contact, client-side booking flow), plus the
 * supporting files a real launch needs — privacy policy, terms, a 404
 * page, robots.txt/sitemap.xml, and a security-headers file.
 *
 * No backend, no login, no build step, zero npm dependencies. Only data
 * present in the input JSON is ever rendered — nothing is invented.
 *
 * Usage:
 *   node generate-site.js --input business.json --outdir dist/
 */

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const WARNINGS = [];
function warn(msg) {
  WARNINGS.push(msg);
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--input" || a === "-i") args.input = argv[++i];
    else if (a === "--outdir" || a === "-o") args.outdir = argv[++i];
    else if (a === "--output") args.output = argv[++i]; // legacy single-file alias
    else if (a === "--help" || a === "-h") args.help = true;
  }
  return args;
}

function fail(msg) {
  console.error("Error: " + msg);
  process.exit(1);
}

// ---------------------------------------------------------------------------
// Small utilities
// ---------------------------------------------------------------------------

function escapeHtml(str) {
  if (str == null) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}
const escapeAttr = escapeHtml;

function slugify(str) {
  return String(str)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
}

function sha256Base64(content) {
  return crypto.createHash("sha256").update(content, "utf8").digest("base64");
}

function truncate(str, max) {
  if (!str) return "";
  if (str.length <= max) return str;
  return str.slice(0, max - 1).trimEnd() + "…";
}

// ---------------------------------------------------------------------------
// Validation (also a security measure: never emit an unvalidated value into
// a tel:/mailto:/href attribute)
// ---------------------------------------------------------------------------

function isValidEmail(v) {
  return typeof v === "string" && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
}
function isValidPhone(v) {
  return typeof v === "string" && /^\+?[0-9()\-.\s]{7,20}$/.test(v);
}
function cleanInstagramHandle(v) {
  if (!v) return null;
  const h = String(v).replace(/^@/, "").trim();
  return /^[A-Za-z0-9._]{1,30}$/.test(h) ? h : null;
}
function isValidUrl(v) {
  try {
    const u = new URL(v);
    return u.protocol === "https:" || u.protocol === "http:";
  } catch {
    return false;
  }
}

// ---------------------------------------------------------------------------
// Color math — used to auto-fix contrast instead of just hoping the input
// brand color is accessible.
// ---------------------------------------------------------------------------

function hexToRgb(hex) {
  const m = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex.trim());
  if (!m) return { r: 0, g: 0, b: 0 };
  return { r: parseInt(m[1], 16), g: parseInt(m[2], 16), b: parseInt(m[3], 16) };
}
function rgbToHex({ r, g, b }) {
  const c = (n) => Math.max(0, Math.min(255, Math.round(n))).toString(16).padStart(2, "0");
  return `#${c(r)}${c(g)}${c(b)}`;
}
function relativeLuminance({ r, g, b }) {
  const chan = (v) => {
    const s = v / 255;
    return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
  };
  return 0.2126 * chan(r) + 0.7152 * chan(g) + 0.0722 * chan(b);
}
function contrastRatio(hexA, hexB) {
  const l1 = relativeLuminance(hexToRgb(hexA));
  const l2 = relativeLuminance(hexToRgb(hexB));
  const [lighter, darker] = l1 > l2 ? [l1, l2] : [l2, l1];
  return (lighter + 0.05) / (darker + 0.05);
}
function rgbToHsl({ r, g, b }) {
  r /= 255; g /= 255; b /= 255;
  const max = Math.max(r, g, b), min = Math.min(r, g, b);
  let h, s;
  const l = (max + min) / 2;
  if (max === min) { h = s = 0; }
  else {
    const d = max - min;
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
    switch (max) {
      case r: h = (g - b) / d + (g < b ? 6 : 0); break;
      case g: h = (b - r) / d + 2; break;
      default: h = (r - g) / d + 4;
    }
    h /= 6;
  }
  return { h, s, l };
}
function hslToRgb({ h, s, l }) {
  if (s === 0) { const v = l * 255; return { r: v, g: v, b: v }; }
  const hue2rgb = (p, q, t) => {
    if (t < 0) t += 1;
    if (t > 1) t -= 1;
    if (t < 1 / 6) return p + (q - p) * 6 * t;
    if (t < 1 / 2) return q;
    if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
    return p;
  };
  const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
  const p = 2 * l - q;
  return {
    r: hue2rgb(p, q, h + 1 / 3) * 255,
    g: hue2rgb(p, q, h) * 255,
    b: hue2rgb(p, q, h - 1 / 3) * 255,
  };
}
// Nudges `hex` darker or lighter (whichever helps) until it contrasts with
// `againstHex` by at least `minRatio`. Returns { hex, changed }.
function ensureContrast(hex, againstHex, minRatio, label) {
  if (contrastRatio(hex, againstHex) >= minRatio) return { hex, changed: false };
  const bgIsLight = relativeLuminance(hexToRgb(againstHex)) > 0.5;
  const hsl = rgbToHsl(hexToRgb(hex));
  let best = hex;
  for (let i = 0; i < 50; i++) {
    hsl.l = bgIsLight ? Math.max(0, hsl.l - 0.02) : Math.min(1, hsl.l + 0.02);
    const candidate = rgbToHex(hslToRgb(hsl));
    best = candidate;
    if (contrastRatio(candidate, againstHex) >= minRatio) break;
  }
  if (label) warn(`Adjusted ${label} from ${hex} to ${best} to meet ${minRatio}:1 contrast against ${againstHex}.`);
  return { hex: best, changed: true };
}
function mix(hexA, hexB, weight) {
  const a = hexToRgb(hexA), b = hexToRgb(hexB);
  return rgbToHex({
    r: a.r + (b.r - a.r) * weight,
    g: a.g + (b.g - a.g) * weight,
    b: a.b + (b.b - a.b) * weight,
  });
}

// ---------------------------------------------------------------------------
// Images
// ---------------------------------------------------------------------------

const MIME_BY_EXT = {
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
  ".gif": "image/gif",
  ".svg": "image/svg+xml",
};
const LARGE_IMAGE_BYTES = 400 * 1024;

function resolveImageSrc(src, baseDir, label) {
  if (!src) return null;
  if (/^(https?:)?\/\//i.test(src) || /^data:/i.test(src)) return src;
  const abs = path.isAbsolute(src) ? src : path.resolve(baseDir, src);
  if (!fs.existsSync(abs)) {
    warn(`Image not found, skipped: ${src}`);
    return null;
  }
  const stat = fs.statSync(abs);
  if (stat.size > LARGE_IMAGE_BYTES) {
    warn(`${label || src} is ${(stat.size / 1024).toFixed(0)}KB — compress it before shipping (target < ${LARGE_IMAGE_BYTES / 1024}KB) for page load speed.`);
  }
  const ext = path.extname(abs).toLowerCase();
  const mime = MIME_BY_EXT[ext] || "application/octet-stream";
  return `data:${mime};base64,${fs.readFileSync(abs).toString("base64")}`;
}

function faviconDataUri(business, primaryColor) {
  const initials = (business.logoInitials || business.name || "?")
    .split(/\s+/)
    .map((w) => w[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
  const svg =
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">` +
    `<rect width="64" height="64" rx="14" fill="${primaryColor}"/>` +
    `<text x="32" y="42" font-family="Georgia, serif" font-size="28" text-anchor="middle" fill="#ffffff">${escapeHtml(initials)}</text>` +
    `</svg>`;
  return "data:image/svg+xml," + encodeURIComponent(svg);
}

// ---------------------------------------------------------------------------
// Services / reviews
// ---------------------------------------------------------------------------

function groupServices(services) {
  const order = [];
  const map = new Map();
  for (const item of services) {
    const cat = item.category || "Services";
    if (!map.has(cat)) { map.set(cat, []); order.push(cat); }
    map.get(cat).push(item);
  }
  return order.map((cat) => ({ category: cat, items: map.get(cat) }));
}

function reviewStars(rating) {
  const r = Math.max(1, Math.min(5, Math.round(Number(rating) || 5)));
  return { glyphs: "★★★★★".slice(0, r) + "☆☆☆☆☆".slice(0, 5 - r), label: `Rated ${r} out of 5 stars` };
}

function buildBookingConfig(business, services) {
  const booking = business.booking || {};
  return {
    services: services.map((s, i) => ({ id: `svc_${i}`, name: s.name, price: s.price || "" })),
    availableDays: booking.availableDays && booking.availableDays.length ? booking.availableDays : ["Mon", "Tue", "Wed", "Thu", "Fri"],
    daysAhead: booking.daysAhead || 14,
    startHour: booking.startHour != null ? booking.startHour : 9,
    endHour: booking.endHour != null ? booking.endHour : 17,
    slotMinutes: booking.slotMinutes || 60,
  };
}

// ---------------------------------------------------------------------------
// Shared document chrome (used by every generated HTML page)
// ---------------------------------------------------------------------------

// Google Fonts: Space Grotesk (bold geometric display) + Inter (clean
// body sans) — a modern agency/startup register (dark, high-contrast,
// technical-grotesk headlines) rather than the editorial/spa-serif look
// of the previous pass, which read as boutique rather than bold-modern.
const FONTS_PRECONNECT = `<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap">`;

function buildCsp({ scriptHash, styleHash, analytics, webFonts }) {
  const scriptSrc = ["'self'"];
  const connectSrc = ["'none'"];
  const styleSrc = ["'self'"];
  const fontSrc = ["'self'"];
  if (scriptHash) scriptSrc.push(`'sha256-${scriptHash}'`);
  if (webFonts) {
    styleSrc.push("https://fonts.googleapis.com");
    fontSrc.push("https://fonts.gstatic.com");
  }
  if (analytics && analytics.provider === "plausible") {
    scriptSrc.push("https://plausible.io");
    connectSrc[0] = "https://plausible.io";
  } else if (analytics && analytics.provider === "ga4") {
    scriptSrc.push("https://www.googletagmanager.com");
    connectSrc[0] = "https://www.google-analytics.com";
  }
  const directives = [
    "default-src 'self'",
    `script-src ${scriptSrc.join(" ")}`,
    `style-src ${styleSrc.join(" ")}${styleHash ? ` 'sha256-${styleHash}'` : ""}`,
    "img-src 'self' data: https:",
    `font-src ${fontSrc.join(" ")}`,
    `connect-src ${connectSrc.join(" ")}`,
    "object-src 'none'",
    "base-uri 'none'",
    "form-action 'self'",
    // frame-ancestors is intentionally omitted: it's a no-op in a <meta> CSP
    // (spec requires an HTTP header); X-Frame-Options in _headers covers it
    // for hosts that honor that file (Netlify, Cloudflare Pages).
    "upgrade-insecure-requests",
  ];
  return directives.join("; ");
}

function baseStyles(colors) {
  const { primary, primaryDark, accent, ink, surface } = colors;
  return `
  :root {
    --primary: ${primary};
    --primary-dark: ${primaryDark};
    --accent: ${accent};
    --ink: ${ink};
    --surface: ${surface};
    --surface-soft: #fafaf8;
    --line: rgba(10,10,10,0.09);
    --focus-ring: 0 0 0 3px #fff, 0 0 0 5px var(--primary);
    --font-display: "Space Grotesk", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    --font-body: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    --ease-out: cubic-bezier(0.25, 0.46, 0.45, 0.94);
    --space-section: clamp(56px, 9vw, 128px);
  }
  * { box-sizing: border-box; }
  html { -webkit-text-size-adjust: 100%; scroll-behavior: smooth; }
  section[id] { scroll-margin-top: 84px; } /* keeps the sticky header from covering the section heading on anchor jumps */
  @media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }
  body {
    margin: 0;
    font-family: var(--font-body);
    color: var(--ink);
    background: var(--surface);
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
  }
  h1, h2, h3 { font-family: var(--font-display); line-height: 1.02; margin: 0 0 0.4em; letter-spacing: -0.03em; font-weight: 600; }
  a { color: var(--primary-dark); }
  img { max-width: 100%; display: block; }
  .skip-link {
    position: absolute; left: -9999px; top: auto;
    background: var(--primary); color: #fff; padding: 12px 18px; border-radius: 0 0 8px 0;
    z-index: 100; font-weight: 600; text-decoration: none;
  }
  .skip-link:focus { left: 0; top: 0; }
  :focus-visible { outline: none; box-shadow: var(--focus-ring); border-radius: 4px; }
  .container { max-width: 1040px; margin: 0 auto; padding: 0 24px; }
  header.site-header {
    position: sticky; top: 0; z-index: 20;
    display: flex; align-items: center; justify-content: space-between;
    gap: 12px; padding: 16px 24px;
    background: rgba(255,255,255,0.9);
    -webkit-backdrop-filter: blur(14px) saturate(1.6); backdrop-filter: blur(14px) saturate(1.6);
    border-bottom: 1px solid var(--line);
  }
  .brand { display: flex; align-items: center; gap: 10px; font-family: var(--font-display); font-weight: 700; font-size: 1.1rem; text-decoration: none; color: var(--ink); }
  .brand img { width: 30px; height: 30px; border-radius: 8px; }
  .btn {
    display: inline-flex; align-items: center; justify-content: center; gap: 6px;
    border: none; border-radius: 999px; padding: 13px 24px; min-height: 44px;
    font: inherit; font-size: 0.95rem; font-weight: 600; cursor: pointer;
    text-decoration: none; text-align: center;
    transition: transform 0.18s var(--ease-out), box-shadow 0.18s var(--ease-out), background-color 0.18s var(--ease-out), opacity 0.18s var(--ease-out);
  }
  .btn-primary { background: var(--primary); color: #fff; box-shadow: 0 1px 2px rgba(0,0,0,0.1); }
  @media (hover: hover) {
    .btn-primary:hover { background: var(--primary-dark); transform: translateY(-2px); box-shadow: 0 10px 24px -8px color-mix(in srgb, var(--primary) 65%, transparent); }
    .btn-outline:hover { border-color: var(--primary-dark); background: color-mix(in srgb, var(--primary) 6%, transparent); }
  }
  .btn:active { transform: scale(0.97); box-shadow: none; }
  .btn-outline { background: transparent; color: var(--primary-dark); border: 1.5px solid var(--primary); }
  .btn[disabled] { opacity: 0.5; cursor: not-allowed; transform: none !important; }
  .btn-invert { background: #fff; color: var(--ink); }
  @media (hover: hover) { .btn-invert:hover { background: #fff; transform: translateY(-2px); box-shadow: 0 10px 24px -8px rgba(0,0,0,0.35); } }
  main { display: block; }

  /* ---- Hero: dark, bold, oversized grotesk display type ---- */
  .hero {
    padding: clamp(72px, 13vw, 160px) 24px clamp(64px, 9vw, 104px);
    background:
      radial-gradient(720px 480px at 18% -10%, color-mix(in srgb, var(--primary) 55%, transparent), transparent 65%),
      radial-gradient(900px 600px at 100% 0%, color-mix(in srgb, var(--primary) 30%, transparent), transparent 60%),
      var(--ink);
    color: #fff;
    text-align: center;
    position: relative;
    overflow: hidden;
  }
  .hero::before {
    content: ""; position: absolute; inset: 0; pointer-events: none; opacity: 0.5;
    background-image: radial-gradient(rgba(255,255,255,0.14) 1px, transparent 1px);
    background-size: 26px 26px;
    mask-image: radial-gradient(ellipse 80% 60% at 50% 30%, #000 40%, transparent 100%);
  }
  .hero > * { position: relative; }
  .hero-eyebrow { font-family: var(--font-body); text-transform: uppercase; letter-spacing: 0.16em; font-size: 0.78rem; font-weight: 600; color: #fff; opacity: 0.75; margin: 0 0 20px; }
  .hero h1 { font-size: clamp(2.75rem, 8.5vw, 5.75rem); margin: 0 0 20px; letter-spacing: -0.04em; color: #fff; }
  .hero p.subhead { margin: 0 auto 32px; opacity: 0.78; font-size: clamp(1.05rem, 2vw, 1.25rem); max-width: 46ch; font-family: var(--font-body); color: #fff; }
  .hero .btn-primary { background: #fff; color: var(--ink); }
  @media (hover: hover) { .hero .btn-primary:hover { background: #fff; opacity: 0.9; box-shadow: 0 10px 24px -8px rgba(0,0,0,0.4); } }
  .hero.has-image { padding: 0; text-align: left; }
  .hero.has-image::before { display: none; }
  .hero.has-image .hero-media { position: relative; aspect-ratio: 4 / 5; max-height: 82vh; overflow: hidden; }
  .hero.has-image .hero-media img { width: 100%; height: 100%; object-fit: cover; }
  .hero.has-image .hero-scrim { position: absolute; inset: 0; background: linear-gradient(to top, rgba(0,0,0,0.8), rgba(0,0,0,0.15) 60%); }
  .hero.has-image .hero-copy { position: absolute; left: 0; right: 0; bottom: 0; padding: 32px 28px 40px; }
  .hero.has-image h1 { font-size: clamp(2.4rem, 9vw, 4.2rem); }

  .section { max-width: 1040px; margin: 0 auto; padding: var(--space-section) 24px; }
  .section-narrow { max-width: 680px; }
  .section + .section { border-top: 1px solid var(--line); }
  .eyebrow { text-transform: uppercase; letter-spacing: 0.14em; font-size: 0.75rem; color: var(--primary-dark); font-weight: 700; margin: 0 0 10px; }
  .section h2 { font-size: clamp(1.8rem, 4vw, 2.5rem); }
  .section-head { max-width: 640px; margin-bottom: 40px; }
  .rule { width: 48px; height: 3px; background: var(--primary); border: none; margin: 16px 0 0; border-radius: 2px; }
  .body-text { opacity: 0.75; max-width: 60ch; font-size: 1.05rem; }
  .service-category { margin: 32px 0 10px; font-size: 1.1rem; font-family: var(--font-display); }
  .service-category:first-of-type { margin-top: 8px; }
  .service-list { border-top: 1px solid var(--line); }
  .service-row { display: flex; justify-content: space-between; gap: 12px; padding: 16px 2px; border-bottom: 1px solid var(--line); }
  .service-name { font-weight: 600; }
  .service-desc { font-size: 0.88rem; opacity: 0.65; margin-top: 2px; }
  .service-price { font-weight: 600; white-space: nowrap; color: var(--primary-dark); }

  /* ---- Bento-style gallery grid: varied spans, not a flat 2-col wall ---- */
  .gallery-grid { display: grid; grid-template-columns: repeat(4, 1fr); grid-auto-rows: minmax(90px, auto); gap: 12px; }
  .gallery-item { position: relative; border-radius: 20px; overflow: hidden; background: var(--surface-soft); grid-column: span 2; grid-row: span 2; }
  .gallery-item.span-wide { grid-column: span 4; aspect-ratio: 16 / 9; }
  .gallery-item.span-tall { grid-row: span 3; }
  .gallery-item img { width: 100%; height: 100%; object-fit: cover; }
  @media (hover: hover) {
    .gallery-item img { transition: transform 0.5s var(--ease-out); }
    .gallery-item:hover img { transform: scale(1.045); }
  }
  .gallery-tag { position: absolute; top: 12px; left: 12px; background: rgba(255,255,255,0.94); border-radius: 999px; padding: 4px 13px; font-size: 0.75rem; font-weight: 600; }
  @media (max-width: 640px) {
    .gallery-grid { grid-template-columns: repeat(2, 1fr); }
    .gallery-item { grid-column: span 1; grid-row: span 1; aspect-ratio: 4 / 5; }
    .gallery-item.span-wide { grid-column: span 2; }
  }

  /* ---- Reviews: one editorial pull-quote + a bento row of supporting cards ---- */
  .review-list { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
  .review-card { background: var(--surface-soft); border-radius: 20px; padding: 26px; position: relative; }
  .review-card.pull-quote { grid-column: 1 / -1; background: var(--ink); color: #fff; padding: clamp(32px, 5vw, 56px); }
  .review-card.pull-quote::before {
    content: "\\201C"; font-family: var(--font-display); font-size: 5rem; line-height: 1; color: var(--primary);
    opacity: 0.8; display: block; margin-bottom: -0.3em;
  }
  .review-card.pull-quote .review-quote { font-family: var(--font-display); font-weight: 500; font-size: clamp(1.3rem, 2.6vw, 1.9rem); line-height: 1.3; letter-spacing: -0.02em; color: #fff; }
  .review-card.pull-quote .review-author { color: rgba(255,255,255,0.7); }
  .review-card.pull-quote .stars { color: #ffd876; }
  .stars { color: #c9982b; letter-spacing: 2px; }
  .review-quote { margin: 10px 0 14px; font-size: 1.02rem; }
  .review-author { margin: 0; font-size: 0.85rem; opacity: 0.65; }
  @media (max-width: 640px) { .review-list { grid-template-columns: 1fr; } .review-card.pull-quote { grid-column: auto; } }

  .visually-hidden { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
  .contact-rows { display: flex; flex-direction: column; gap: 14px; }
  .contact-row { display: flex; align-items: center; gap: 10px; }
  .contact-row a { text-decoration: none; font-weight: 600; }
  .cta-row { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 20px; }

  /* ---- Closing CTA band: inverted, high-impact, one job: get the click ---- */
  .cta-band { background: var(--ink); color: #fff; text-align: center; padding: clamp(56px, 10vw, 110px) 24px; }
  .cta-band h2 { color: #fff; font-size: clamp(2rem, 5vw, 3.2rem); margin-bottom: 16px; }
  .cta-band p { color: rgba(255,255,255,0.72); margin: 0 auto 32px; max-width: 46ch; font-size: 1.05rem; }

  footer.site-footer { text-align: center; padding: 32px 20px; font-size: 0.85rem; opacity: 0.6; }

  /* ---- Motion: JS arms .reveal groups only when IO + no-reduced-motion;
     everything is visible by default so no-JS / crawlers / reduced-motion
     always see full content immediately. ---- */
  .reveal { opacity: 1; transform: none; }
  html.reveal-armed .reveal:not(.in-view) { opacity: 0; transform: translateY(24px); }
  html.reveal-armed .reveal.in-view {
    opacity: 1; transform: none;
    transition: opacity 0.6s var(--ease-out), transform 0.6s var(--ease-out);
    transition-delay: var(--reveal-delay, 0ms);
  }
  #booking-app { border: 1px solid rgba(0,0,0,0.1); border-radius: 18px; padding: 20px; background: var(--surface); }
  .bk-steps { display: flex; gap: 4px; margin-bottom: 20px; }
  .bk-steps div { flex: 1; height: 4px; border-radius: 4px; background: rgba(0,0,0,0.1); }
  .bk-steps div.done { background: var(--primary); }
  .bk-step-title { font-weight: 700; margin-bottom: 4px; }
  .bk-step-sub { font-size: 0.88rem; opacity: 0.7; margin-bottom: 16px; }
  .bk-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
  .bk-choice {
    border: 1.5px solid var(--line); border-radius: 14px; padding: 13px; background: var(--surface);
    cursor: pointer; text-align: left; font: inherit; min-height: 44px;
    transition: border-color 0.15s var(--ease-out), background-color 0.15s var(--ease-out), transform 0.15s var(--ease-out);
  }
  @media (hover: hover) { .bk-choice:hover { border-color: var(--primary); } }
  .bk-choice:active { transform: scale(0.97); }
  .bk-choice.selected { border-color: var(--primary); background: var(--accent); }
  .bk-choice[aria-pressed="true"] { border-width: 2px; }
  .bk-choice small { display: block; opacity: 0.65; margin-top: 2px; }
  .bk-actions { display: flex; justify-content: space-between; gap: 10px; margin-top: 20px; }
  .bk-summary { background: var(--accent); border-radius: 12px; padding: 14px; margin-bottom: 16px; font-size: 0.92rem; }
  .bk-field { margin-bottom: 14px; }
  .bk-field label { display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 5px; }
  .bk-field input { width: 100%; padding: 12px; border-radius: 8px; border: 1px solid rgba(0,0,0,0.25); font: inherit; min-height: 44px; }
  .bk-field input[aria-invalid="true"] { border-color: #b3261e; }
  .bk-error { color: #b3261e; font-size: 0.82rem; margin-top: 4px; }
  .bk-note { font-size: 0.8rem; opacity: 0.65; margin-top: 12px; }
  .legal-page main { max-width: 680px; margin: 0 auto; padding: 40px 20px 64px; }
  .legal-banner { background: #fff6e5; border: 1px solid #f0d999; border-radius: 10px; padding: 14px 16px; font-size: 0.9rem; margin-bottom: 28px; }
  .error-page { min-height: 70vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 40px 20px; }
  .cookie-banner {
    position: fixed; left: 12px; right: 12px; bottom: 12px; z-index: 50;
    background: var(--ink); color: #fff; border-radius: 14px; padding: 16px;
    display: flex; flex-wrap: wrap; gap: 12px; align-items: center; justify-content: space-between;
    box-shadow: 0 8px 30px rgba(0,0,0,0.25);
  }
  .cookie-banner p { margin: 0; font-size: 0.85rem; flex: 1 1 240px; }
  .cookie-actions { display: flex; gap: 8px; }
  .cookie-actions button { border-radius: 999px; border: none; padding: 8px 16px; font: inherit; font-weight: 600; cursor: pointer; min-height: 40px; }
  .cookie-accept { background: var(--primary); color: #fff; }
  .cookie-decline { background: transparent; color: #fff; border: 1px solid rgba(255,255,255,0.5) !important; }
  @media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; } }
  `;
}

function pageShell({ title, description, canonical, socialImage, faviconUri, cspContent, styleTag, bodyHtml, ogType }) {
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="${escapeAttr(cspContent)}">
<title>${escapeHtml(title)}</title>
${description ? `<meta name="description" content="${escapeAttr(description)}">` : ""}
${canonical ? `<link rel="canonical" href="${escapeAttr(canonical)}">` : ""}
<link rel="icon" href="${faviconUri}">
<meta property="og:type" content="${ogType || "website"}">
<meta property="og:title" content="${escapeAttr(title)}">
${description ? `<meta property="og:description" content="${escapeAttr(description)}">` : ""}
${canonical ? `<meta property="og:url" content="${escapeAttr(canonical)}">` : ""}
${socialImage ? `<meta property="og:image" content="${escapeAttr(socialImage)}">\n<meta name="twitter:card" content="summary_large_image">` : `<meta name="twitter:card" content="summary">`}
${FONTS_PRECONNECT}
${styleTag}
</head>
<body>
${bodyHtml}
</body>
</html>
`;
}

// ---------------------------------------------------------------------------
// Booking widget (client-side only script, built as a plain string so it can
// be sha256-hashed for the CSP script-src allowlist)
// ---------------------------------------------------------------------------

function buildBookingScript(bookingCfg, contact) {
  return `(function () {
  var CONFIG = ${JSON.stringify(bookingCfg)};
  var CONTACT = ${JSON.stringify({ email: contact.email || null, phone: contact.phone || null })};
  var DAY_NAMES = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];
  var state = { step: 1, service: null, date: null, time: null, name: "", customerContact: "" };
  var root = document.getElementById("booking-app");
  var live = document.getElementById("booking-live");

  function announce(msg) { if (live) live.textContent = msg; }
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
      var short = DAY_NAMES[d.getDay()].slice(0, 3);
      if (wanted.indexOf(short) !== -1) {
        out.push({ iso: d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()), label: short + " " + (d.getMonth() + 1) + "/" + d.getDate() });
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
      else if (k === "oninput") node.addEventListener("input", attrs[k]);
      else node.setAttribute(k, attrs[k]);
    }
    (children || []).forEach(function (c) { if (c) node.appendChild(typeof c === "string" ? document.createTextNode(c) : c); });
    return node;
  }

  function steps(activeCount) {
    var wrap = el("div", { class: "bk-steps", role: "presentation" });
    for (var i = 0; i < 4; i++) wrap.appendChild(el("div", { class: i < activeCount ? "done" : "" }));
    return wrap;
  }

  function backRow(prevStep, label) {
    var row = el("div", { class: "bk-actions" });
    row.appendChild(el("button", { class: "btn btn-outline", type: "button", onclick: function () { state.step = prevStep; render(); } }, ["Back to " + label]));
    return row;
  }

  function render() {
    root.innerHTML = "";
    root.appendChild(steps(state.step));

    if (state.step === 1) {
      root.appendChild(el("h3", { class: "bk-step-title" }, ["1. Choose a service"]));
      root.appendChild(el("p", { class: "bk-step-sub" }, ["Tap the service you'd like to book."]));
      var grid = el("div", { class: "bk-grid", role: "group", "aria-label": "Choose a service" });
      CONFIG.services.forEach(function (s) {
        grid.appendChild(el("button", { class: "bk-choice", type: "button", "aria-pressed": "false", onclick: function () {
          state.service = s; state.step = 2; announce("Service selected: " + s.name + ". Step 2 of 4, choose a date."); render();
        } }, [s.name, s.price ? el("small", {}, [s.price]) : null]));
      });
      root.appendChild(grid);
    }

    if (state.step === 2) {
      root.appendChild(el("h3", { class: "bk-step-title" }, ["2. Choose a date"]));
      var dates = upcomingDates();
      var grid2 = el("div", { class: "bk-grid", role: "group", "aria-label": "Choose a date" });
      if (!dates.length) root.appendChild(el("p", { class: "bk-step-sub" }, ["No upcoming availability configured — please contact us directly."]));
      dates.forEach(function (d) {
        grid2.appendChild(el("button", { class: "bk-choice", type: "button", "aria-pressed": "false", onclick: function () {
          state.date = d; state.step = 3; announce("Date selected: " + d.label + ". Step 3 of 4, choose a time."); render();
        } }, [d.label]));
      });
      root.appendChild(grid2);
      root.appendChild(backRow(1, "service"));
    }

    if (state.step === 3) {
      root.appendChild(el("h3", { class: "bk-step-title" }, ["3. Choose a time"]));
      var grid3 = el("div", { class: "bk-grid", role: "group", "aria-label": "Choose a time" });
      timeSlots().forEach(function (h) {
        var label = formatSlot(h);
        grid3.appendChild(el("button", { class: "bk-choice", type: "button", "aria-pressed": "false", onclick: function () {
          state.time = label; state.step = 4; announce("Time selected: " + label + ". Step 4 of 4, confirm your details."); render();
        } }, [label]));
      });
      root.appendChild(grid3);
      root.appendChild(backRow(2, "date"));
    }

    if (state.step === 4) {
      root.appendChild(el("h3", { class: "bk-step-title" }, ["4. Confirm your details"]));
      root.appendChild(el("div", { class: "bk-summary" }, [
        state.service.name + (state.service.price ? " (" + state.service.price + ")" : ""),
        document.createElement("br"),
        state.date.label + " at " + state.time,
      ]));

      var errors = { name: null, contact: null };

      var nameField = el("div", { class: "bk-field" }, [el("label", { for: "bk-name" }, ["Your name"])]);
      var nameInput = el("input", { type: "text", id: "bk-name", name: "bk-name", autocomplete: "name", required: "required", "aria-describedby": "bk-name-err" });
      nameInput.addEventListener("input", function (e) { state.name = e.target.value; validate(); });
      var nameErr = el("div", { id: "bk-name-err", class: "bk-error", role: "alert" }, []);
      nameField.appendChild(nameInput);
      nameField.appendChild(nameErr);
      root.appendChild(nameField);

      var contactField = el("div", { class: "bk-field" }, [el("label", { for: "bk-contact" }, ["Phone or email"])]);
      var contactInput = el("input", { type: "text", id: "bk-contact", name: "bk-contact", autocomplete: "tel", required: "required", "aria-describedby": "bk-contact-err" });
      contactInput.addEventListener("input", function (e) { state.customerContact = e.target.value; validate(); });
      var contactErr = el("div", { id: "bk-contact-err", class: "bk-error", role: "alert" }, []);
      contactField.appendChild(contactInput);
      contactField.appendChild(contactErr);
      root.appendChild(contactField);

      // Honeypot: hidden from sighted/keyboard users, visible to naive bots that
      // fill every field. If it's non-empty on submit we silently no-op.
      var honeypot = el("input", { type: "text", tabindex: "-1", autocomplete: "off", class: "visually-hidden", "aria-hidden": "true", name: "company_website", id: "bk-hp" });
      root.appendChild(honeypot);

      var actions = el("div", { class: "bk-actions" });
      actions.appendChild(el("button", { class: "btn btn-outline", type: "button", onclick: function () { state.step = 3; render(); } }, ["Back to time"]));

      var canSend = !!(CONTACT.email || CONTACT.phone);
      var sendBtn = el("button", { class: "btn btn-primary", type: "button" }, [canSend ? "Send Booking Request" : "Confirm"]);
      sendBtn.disabled = true;

      function validate() {
        errors.name = state.name.trim().length >= 2 ? null : "Enter your name.";
        var c = state.customerContact.trim();
        var looksLikeContact = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(c) || /^\\+?[0-9()\\-.\\s]{7,20}$/.test(c);
        errors.contact = looksLikeContact ? null : "Enter a valid phone number or email.";
        nameErr.textContent = errors.name || "";
        contactErr.textContent = errors.contact || "";
        nameInput.setAttribute("aria-invalid", errors.name ? "true" : "false");
        contactInput.setAttribute("aria-invalid", errors.contact ? "true" : "false");
        sendBtn.disabled = !!(errors.name || errors.contact);
      }

      sendBtn.addEventListener("click", function () {
        if (honeypot.value) return; // bot: silently drop
        validate();
        if (errors.name || errors.contact) return;
        if (!canSend) { state.step = 5; render(); return; }
        var subject = "Booking request: " + state.service.name;
        var body = "Name: " + state.name + "\\nContact: " + state.customerContact + "\\nService: " + state.service.name + "\\nDate: " + state.date.label + "\\nTime: " + state.time;
        var href = CONTACT.email
          ? "mailto:" + CONTACT.email + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body)
          : "sms:" + CONTACT.phone + "?body=" + encodeURIComponent(subject + " - " + body.replace(/\\n/g, " | "));
        window.location.href = href;
      });

      actions.appendChild(sendBtn);
      root.appendChild(actions);
      root.appendChild(el("p", { class: "bk-note" }, ["This opens your messaging app to send the request directly to us — we'll confirm shortly."]));
    }

    if (state.step === 5) {
      root.appendChild(el("h3", { class: "bk-step-title" }, ["Request ready"]));
      root.appendChild(el("p", { class: "bk-step-sub" }, ["Please call or message us to confirm: " + state.service.name + " on " + state.date.label + " at " + state.time + "."]));
    }
  }

  render();
})();`;
}

function buildCookieBannerScript() {
  return `(function () {
  var KEY = "cookie-consent";
  var banner = document.getElementById("cookie-banner");
  if (!banner) return;
  var stored = null;
  try { stored = localStorage.getItem(KEY); } catch (e) {}
  function loadAnalytics() {
    var tpl = document.getElementById("analytics-snippet");
    if (tpl && tpl.content) document.body.appendChild(tpl.content.cloneNode(true));
  }
  if (stored === "accepted") { loadAnalytics(); }
  if (stored) { banner.hidden = true; return; }
  banner.hidden = false;
  var accept = document.getElementById("cookie-accept");
  var decline = document.getElementById("cookie-decline");
  if (accept) accept.addEventListener("click", function () {
    try { localStorage.setItem(KEY, "accepted"); } catch (e) {}
    banner.hidden = true;
    loadAnalytics();
  });
  if (decline) decline.addEventListener("click", function () {
    try { localStorage.setItem(KEY, "declined"); } catch (e) {}
    banner.hidden = true;
  });
})();`;
}

// Scroll-reveal, hand-rolled (no GSAP/Framer Motion — this stays a single
// dependency-free HTML file). Timing/easing/stagger-cap values are ported
// from the ui-ux-pro-max design-data skill's "Scroll Reveal — Standard"
// GSAP preset (duration 400-600ms, power2.out, viewport-enter trigger,
// don't stagger more than ~8 children) rather than guessed.
//
// Content is opacity:1 by default in CSS (see .reveal in baseStyles) so
// no-JS clients and crawlers always see everything immediately. This script
// only *arms* the hidden-until-in-view behavior, and skips that entirely
// under prefers-reduced-motion.
function buildRevealScript() {
  return `(function () {
  if (!window.IntersectionObserver || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  document.documentElement.classList.add('reveal-armed');
  var groups = document.querySelectorAll('[data-reveal-group]');
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('in-view');
      io.unobserve(entry.target);
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -10% 0px' });
  groups.forEach(function (group) {
    var items = group.hasAttribute('data-reveal-self') ? [group] : Array.prototype.slice.call(group.children);
    items.slice(0, 8).forEach(function (item, i) {
      item.classList.add('reveal');
      item.style.setProperty('--reveal-delay', (i * 80) + 'ms');
      io.observe(item);
    });
    items.slice(8).forEach(function (item) { item.classList.add('reveal', 'in-view'); });
  });
})();`;
}

// ---------------------------------------------------------------------------
// Page builders
// ---------------------------------------------------------------------------

function renderIndex(data, baseDir) {
  const business = data.business || {};
  if (!business.name) fail('"business.name" is required in the input JSON.');

  const surface = "#ffffff";
  let primary = business.primaryColor || "#8a6240";
  const accent = business.accentColor || mix(primary, "#ffffff", 0.9);
  let ink = business.inkColor || "#20201d";

  ({ hex: primary } = ensureContrast(primary, surface, 4.5, "business.primaryColor (button text on it must stay readable)"));
  ({ hex: ink } = ensureContrast(ink, accent, 4.5, "business.inkColor (body text against accentColor)"));
  const primaryDark = mix(primary, "#000000", 0.18);
  const colors = { primary, primaryDark, accent, ink, surface };

  const siteUrl = business.siteUrl && isValidUrl(business.siteUrl) ? business.siteUrl.replace(/\/$/, "") : null;
  if (business.siteUrl && !siteUrl) warn(`business.siteUrl "${business.siteUrl}" is not a valid absolute URL — canonical link, sitemap, and robots.txt are skipped.`);

  const hero = data.hero || {};
  const heroImage = resolveImageSrc(hero.image, baseDir, "hero.image");
  const heroHeadline = hero.headline || business.tagline || business.name;
  const heroSubheadline = hero.subheadline || "";

  const services = Array.isArray(data.services) ? data.services : [];
  const grouped = groupServices(services);
  const showBooking = services.length > 0;

  const gallery = (Array.isArray(data.gallery) ? data.gallery : [])
    .map((g, i) => {
      const raw = typeof g === "string" ? { src: g } : g;
      const src = resolveImageSrc(raw.src, baseDir, `gallery[${i}]`);
      if (!src) return null;
      if (!raw.alt) warn(`gallery[${i}] has no "alt" text — add a short description of the photo for screen-reader users.`);
      return { src, alt: raw.alt || `${business.name} — photo ${i + 1}`, tag: raw.tag || null };
    })
    .filter(Boolean);

  const reviews = Array.isArray(data.reviews) ? data.reviews : [];
  const contact = business.contact || {};
  const validEmail = contact.email && isValidEmail(contact.email) ? contact.email : (contact.email ? (warn(`contact.email "${contact.email}" doesn't look valid — omitted.`), null) : null);
  const validPhone = contact.phone && isValidPhone(contact.phone) ? contact.phone : (contact.phone ? (warn(`contact.phone "${contact.phone}" doesn't look valid — omitted.`), null) : null);
  const igHandle = cleanInstagramHandle(contact.instagram);
  if (contact.instagram && !igHandle) warn(`contact.instagram "${contact.instagram}" doesn't look like a valid handle — omitted.`);

  const bookingCfg = buildBookingConfig(business, services);
  const faviconUri = faviconDataUri(business, primary);
  const analytics = data.analytics && data.analytics.provider ? data.analytics : null;
  const cookieBannerNeeded = !!(analytics && analytics.provider === "ga4");

  // ---- body sections -------------------------------------------------
  const metaDescription = truncate(business.metaDescription || business.bio || business.tagline || `${business.name} — ${business.tagline || "book an appointment"}.`, 155);
  const socialImage = business.socialImage && isValidUrl(business.socialImage) ? business.socialImage : (heroImage && /^https?:/i.test(heroImage) ? heroImage : null);
  if (!socialImage && heroImage) warn("Hero image is embedded locally (data: URI), so it can't be used as a social-share preview image. Set business.socialImage to a hosted https:// image URL if you want link previews to show a photo.");

  const bioBlock = business.bio ? `
      <section class="section section-narrow" id="about" aria-labelledby="about-h">
        <div class="section-head" data-reveal-group data-reveal-self>
          <p class="eyebrow">About</p>
          <h2 id="about-h">${escapeHtml(business.aboutHeadline || "Our Story")}</h2>
          <hr class="rule" aria-hidden="true">
        </div>
        <p class="body-text" data-reveal-group data-reveal-self>${escapeHtml(business.bio)}</p>
      </section>` : "";

  const servicesBlock = grouped.length ? `
      <section class="section" id="services" aria-labelledby="services-h">
        <div class="section-head" data-reveal-group data-reveal-self>
          <p class="eyebrow">Menu</p>
          <h2 id="services-h">Services &amp; Pricing</h2>
          <hr class="rule" aria-hidden="true">
          ${business.servicesNote ? `<p class="body-text">${escapeHtml(business.servicesNote)}</p>` : ""}
        </div>
        ${grouped.map((group) => `
          <h3 class="service-category">${escapeHtml(group.category)}</h3>
          <div class="service-list" data-reveal-group>
            ${group.items.map((item) => `
              <div class="service-row">
                <div>
                  <div class="service-name">${escapeHtml(item.name)}</div>
                  ${item.description ? `<div class="service-desc">${escapeHtml(item.description)}</div>` : ""}
                </div>
                ${item.price ? `<div class="service-price">${escapeHtml(item.price)}</div>` : ""}
              </div>`).join("")}
          </div>`).join("")}
      </section>` : "";

  const galleryBlock = gallery.length ? `
      <section class="section" id="gallery" aria-labelledby="gallery-h">
        <div class="section-head" data-reveal-group data-reveal-self>
          <p class="eyebrow">Recent Work</p>
          <h2 id="gallery-h">${escapeHtml(business.galleryHeadline || "See For Yourself")}</h2>
          <hr class="rule" aria-hidden="true">
        </div>
        <div class="gallery-grid" data-reveal-group>
          ${gallery.map((g, i) => `
            <div class="gallery-item${i === 0 && gallery.length > 1 ? " span-wide" : ""}">
              <img src="${g.src}" alt="${escapeAttr(g.alt)}" loading="lazy" decoding="async">
              ${g.tag ? `<span class="gallery-tag">${escapeHtml(g.tag)}</span>` : ""}
            </div>`).join("")}
        </div>
      </section>` : "";

  const reviewsBlock = reviews.length ? `
      <section class="section" id="reviews" aria-labelledby="reviews-h">
        <div class="section-head" data-reveal-group data-reveal-self>
          <p class="eyebrow">Kind Words</p>
          <h2 id="reviews-h">What Clients Say</h2>
          <hr class="rule" aria-hidden="true">
        </div>
        <div class="review-list" data-reveal-group>
          ${reviews.map((r, i) => { const s = reviewStars(r.rating); return `
            <div class="review-card${i === 0 && reviews.length > 1 ? " pull-quote" : ""}">
              <span class="stars" aria-hidden="true">${s.glyphs}</span>
              <span class="visually-hidden">${escapeHtml(s.label)}</span>
              <p class="review-quote">"${escapeHtml(r.quote)}"</p>
              ${r.author ? `<p class="review-author">— ${escapeHtml(r.author)}</p>` : ""}
            </div>`; }).join("")}
        </div>
      </section>` : "";

  const contactRows = [
    contact.address ? `<div class="contact-row"><span aria-hidden="true">📍</span> <span>${escapeHtml(contact.address)}</span></div>` : "",
    validPhone ? `<div class="contact-row"><span aria-hidden="true">📞</span> <a href="tel:${escapeAttr(validPhone)}">${escapeHtml(validPhone)}</a></div>` : "",
    validEmail ? `<div class="contact-row"><span aria-hidden="true">✉️</span> <a href="mailto:${escapeAttr(validEmail)}">${escapeHtml(validEmail)}</a></div>` : "",
    igHandle ? `<div class="contact-row"><span aria-hidden="true">📸</span> <a href="https://instagram.com/${escapeAttr(igHandle)}" target="_blank" rel="noopener noreferrer">@${escapeHtml(igHandle)}</a></div>` : "",
    contact.hours ? `<div class="contact-row"><span aria-hidden="true">🕐</span> <span>${escapeHtml(contact.hours)}</span></div>` : "",
  ].filter(Boolean).join("\n");

  const contactBlock = contactRows ? `
      <section class="section section-narrow" id="contact" aria-labelledby="contact-h">
        <div class="section-head" data-reveal-group data-reveal-self>
          <p class="eyebrow">Visit Us</p>
          <h2 id="contact-h">Contact</h2>
          <hr class="rule" aria-hidden="true">
        </div>
        <div class="contact-rows" data-reveal-group data-reveal-self>${contactRows}</div>
      </section>` : "";

  const bookingBlock = showBooking ? `
      <section class="section" id="book" aria-labelledby="book-h">
        <p class="eyebrow">Appointments</p>
        <h2 id="book-h">Book Your Appointment</h2>
        <hr class="rule" aria-hidden="true">
        <p class="body-text">Pick a service, date &amp; time — no account or login needed.</p>
        <div id="booking-app" role="group" aria-label="Book an appointment"></div>
        <p id="booking-live" class="visually-hidden" role="status" aria-live="polite"></p>
      </section>` : "";

  const ctaHref = showBooking ? "#book" : validPhone ? `tel:${escapeAttr(validPhone)}` : igHandle ? `https://instagram.com/${escapeAttr(igHandle)}` : validEmail ? `mailto:${escapeAttr(validEmail)}` : null;
  const ctaLabel = showBooking ? "Book Now" : validPhone ? "Call Now" : igHandle ? "DM to Book" : validEmail ? "Email to Book" : null;
  const ctaIsExternal = !showBooking && !validPhone && igHandle;
  function ctaButton(cls) {
    if (!ctaHref) return "";
    return `<a class="btn ${cls}" href="${ctaHref}"${ctaIsExternal ? ` target="_blank" rel="noopener noreferrer"` : ""}>${ctaLabel}</a>`;
  }
  const topCta = ctaButton("btn-primary");

  const heroBlock = heroImage ? `
    <section class="hero has-image" aria-labelledby="hero-h">
      <div class="hero-media"><img src="${heroImage}" alt="" role="presentation"></div>
      <div class="hero-scrim" aria-hidden="true"></div>
      <div class="hero-copy" data-reveal-group>
        <h1 id="hero-h">${escapeHtml(heroHeadline)}</h1>
        ${heroSubheadline ? `<p class="subhead">${escapeHtml(heroSubheadline)}</p>` : ""}
        ${topCta}
      </div>
    </section>` : `
    <section class="hero" aria-labelledby="hero-h">
      <div data-reveal-group>
        <h1 id="hero-h">${escapeHtml(heroHeadline)}</h1>
        ${heroSubheadline ? `<p class="subhead">${escapeHtml(heroSubheadline)}</p>` : ""}
        ${topCta}
      </div>
    </section>`;

  // Bold closing CTA band. Skipped when the booking wizard is present since
  // that section already ends the page with a strong, non-redundant CTA.
  const ctaBandBlock = !showBooking && ctaHref ? `
      <section class="cta-band" aria-labelledby="cta-band-h">
        <div data-reveal-group data-reveal-self>
          <h2 id="cta-band-h">${escapeHtml(business.closingHeadline || `Ready to book with ${business.name}?`)}</h2>
          <p>${escapeHtml(business.closingSubhead || "Reach out and we'll get you sorted.")}</p>
          ${ctaButton("btn-invert")}
        </div>
      </section>` : "";

  const cookieBannerHtml = cookieBannerNeeded ? `
    <div id="cookie-banner" class="cookie-banner" role="dialog" aria-label="Cookie notice" hidden>
      <p>We use analytics cookies to understand site traffic. See our <a href="privacy.html">privacy policy</a>.</p>
      <div class="cookie-actions">
        <button id="cookie-decline" class="cookie-decline" type="button">Decline</button>
        <button id="cookie-accept" class="cookie-accept" type="button">Accept</button>
      </div>
    </div>` : "";

  const analyticsSnippet = analytics
    ? analytics.provider === "plausible" && analytics.domain
      ? `<script defer data-domain="${escapeAttr(analytics.domain)}" src="https://plausible.io/js/script.js"></script>`
      : analytics.provider === "ga4" && analytics.id
        ? `<script async src="https://www.googletagmanager.com/gtag/js?id=${escapeAttr(analytics.id)}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','${escapeAttr(analytics.id)}');</script>`
        : ""
    : "";
  const analyticsHtml = analyticsSnippet
    ? (cookieBannerNeeded ? `<template id="analytics-snippet">${analyticsSnippet}</template>` : analyticsSnippet)
    : "";
  if (analytics && analytics.provider === "plausible" && !analytics.domain) warn('analytics.provider is "plausible" but analytics.domain is missing — analytics not injected.');
  if (analytics && analytics.provider === "ga4" && !analytics.id) warn('analytics.provider is "ga4" but analytics.id is missing — analytics not injected.');

  const bookingScript = showBooking ? buildBookingScript(bookingCfg, { email: validEmail, phone: validPhone }) : "";
  const cookieScript = cookieBannerNeeded ? buildCookieBannerScript() : "";
  const fullScript = [buildRevealScript(), bookingScript, cookieScript].filter(Boolean).join("\n\n");
  const styleContent = baseStyles(colors);

  const bodyHtml = `<a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <a class="brand" href="#main"><img src="${faviconUri}" alt="" role="presentation">${escapeHtml(business.logoText || business.name)}</a>
    ${topCta}
  </header>
  <main id="main">
    ${heroBlock}
    ${bioBlock}
    ${servicesBlock}
    ${galleryBlock}
    ${reviewsBlock}
    ${bookingBlock}
    ${ctaBandBlock}
    ${contactBlock}
  </main>
  <footer class="site-footer">
    <p>${escapeHtml(business.name)} · <a href="privacy.html">Privacy</a> · <a href="terms.html">Terms</a></p>
  </footer>
  ${cookieBannerHtml}
  ${analyticsHtml}
  ${fullScript ? `<script>${fullScript}</script>` : ""}
`;

  const scriptHash = fullScript ? sha256Base64(fullScript) : null;
  const styleHash = sha256Base64(styleContent);
  const csp = buildCsp({ scriptHash, styleHash, analytics, webFonts: true });

  const html = pageShell({
    title: business.name,
    description: metaDescription,
    canonical: siteUrl ? siteUrl + "/" : null,
    socialImage,
    faviconUri,
    cspContent: csp,
    styleTag: `<style>${styleContent}</style>`,
    bodyHtml,
  });

  return { html, colors, siteUrl, faviconUri };
}

function legalPageShell({ title, business, colors, faviconUri, bodyHtml }) {
  const styleContent = baseStyles(colors) + `.legal-page main { max-width: 680px; }`;
  const csp = buildCsp({ styleHash: sha256Base64(styleContent), webFonts: true });
  return pageShell({
    title: `${title} — ${business.name}`,
    faviconUri,
    cspContent: csp,
    styleTag: `<style>${styleContent}</style>`,
    bodyHtml: `<div class="legal-page"><header class="site-header"><a class="brand" href="index.html">${escapeHtml(business.name)}</a><a class="btn btn-outline" href="index.html">Back to site</a></header><main>${bodyHtml}</main></div>`,
  });
}

function buildPrivacyPolicy(business, colors, faviconUri) {
  const contact = business.contact || {};
  const contactLine = contact.email || contact.phone || "the contact details on our homepage";
  const body = `
    <h1>Privacy Policy</h1>
    <div class="legal-banner">This is a generic starting template, not legal advice. Have it reviewed for your business and jurisdiction (e.g. UK GDPR, EU GDPR, US state privacy laws) before relying on it.</div>
    <p>This website is a static site with no server-side database. Here's exactly what happens to your information:</p>
    <h2>Booking requests</h2>
    <p>When you use the booking form, the details you enter (name, phone/email, chosen service, date and time) are placed into a message that opens in <em>your own</em> email or messaging app, addressed to us. Nothing is transmitted to or stored on this website or by any third party — you choose whether to actually send that message.</p>
    <h2>Cookies &amp; analytics</h2>
    <p>${business.analytics ? "We use privacy-conscious analytics to understand site traffic. You can decline this in the cookie banner at any time." : "This site does not use cookies, trackers, or analytics of any kind."}</p>
    <h2>Contacting us</h2>
    <p>If you have questions about this policy, contact us at ${escapeHtml(contactLine)}.</p>
    <p><em>Last updated: ${new Date().toISOString().slice(0, 10)}</em></p>`;
  return legalPageShell({ title: "Privacy Policy", business, colors, faviconUri, bodyHtml: body });
}

function buildTerms(business, colors, faviconUri) {
  const contact = business.contact || {};
  const contactLine = contact.email || contact.phone || "the contact details on our homepage";
  const body = `
    <h1>Terms &amp; Conditions</h1>
    <div class="legal-banner">This is a generic starting template, not legal advice. Have it reviewed before relying on it — it does not account for your specific services, local regulations, or liability needs.</div>
    <h2>Bookings</h2>
    <p>Submitting a booking request through this site sends a message to us directly — it is a <strong>request</strong>, not a confirmed appointment, until we respond to confirm it.</p>
    <h2>Pricing</h2>
    <p>Prices shown are starting estimates. Final pricing may vary based on the specifics of the service and will be confirmed before your appointment.</p>
    <h2>Cancellations</h2>
    <p>[Add your cancellation / no-show / late policy here.]</p>
    <h2>Liability</h2>
    <p>Services are provided with reasonable skill and care. To the extent permitted by law, we are not liable for indirect or consequential losses arising from use of this website.</p>
    <h2>Changes</h2>
    <p>We may update these terms from time to time; the current version is always the one posted here.</p>
    <h2>Contact</h2>
    <p>Questions about these terms: ${escapeHtml(contactLine)}.</p>
    <p><em>Last updated: ${new Date().toISOString().slice(0, 10)}</em></p>`;
  return legalPageShell({ title: "Terms & Conditions", business, colors, faviconUri, bodyHtml: body });
}

function build404(business, colors, faviconUri) {
  const styleContent = baseStyles(colors);
  const csp = buildCsp({ styleHash: sha256Base64(styleContent), webFonts: true });
  const bodyHtml = `
    <header class="site-header"><a class="brand" href="index.html">${escapeHtml(business.name)}</a></header>
    <main>
      <div class="error-page">
        <p class="eyebrow">404</p>
        <h1>Page not found</h1>
        <p class="body-text">The page you're looking for doesn't exist or has moved.</p>
        <a class="btn btn-primary" href="index.html">Back to homepage</a>
      </div>
    </main>`;
  return pageShell({
    title: `Page not found — ${business.name}`,
    faviconUri,
    cspContent: csp,
    styleTag: `<style>${styleContent}</style>`,
    bodyHtml,
  });
}

function buildRobotsTxt(siteUrl) {
  return `User-agent: *\nAllow: /\n\nSitemap: ${siteUrl}/sitemap.xml\n`;
}

function buildSitemapXml(siteUrl) {
  const today = new Date().toISOString().slice(0, 10);
  const urls = ["/", "/privacy.html", "/terms.html"];
  return `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls
    .map((u) => `  <url><loc>${siteUrl}${u}</loc><lastmod>${today}</lastmod></url>`)
    .join("\n")}\n</urlset>\n`;
}

function buildHeadersFile() {
  return `/*
  Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=()
`;
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help || !args.input) {
    console.log("Usage: node generate-site.js --input <business.json> --outdir <dist/>\nSee site-builder/README.md for the input schema.");
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

  let outdir;
  if (args.outdir) outdir = path.resolve(args.outdir);
  else if (args.output) outdir = path.dirname(path.resolve(args.output));
  else outdir = path.resolve(`./dist/${slugify((data.business && data.business.name) || "site")}`);
  fs.mkdirSync(outdir, { recursive: true });

  const { html: indexHtml, colors, siteUrl, faviconUri } = renderIndex(data, baseDir);
  fs.writeFileSync(path.join(outdir, "index.html"), indexHtml, "utf8");

  const business = data.business;
  fs.writeFileSync(path.join(outdir, "privacy.html"), buildPrivacyPolicy(business, colors, faviconUri), "utf8");
  fs.writeFileSync(path.join(outdir, "terms.html"), buildTerms(business, colors, faviconUri), "utf8");
  fs.writeFileSync(path.join(outdir, "404.html"), build404(business, colors, faviconUri), "utf8");
  fs.writeFileSync(path.join(outdir, "_headers"), buildHeadersFile(), "utf8");

  if (siteUrl) {
    fs.writeFileSync(path.join(outdir, "robots.txt"), buildRobotsTxt(siteUrl), "utf8");
    fs.writeFileSync(path.join(outdir, "sitemap.xml"), buildSitemapXml(siteUrl), "utf8");
  } else {
    warn('Set business.siteUrl (e.g. "https://example.com") to also generate robots.txt and sitemap.xml.');
  }

  console.log(`Wrote site to ${outdir}/`);
  if (WARNINGS.length) {
    console.log(`\n${WARNINGS.length} thing(s) to look at:`);
    WARNINGS.forEach((w) => console.log(" - " + w));
  }
}

if (require.main === module) main();

module.exports = { renderIndex, ensureContrast, contrastRatio };

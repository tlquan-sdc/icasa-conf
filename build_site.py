#!/usr/bin/env python3
"""Rebuild the current ICASA conference website. Run: python build_site.py"""

from pathlib import Path
import html
import json
import sys

sys.dont_write_bytecode = True
from conference_config import CONFERENCE

ROOT = Path(__file__).resolve().parent
SERIES = CONFERENCE["series_name"]
YEAR = str(CONFERENCE["year"])
SITE_NAME = f"{SERIES} {YEAR}"
NAME = CONFERENCE["full_name"]
ORGANIZER = CONFERENCE["organizer"]
SOCIAL_IMAGE = CONFERENCE["social_image"]
HERO_IMAGE = CONFERENCE["hero_image"]
LOGO_IMAGE = CONFERENCE["logo_image"]
SITE_URL = CONFERENCE["site_url"]
CMT_URL = CONFERENCE["cmt_url"]
CONTACT_EMAIL = CONFERENCE["contact_email"]
PUBLICATION = CONFERENCE["publication"]
SHOW_PUBLICATION = bool(PUBLICATION.get("visible", False))
TRACKS = CONFERENCE["tracks"]
NAV = [
    ("index.html", "Home"), ("committee.html", "Committee"),
    ("keynote-speakers.html", "Keynotes"), ("call-for-papers.html", "Call for Papers"),
    ("important-dates.html", "Dates"), ("registration.html", "Attendees"),
    ("venue.html", "Venue"), ("contact.html", "Contact"),
]


def logo():
    partners = "".join(
        f'<img src="{html.escape(item["src"], quote=True)}" alt="" '
        f'width="{int(item["width"])}" height="{int(item["height"])}">'
        for item in CONFERENCE["partner_logos"]
    )
    return f'''<a class="brand" href="index.html" aria-label="{SITE_NAME} home">
      <span class="conference-logo" aria-hidden="true"><img src="{LOGO_IMAGE}" alt="" width="512" height="512"></span>
      <span class="brand-copy"><strong>{SITE_NAME}</strong><small>AI · Agriculture · ASEAN</small></span>
      <span class="brand-partners" aria-hidden="true">{partners}</span>
    </a>'''


def cmt_cta(label="Open Microsoft CMT portal"):
    if CMT_URL:
        url = html.escape(CMT_URL, quote=True)
        return f'<a class="btn primary" href="{url}" target="_blank" rel="noopener noreferrer">{html.escape(label)} <span>↗</span></a>'
    return '<span class="btn primary disabled" aria-disabled="true">Microsoft CMT · Available soon</span>'


def edition_links():
    archived = "".join(
        f'<a href="{html.escape(item["url"], quote=True)}">{int(item["year"])} archive</a>'
        for item in CONFERENCE.get("past_editions", [])
    )
    return (
        '<div><h3>Editions</h3><div class="footer-links edition-links">'
        f'<span><strong>{YEAR}</strong> Current edition</span>{archived}</div></div>'
    )


def contact_strip():
    domain = SITE_URL.removeprefix("https://").removeprefix("http://").rstrip("/")
    email = html.escape(CONTACT_EMAIL)
    email_href = html.escape(CONTACT_EMAIL, quote=True)
    site_href = html.escape(SITE_URL, quote=True)
    return f'''<section class="contact-strip" aria-label="Official conference contact channels"><div class="container contact-strip-grid">
      <a href="mailto:{email_href}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5.5h18v13H3zM4 7l8 6 8-6"/></svg><span><small>Email</small><strong>{email}</strong></span></a>
      <a href="{site_href}" target="_blank" rel="noopener noreferrer"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/></svg><span><small>Official website</small><strong>{html.escape(domain)}</strong></span></a>
    </div></section>'''


def wrap(page, title, body, description):
    site_root = SITE_URL.rstrip("/")
    page_url = f"{site_root}/{page}" if site_root else page
    social_image_url = f"{site_root}/{SOCIAL_IMAGE}" if site_root else SOCIAL_IMAGE
    nav = "".join(
        f'<a href="{url}" class="{"active" if url == page else ""}" '
        f'{"aria-current=\"page\"" if url == page else ""}>{label}</a>'
        for url, label in NAV
    )
    return f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#102e4a">
<meta name="description" content="{html.escape(description, quote=True)}">
<title>{html.escape(title)} | {SITE_NAME}</title>
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{html.escape(title, quote=True)} | {SITE_NAME}">
<meta property="og:description" content="{html.escape(description, quote=True)}">
<meta property="og:url" content="{html.escape(page_url, quote=True)}">
<meta property="og:image" content="{html.escape(social_image_url, quote=True)}">
<meta property="og:image:width" content="{CONFERENCE['social_image_width']}">
<meta property="og:image:height" content="{CONFERENCE['social_image_height']}">
<meta property="og:image:alt" content="{CONFERENCE['city']}, host city of {SITE_NAME}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title, quote=True)} | {SITE_NAME}">
<meta name="twitter:description" content="{html.escape(description, quote=True)}">
<meta name="twitter:image" content="{html.escape(social_image_url, quote=True)}">
<link rel="icon" type="image/png" sizes="192x192" href="assets/favicon-icasa.png?v=2027-9">
<link rel="apple-touch-icon" href="assets/favicon-icasa.png?v=2027-9">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet">
<script>document.documentElement.classList.add('js','is-loading');window.__ICASA_LOAD_START=performance.now();setTimeout(function(){{document.documentElement.classList.remove('is-loading')}},1000);</script>
<link rel="stylesheet" href="assets/style.css?v={YEAR}-29">
<link rel="stylesheet" href="assets/enhancements.css?v={YEAR}-29">
<style>
.hero{{background-image:linear-gradient(90deg,rgb(244 241 232 / .82) 0%,rgb(244 241 232 / .68) 42%,rgb(244 241 232 / .38) 100%),linear-gradient(0deg,rgb(244 241 232 / .66) 0%,transparent 48%),url("{html.escape(HERO_IMAGE, quote=True)}")}}
@media(max-width:580px){{.hero{{background-image:linear-gradient(90deg,rgb(244 241 232 / .92),rgb(244 241 232 / .67)),linear-gradient(0deg,rgb(244 241 232 / .82),transparent 48%),url("{html.escape(HERO_IMAGE, quote=True)}")}}}}
</style>
<script src="assets/site-data.js?v={YEAR}-29" defer></script><script src="assets/main.js?v={YEAR}-29" defer></script>
</head><body data-page="{page}">
<div class="site-loader" role="status" aria-label="Loading {SITE_NAME}"><div class="loader-emblem" aria-hidden="true"><span class="loader-orbit"></span><span class="loader-logo"><img src="{LOGO_IMAGE}" alt="" width="512" height="512"></span></div><div class="loader-copy"><strong>{SITE_NAME}</strong><span>AI · Agriculture · ASEAN</span></div><span class="loader-progress" aria-hidden="true"><i></i></span></div>
<a class="skip-link" href="#main-content">Skip to main content</a>
<div class="reading-progress" aria-hidden="true"><span></span></div>
<div class="utility"><div class="container utility-inner"><span>{SITE_NAME} · Official conference website</span><span>{CONFERENCE['city']} time <strong data-live-time>{CONFERENCE['timezone_label']}</strong></span></div></div>
<header class="site-header" data-header><div class="container nav-container">{logo()}
<button class="nav-toggle" aria-expanded="false" aria-label="Open navigation" aria-controls="primary-nav" data-menu-toggle><span class="hamburger" aria-hidden="true"><i></i><i></i><i></i></span></button>
<nav class="site-nav" id="primary-nav" aria-label="Main navigation" data-site-nav>{nav}</nav></div></header>
<main id="main-content">{body}</main>
{contact_strip()}
<footer class="footer"><div class="container"><div class="footer-lead"><div><span class="section-label">{SERIES} / {YEAR}</span><h2>Research for agriculture,<br>grounded in the region.</h2></div><a class="text-link light" href="contact.html">Contact the host institution <span>↗</span></a></div><div class="footer-grid"><div>{logo()}<p>{NAME}. {CONFERENCE['edition_label']} in {CONFERENCE['city']}, {CONFERENCE['country']}.</p></div><div><h3>Conference</h3><div class="footer-links"><a href="call-for-papers.html">Call for Papers</a><a href="important-dates.html">Important Dates</a><a href="committee.html">Committee</a><a href="registration.html">For Attendees</a></div></div>{edition_links()}<div><h3>Host institution</h3><p>{ORGANIZER}<br>{CONFERENCE['city']}, {CONFERENCE['country']}</p><a href="{CONFERENCE['organizer_url']}" target="_blank" rel="noopener noreferrer">Official organiser website ↗</a></div></div><div class="copyright"><span>© {YEAR} {SERIES} · All rights reserved</span><span>Last updated · {CONFERENCE['last_updated']}</span></div></div></footer>
<button class="to-top" type="button" aria-label="Back to top" data-to-top>↑</button>
</body></html>'''


def page_head(title, description, crumb):
    positions = {
        "Committee": 2,
        "Keynotes": 3,
        "Call for Papers": 4,
        "Dates": 5,
        "Attendees": 6,
        "Venue": 7,
        "Contact": 8,
    }
    position = positions[crumb]
    page_number = f"Section {position:02d} / 08"
    return f'''<section class="page-head"><div class="container">
      <div class="page-head-meta"><nav class="breadcrumb" aria-label="Breadcrumb"><a href="index.html">{SITE_NAME}</a><span aria-hidden="true">/</span><span aria-current="page">{html.escape(crumb)}</span></nav><span class="page-index" aria-label="Page {position} of 8">{page_number}</span></div>
      <div class="page-title-grid"><div><span class="section-label">{html.escape(crumb)}</span><h1>{html.escape(title)}</h1></div><p class="intro">{html.escape(description)}</p></div>
    </div></section>'''


def aside():
    return '''<aside class="aside-card" data-reveal><span class="section-label">Conference information</span><h3>Official updates</h3><p>Dates, submission instructions and attendee information are updated here as they are announced.</p><div class="aside-links"><a href="important-dates.html">Important dates →</a><a href="contact.html">Host institution →</a></div></aside>'''


def inner(content):
    return f'<div class="container inner-grid"><div class="prose" data-reveal>{content}</div>{aside()}</div>'


def gallery_section():
    """Render only verified conference photos configured for this edition."""
    photos = CONFERENCE.get("gallery", [])
    if not photos:
        return ""

    cards = []
    for photo in photos:
        src = html.escape(photo["src"], quote=True)
        alt = html.escape(photo["alt"], quote=True)
        caption = html.escape(photo.get("caption", ""))
        width = int(photo.get("width", 1600))
        height = int(photo.get("height", 1067))
        figcaption = f"<figcaption>{caption}</figcaption>" if caption else ""
        cards.append(
            f'<figure class="gallery-item" data-reveal>'
            f'<img src="{src}" alt="{alt}" width="{width}" height="{height}" loading="lazy" decoding="async">'
            f'{figcaption}</figure>'
        )

    return f'''<section class="gallery-section" aria-labelledby="gallery-title"><div class="container">
      <div class="gallery-heading" data-reveal><div><span class="section-label">Conference moments</span><h2 id="gallery-title">Inside {SITE_NAME}</h2></div><p>People, presentations and exchanges from the conference community.</p></div>
      <div class="gallery-grid">{"".join(cards)}</div>
    </div></section>'''


def home_track_items():
    featured = [track for track in TRACKS if track.get("featured")]
    return "".join(
        f'<li data-reveal><span>{index:02d}</span>'
        f'<h3>{html.escape(track["title"])}</h3>'
        f'<p>{html.escape(track["description"])}</p></li>'
        for index, track in enumerate(featured, 1)
    )


def cfp_track_items():
    return "".join(
        f'<li>{html.escape(track["title"])}</li>'
        for track in TRACKS
    )


def registration_fee_table():
    fees = CONFERENCE["registration_fees"]
    rows = "".join(
        f'<tr><th scope="row">{html.escape(item["category"])}</th>'
        f'<td>{html.escape(item["early"])}</td>'
        f'<td>{html.escape(item["late"])}</td></tr>'
        for item in fees["rows"]
    )
    return f'''<div class="fee-table-wrap" role="region" aria-label="Registration fees" tabindex="0">
      <table class="fee-table"><caption>{SITE_NAME} registration fees</caption>
      <thead><tr><th scope="col">Registration type</th><th scope="col">{html.escape(fees['early_label'])}</th><th scope="col">{html.escape(fees['late_label'])}</th></tr></thead>
      <tbody>{rows}</tbody></table></div>'''


def registration_information():
    return '''<div class="registration-information">
      <section class="registration-notes" aria-labelledby="registration-notes-heading">
        <h3 id="registration-notes-heading">Important Notes</h3>
        <ul>
          <li>The <a href="https://cmt3.research.microsoft.com/" target="_blank" rel="noopener noreferrer">Microsoft CMT</a> service was used for managing the peer-reviewing process for this conference. This service was provided for free by Microsoft and they bore all expenses, including costs for Azure cloud services as well as for software development and support.</li>
          <li>The conference registration fee includes admission to all conference sessions, coffee break refreshments, lunches, the Banquet, and a copy of the Conference Abstract.</li>
          <li>For attendance: one-day registration ($25 = 640,000 VND/day) is registered and paid at the conference.</li>
          <li>The registration fee covers papers of up to 10 pages. Each page beyond 10 pages is subject to an additional fee of $15 (385,000 VND) per page.</li>
          <li>15% similarity is acceptable.</li>
          <li>If a paper is not presented at the conference, it will not be included in the proceedings.</li>
        </ul>
      </section>
      <aside class="registration-benefits" aria-labelledby="registration-benefits-heading">
        <span class="section-label">Included with registration</span>
        <h3 id="registration-benefits-heading">Registration Benefits</h3>
        <ul>
          <li>Admission to the Scientific Sessions</li>
          <li>Coffee Breaks</li>
          <li>Lunches</li>
          <li>A Certificate of Attendance</li>
        </ul>
      </aside>
    </div>'''


def submission_guidelines():
    return f'''<h3 id="submission-guidelines">Requirements</h3>
      <p>Manuscripts must follow the official conference instructions. Authors should check the formatting requirements carefully before submitting a paper.</p>
      <ul class="guideline-list">
        <li>The registration fee covers papers of up to 10 pages. Each page beyond 10 pages is subject to an additional fee of $15 (385,000 VND) per page.</li>
        <li>Papers must be written in English.</li>
        <li>Submissions must be original, not previously published and not under review elsewhere.</li>
        <li>The manuscript must fit at least one official {SITE_NAME} conference track.</li>
        <li>Use the official conference manuscript template when it becomes available and submit the review manuscript as a PDF with all fonts embedded.</li>
        <li>Enter the title, abstract, author names, affiliations, email addresses and topics accurately in Microsoft CMT.</li>
      </ul>
      <div class="notice-line">The review model, PDF file-size limit and supplementary-material policy will be published here when confirmed.</div>'''


def submission_resources():
    if not SHOW_PUBLICATION:
        return ""
    return '''<div class="submission-resources" aria-label="Springer Nature author resources">
      <a href="https://www.springernature.com/gp/authors/publish-a-book/step-by-step-conference-proceedings" target="_blank" rel="noopener noreferrer"><span>01 · Guidelines</span><strong>Springer proceedings instructions</strong><small>Official author guidance and technical requirements</small></a>
      <a href="https://resource-cms.springernature.com/springer-cms/rest/v1/content/19238648/data/v8" target="_blank" rel="noopener noreferrer"><span>02 · LaTeX</span><strong>LaTeX template package</strong><small>Official Springer Nature proceedings files</small></a>
      <a href="https://www.springernature.com/gp/authors/publish-a-book/step-by-step-conference-proceedings" target="_blank" rel="noopener noreferrer"><span>03 · Microsoft Word</span><strong>Word template</strong><small>Download from the official author resources page</small></a>
      <a href="https://www.springernature.com/gp/authors/publish-a-book/step-by-step-conference-proceedings" target="_blank" rel="noopener noreferrer"><span>04 · After acceptance</span><strong>Publishing agreement</strong><small>The applicable agreement will be confirmed for accepted papers</small></a>
    </div>'''


def paper_submission_details():
    return f'''<div class="paper-submission">
      {submission_guidelines()}
{f'<h3>Templates and author resources</h3>{submission_resources()}' if SHOW_PUBLICATION else ''}
      <h3>Submission procedure</h3>
      <p>All full papers must be submitted through the official {SITE_NAME} Microsoft Conference Management Toolkit (CMT) portal. Do not submit through a CMT link belonging to another conference.</p>
      <div class="submission-card"><div><span class="section-label">Official submission portal</span><h3>{SITE_NAME} on Microsoft CMT</h3><p>{'Submit your paper through the official conference-specific portal.' if CMT_URL else 'The conference-specific URL will be activated here after the ICASA workspace is approved.'}</p></div>{cmt_cta("Submit via Microsoft CMT")}</div>
      <h3>Submission process</h3>
      <ol class="attendee-steps submission-steps">
        <li><span>01</span><div><strong>Create or access your account</strong><p>Create a Microsoft CMT account or sign in with the email address you will use for conference correspondence.</p></div></li>
        <li><span>02</span><div><strong>Open the ICASA 2027 portal</strong><p>Use only the conference-specific link published on this website and review the current submission instructions.</p></div></li>
        <li><span>03</span><div><strong>Prepare the manuscript</strong><p>Use the official conference template when available, convert the paper to PDF and ensure that all fonts are embedded.</p></div></li>
        <li><span>04</span><div><strong>Create a new submission</strong><p>Open the Author Console, enter the title, abstract, authors, affiliations and relevant conference topics, then upload the PDF manuscript.</p></div></li>
        <li><span>05</span><div><strong>Add supporting files if requested</strong><p>Upload supplementary material only when permitted by the final submission policy.</p></div></li>
        <li><span>06</span><div><strong>Review and confirm</strong><p>Check all metadata and files before finalising the submission. Retain the paper ID and confirmation email.</p></div></li>
      </ol>
      <div class="post-submission">
        <div><span>Revisions</span><p>Submit a revised manuscript through the same paper record when requested and before the stated deadline.</p></div>
        <div><span>Communication</span><p>Check your registered email address and the CMT Author Console regularly for decisions and reviewer comments.</p></div>
        <div><span>Final submission</span><p>Accepted papers must satisfy the camera-ready, publishing-agreement, registration and presentation requirements.</p></div>
      </div>
      <div class="submission-contact"><span class="section-label">Submission enquiries</span><strong><a href="mailto:{html.escape(CONTACT_EMAIL, quote=True)}">{html.escape(CONTACT_EMAIL)}</a></strong><a class="text-link" href="contact.html">Contact information <span>→</span></a></div>
    </div>'''


home = f'''
<section class="hero"><div class="container hero-grid">
  <div class="hero-main" data-reveal><span class="section-label">International conference · {CONFERENCE['edition_label']}</span><h1><span>{SERIES}</span><strong>{YEAR}</strong></h1><p class="conference-name">{NAME}</p><div class="hero-location" aria-label="Conference location"><span><small>Coordinates</small><strong>{CONFERENCE['latitude']}° N · {CONFERENCE['longitude']}° E</strong></span><span><small>Destination</small><strong>{CONFERENCE['city']} · {CONFERENCE['country']}</strong></span><span><small>Setting</small><strong>{CONFERENCE['setting']} · {CONFERENCE['conference_period']}</strong></span></div></div>
  <div class="hero-side" data-reveal><div class="edition-code" aria-hidden="true"><span>{CONFERENCE['edition_number']}</span><small>{CONFERENCE['edition_label']}</small></div><p>An academic forum for researchers and practitioners working across artificial intelligence, agriculture and sustainable regional development.</p><div class="actions"><a class="btn primary" href="call-for-papers.html">Call for Papers <span>↗</span></a><a class="btn text" href="important-dates.html">View timeline <span>→</span></a></div><dl class="event-facts"><div><dt>Host city</dt><dd>{CONFERENCE['city']}, {CONFERENCE['country']}</dd></div><div><dt>Conference</dt><dd>{CONFERENCE['conference_period']}</dd></div><div><dt>Paper deadline</dt><dd>{CONFERENCE['submission_deadline']}</dd></div><div><dt>Organiser</dt><dd>{CONFERENCE['organizer_short']}</dd></div></dl></div>
</div><div class="hero-rule" aria-hidden="true"><span></span><i></i><span></span><i></i><span></span></div></section>
<section class="section" data-reveal><div class="container editorial-grid"><div><span class="section-label">Purpose</span><h2>From research question<br>to field application.</h2></div><div class="prose-large"><p>{SERIES} brings together computer science, agricultural engineering, environmental research and regional development communities.</p><p>This edition focuses on the conditions that make technology useful in practice: local data, responsible deployment, resilient farming systems and collaboration across ASEAN.</p><a class="text-link" href="committee.html">How the conference is organised <span>→</span></a></div></div></section>
<section class="section themes"><div class="container"><div class="section-heading" data-reveal><span class="section-label">Conference scope</span><h2>Research themes</h2><p>Featured areas from a broader interdisciplinary programme spanning AI, agricultural engineering, life sciences and regional innovation.</p></div><ol class="theme-list">{home_track_items()}</ol><a class="text-link" href="call-for-papers.html">Explore all {len(TRACKS)} conference tracks <span>→</span></a></div></section>
<section class="section deadlines"><div class="container deadline-grid"><div data-reveal><span class="section-label">Conference timeline</span><h2>Key milestones</h2><p>Submission, notification, registration and conference dates are maintained on the Important Dates page.</p><a class="text-link light" href="important-dates.html">Full timeline <span>→</span></a></div><div class="deadline-list" data-deadlines data-limit="4"><noscript>Enable JavaScript to view the conference timeline.</noscript></div></div></section>
{gallery_section()}
<section class="identity-section" id="institutional-network"><div class="container"><div class="identity-heading" data-reveal><div><span class="section-label">Institutional network</span><h2>Host, organiser<br>and partner institutions.</h2></div><p>Official institutional and partner information for the current conference edition.</p></div><div class="identity-grid">
  <a class="identity-card" href="https://www.udn.vn/" target="_blank" rel="noopener noreferrer" data-reveal><span class="identity-kicker">Host university</span><span class="identity-logo udn"><img src="assets/udn-logo.webp" alt="The University of Danang logo" width="640" height="640"></span><strong>The University of Danang</strong><small>Institutional identity</small></a>
  <a class="identity-card" href="https://sdc.udn.vn/" target="_blank" rel="noopener noreferrer" data-reveal><span class="identity-kicker">Organising unit</span><span class="identity-logo sdc"><img src="assets/sdc-logo.jpg" alt="Software Development Centre logo" width="500" height="500"></span><strong>Software Development Centre</strong><small>SDC · The University of Danang</small></a>
  <a class="identity-card" href="https://www.southernleytestateu.edu.ph/index.php/en/" target="_blank" rel="noopener noreferrer" data-reveal><span class="identity-kicker">Partner university</span><span class="identity-logo slsu"><img src="assets/Southern_Leyte_State_University.png" alt="Southern Leyte State University logo" width="3349" height="3352"></span><strong>Southern Leyte State University</strong><small>SLSU · Philippines</small></a>
  <a class="identity-card" href="https://bipsu.edu.ph/" target="_blank" rel="noopener noreferrer" data-reveal><span class="identity-kicker">Partner university</span><span class="identity-logo bipsu"><img src="assets/BiPSU.jpg" alt="Biliran Province State University logo" width="564" height="543"></span><strong>Biliran Province State University</strong><small>BiPSU · Philippines</small></a>
  <a class="identity-card" href="https://wlcormoc.edu.ph/" target="_blank" rel="noopener noreferrer" data-reveal><span class="identity-kicker">Partner institution</span><span class="identity-logo wlc"><img src="assets/logo Western Leyte College of Ormoc.png" alt="Western Leyte College of Ormoc City logo" width="600" height="300"></span><strong>Western Leyte College of Ormoc City</strong><small>WLC · Philippines</small></a>
  <a class="identity-card" href="https://ucu.edu.ph/" target="_blank" rel="noopener noreferrer" data-reveal><span class="identity-kicker">Partner university</span><span class="identity-logo ucu"><img src="assets/urdaneta city university.png" alt="Urdaneta City University logo" width="400" height="500"></span><strong>Urdaneta City University</strong><small>UCU · Philippines</small></a>
  <a class="identity-card" href="https://www.vsu.edu.ph/" target="_blank" rel="noopener noreferrer" data-reveal><span class="identity-kicker">Partner university</span><span class="identity-logo vsu"><img src="assets/VSU Logo 2016-67f38a29.png" alt="Visayas State University logo" width="2444" height="2444"></span><strong>Visayas State University</strong><small>VSU · Philippines</small></a>
</div></div></section>
<section class="sponsors-section" data-sponsors-section hidden><div class="container"><div class="sponsors-heading"><div><span class="section-label">Conference support</span><h2>Sponsors</h2></div><p>Confirmed sponsors and supporters will appear here after agreement and logo-use approval.</p></div><div class="sponsor-rail" data-sponsors></div></div></section>
<section class="host-band"><div class="container host-grid" data-reveal><div><span class="section-label">Host city</span><strong>{CONFERENCE['city'].upper()}</strong></div><p>{CONFERENCE['region']}<br>{CONFERENCE['latitude']}° N · {CONFERENCE['longitude']}° E</p><div><span class="section-label">Organiser</span><p>{ORGANIZER}</p></div><a class="btn inverse" href="venue.html">Venue information <span>→</span></a></div></section>'''


committee_members = [
    ("leadership", "General Chair", "Nguyen Ha Huy Cuong, Ph.D.", "Software Development Centre (SDC), The University of Danang", "VietNam"),
    ("leadership", "General Co-Chair", "Phayung Meesad, Assoc. Prof.", "King Mongkut's University of Technology North Bangkok (KMUTNB)", "Thailand"),
    ("leadership", "General Co-Chair", "Akhilesh Kumar Sharma, Prof. (Dr.)", "Manipal University Jaipur", "INDIA"),
    ("leadership", "General Co-Chair", "Cao Xuan Tuan, Ph.D.", "The University of Danang", "VietNam"),
    ("advisory", "International Advisory Committee", "Czarina Ancella G. Gabi, Ph.D.", "Southern Leyte State University", "Philippines"),
    ("advisory", "International Advisory Committee", "Surapaneni Phani Praveen, Assoc. Prof.", "Prasad V. Potluri Siddhartha Institute of Technology", "India"),
    ("program", "Technical Programme Chair", "Sakchai Tangwanwit, Ph.D.", "King Mongkut's University of Technology North Bangkok (KMUTNB)", "Thailand"),
    ("program", "Technical Programme Co-Chair", "Nguyen Si Thin, Ph.D.", "Vietnam-Korea University of Information and Communication Technology (VKU), The University of Danang", "VietNam"),
    ("program", "Technical Programme Co-Chair", "Reynold G. Bustillo, Ph.D.", "Biliran Province State University (BiPSU)", "Philippines"),
    ("program", "Technical Programme Committee", "Vu Thi Phuong Anh, Assoc. Prof. Dr.", "Da Nang College", "VietNam"),
    ("program", "Technical Programme Committee", "Reymon M. Santiañez, Ph.D.", "Biliran Province State University (BiPSU)", "Philippines"),
    ("program", "Technical Programme Committee", "Monalee A. dela Cerna, Ph.D.", "Surigao del Norte State University", "Philippines"),
    ("program", "Technical Programme Committee", "Tran Van Dai, Ph.D.", "Vietnam-Korea University of Information and Communication Technology (VKU), The University of Danang", "VietNam"),
    ("program", "Technical Programme Committee", "Ho Van Hung, Ph.D.", "The University of DaNang – Center for Information Technology and Digital Learning Resources", "VietNam"),
    ("program", "Technical Programme Committee", "Hoang Manh Ha, Ph.D.", "Institute of Digital Technology, Thu Dau Mot University", "VietNam"),
    ("program", "Technical Programme Committee", "Adel Grace Prima Gaudicos, Ph.D.", "Southern Leyte State University", "Philippines"),
    ("program", "Technical Programme Committee", "Tzung-Pei Hong, Prof. Dr.", "National University of Kaohsiung", "Taiwan"),
    ("program", "Technical Programme Committee", "David Camacho, Prof. Dr.", "Universidad Autónoma de Madrid", "Spain"),
    ("program", "Technical Programme Committee", "Nitesh Chawla, Prof. Dr.", "University of Notre Dame", "USA"),
    ("program", "Technical Programme Committee", "Kang-Hyun Jo, Prof. Dr.", "University of Ulsan", "South Korea"),
    ("program", "Technical Programme Committee", "Lipo Wang, Prof. Dr.", "Nanyang Technological University", "Singapore"),
    ("program", "Technical Programme Committee", "Chia Nan Wang, Prof. Dr.", "National Kaohsiung University of Science and Technology", "Taiwan"),
    ("program", "Technical Programme Committee", "Gwanggil Jeon, Prof. Dr.", "Incheon National University", "Korea"),
    ("program", "Technical Programme Committee", "Herwig Unger, Prof. Dr.", "University of Hagen", "Germany"),
    ("program", "Technical Programme Committee", "Ian Celmar Alicaya Avila, Ph.D.", "Western Leyte College of Ormoc", "Philippines"),
    ("program", "Technical Programme Committee", "Rhoderick Darganttes Malangsa, Professor", "Southern Leyte State University (SLSU)", "Philippines"),
    ("program", "Technical Programme Committee", "Thittaporn Ganokratanaa, Asst. Prof. Dr.", "King Mongkut's University of Technology Thonburi", "Thailand"),
    ("program", "Technical Programme Committee", "Tran Hoang Vu, Ph.D.", "The University of Danang", "VietNam"),
    ("program", "Technical Programme Committee", "Ly Quynh Tran, Ph.D.", "Vietnam-Korea University of Information and Communication Technology (VKU), The University of Danang", "VietNam"),
    ("program", "Technical Programme Committee", "Ninh Khanh Duy, Ph.D.", "The University of Danang", "VietNam"),
    ("program", "Technical Programme Committee", "Bui Thanh Khiet, Ph.D.", "Thu Dau Mot University", "VietNam"),
    ("program", "Technical Programme Committee", "Las Johansen B. Caluza, Prof., Ph.D., DIT", "Leyte Normal University", "Philippines"),
    ("program", "Technical Programme Committee · Associate Professor · V Dean, Faculty of Computing", "DR. JUDE B. ROLA", "Visayas State University", "Philippines"),
    ("program", "Technical Programme Committee · Dean, College of Information Communications Technology and Engineering", "Cheryl Montederamos Tarre", "Western Leyte College of Ormoc", "Philippines"),
    ("program", "Technical Programme Committee", "PGS.TS Võ Trung Hùng", "Trường Đại học Sư phạm kỹ thuật, ĐHĐN", "VietNam"),
    ("program", "Technical Programme Committee", "PGS.TS Nguyễn Thanh Bình", "Trường Đại học Công nghệ Thông tin và Truyền thông Việt - Hàn - VKU, Đại học Đà Nẵng", "VietNam"),
    ("publication", "Publication Chair", "Jannie Fleur V. Oraño, Ph.D.", "Southern Leyte State University", "Philippines"),
    ("publication", "Publicity & International Relations Chair", "Ingrid Uy, Ph.D.", "Southern Leyte State University", "Philippines"),
    ("publication", "International Liaison Co-Chair", "Sonny Soriano, Ph.D.", "Urdaneta City University", "Philippines"),
    ("publication", "Publicity Committee", "Ho Phan Hieu, Ph.D.", "The University of Danang", "VietNam"),
    ("publication", "Publicity Committee", "Tran Thi Phu, Ph.D.", "The University of Danang", "VietNam"),
    ("publication", "Publication & International Relations Committee", "Thien Khai Tran, Ph.D.", "Ho Chi Minh City University of Economics and Finance (UEF)", "VietNam"),
    ("organizing", "Local Organizing Committee", "Tran Nu Nhu Quynh", "Software Development Centre (SDC), The University of Danang", "VietNam"),
    ("organizing", "Local Organizing Committee", "Truong Luu Quan", "Software Development Centre (SDC), The University of Danang", "VietNam"),
    ("organizing", "Local Organizing Committee", "Tran Anh Kiet, M.Sc.", "The University of Danang", "VietNam"),
]
committee_category_labels = {
    "leadership": "Leadership",
    "advisory": "International advisory",
    "program": "Technical programme",
    "publication": "Publication & relations",
    "organizing": "Local organisation",
}
committee_groups = [
    ("leadership", "Conference leadership"),
    ("advisory", "International Advisory Committee"),
    ("program", "Technical Programme Committee"),
    ("publication", "Publication & International Relations"),
    ("organizing", "Local Organising Committee"),
]
numbered_committee_members = list(enumerate(committee_members, 1))
committee_groups_html = ""
for category, group_title in committee_groups:
    group_members = [item for item in numbered_committee_members if item[1][0] == category]
    group_cards = "".join(
        f'''<article class="committee-card{' committee-card--primary' if member_number == 1 else ''}" data-committee-category="{member_category}" data-reveal>
          <div class="committee-card-head"><span class="member-number">{member_number:02d}</span><span class="category">{html.escape(committee_category_labels[member_category])}</span></div>
          <h4 class="member-role">{html.escape(role)}</h4>
          <strong class="member-name">{html.escape(name)}</strong>
          <p class="member-affiliation">{html.escape(institution)}<span>{html.escape(country)}</span></p>
        </article>'''
        for member_number, (member_category, role, name, institution, country) in group_members
    )
    committee_groups_html += f'''<section class="committee-group committee-group--{category}" data-committee-group="{category}">
      <header class="committee-group-head">
        <div><span class="section-label">Organisation level</span><h3>{html.escape(group_title)}</h3></div>
        <span class="committee-group-count">{len(group_members):02d} members</span>
      </header>
      <div class="committee-group-grid">{group_cards}</div>
    </section>'''

committee = page_head("Conference Committee", "Leadership, advisory, technical programme and organising committee members for ICASA 2027.", "Committee") + f'''<section class="content committee-section"><div class="container"><div class="section-heading split"><div><span class="section-label">Leadership and programme</span><h2>Conference organisation</h2></div><span class="status" data-committee-count aria-live="polite">{len(committee_members)} committee members</span></div><div class="filters" role="group" aria-label="Filter committee groups" data-filter-group><button type="button" class="filter active" data-filter="all" aria-pressed="true">All</button><button type="button" class="filter" data-filter="leadership" aria-pressed="false">Leadership</button><button type="button" class="filter" data-filter="advisory" aria-pressed="false">International advisory</button><button type="button" class="filter" data-filter="program" aria-pressed="false">Technical programme</button><button type="button" class="filter" data-filter="publication" aria-pressed="false">Publication & relations</button><button type="button" class="filter" data-filter="organizing" aria-pressed="false">Local organisation</button></div><div class="committee-directory" data-committee-directory>{committee_groups_html}</div><div class="callout"><p><strong>Committee information.</strong> Names, roles and institutional affiliations are presented as supplied by the conference organiser.</p></div></div></section>'''

publication_notice = ""
publication_resources_section = ""
publication_tab_button = ""
publication_panel = ""
if SHOW_PUBLICATION:
    publication_notice = f'''<div class="callout"><p><strong>Proceedings publication.</strong> The {SITE_NAME} proceedings will be published in <a href="{PUBLICATION['series_url']}" target="_blank" rel="noopener noreferrer">{PUBLICATION['series_name']} ({PUBLICATION['series_short']})</a> by {PUBLICATION['publisher']}. <strong>The {PUBLICATION['series_short']} book series is indexed in Scopus.</strong> Publication and subsequent indexing of an individual paper remain subject to peer review, author registration, presentation, publisher requirements and the policies of the indexing service.</p></div>'''
    publication_resources_section = f'''<h3>Templates and author resources</h3>{submission_resources()}'''
    publication_tab_button = '''<button type="button" role="tab" aria-selected="false" aria-controls="attendee-publication" data-attendee-tab="publication" tabindex="-1">Publication</button>'''
    publication_panel = f'''<article id="attendee-publication" class="attendee-panel" role="tabpanel" hidden><div class="panel-index">06</div><div><span class="section-label">Publication · {PUBLICATION['publisher']}</span><h2>{PUBLICATION['series_short']} proceedings</h2><p>The {SITE_NAME} proceedings will be published in <strong>{PUBLICATION['series_name']}</strong>. <strong>The {PUBLICATION['series_short']} book series is indexed in Scopus.</strong></p><div class="notice-line">Publication and subsequent indexing of an individual paper remain subject to peer review, author registration, presentation, publisher requirements and the policies of the indexing service.</div><a class="btn primary" href="{PUBLICATION['series_url']}" target="_blank" rel="noopener noreferrer">View the book series <span>↗</span></a></div></article>'''

cfp = page_head("Call for Papers", "Research scope for responsible applications of AI in smart and sustainable agriculture across ASEAN.", "Call for Papers") + '<section class="content">' + inner(f'''<span class="section-label">Conference scope</span><h2>Invitation to contribute</h2><p>The full-paper submission deadline is <strong>{CONFERENCE['submission_deadline']}</strong>. Review policies and proceedings information are maintained on this website.</p>{publication_notice}<h3>Conference tracks</h3><p>ICASA welcomes original research and applied work across the following interdisciplinary areas:</p><ol class="numbered-topics">{cfp_track_items()}</ol>{submission_guidelines()}{publication_resources_section}<h3>Submission through Microsoft CMT</h3><p>Authors create or use a Microsoft CMT account, enter the paper metadata and author list, select suitable topics, upload the manuscript and retain the paper ID for later revisions.</p><div class="submission-card"><div><span class="section-label">Submission platform</span><h3>{SITE_NAME} on Microsoft CMT</h3><p>Use only the Microsoft CMT URL published on this website.</p></div>{cmt_cta()}</div><section class="cmt-acknowledgment" aria-labelledby="cmt-acknowledgment-heading"><span class="section-label">Required public statement</span><h3 id="cmt-acknowledgment-heading">CMT Acknowledgment</h3><p>The Microsoft CMT service was used for managing the peer-reviewing process for this conference. This service was provided for free by Microsoft and they bore all expenses, including costs for Azure cloud services as well as for software development and support.</p></section>''') + '</section>'

keynotes = page_head("Keynote Speakers", "The keynote programme is being prepared for the current conference edition.", "Keynotes") + '''<section class="content"><div class="container narrow"><div class="empty-state coming-soon-state" data-reveal><span class="section-label">Keynote programme</span><span class="coming-soon-code" aria-hidden="true">Programme update · 2027</span><h2>Coming soon</h2><p>Keynote speakers, affiliations, presentation topics and session times will be published after formal confirmation.</p><a class="text-link" href="call-for-papers.html">Explore the research scope <span>→</span></a></div></div></section>'''

important = page_head("Important Dates", f"Submission and conference milestones for {SITE_NAME}.", "Dates") + f'''<section class="content"><div class="container dates-page"><div><span class="section-label">{YEAR} conference timeline</span><h2>From submission to conference</h2><p>The full-paper deadline is <strong>{CONFERENCE['submission_deadline']}</strong>. This page is the official source for notification, camera-ready, registration and conference dates.</p><a class="btn primary" href="registration.html#important-dates">Attendee information <span>→</span></a></div><div class="deadline-list full" data-deadlines><noscript>Enable JavaScript to view the conference timeline.</noscript></div></div></section>'''

registration = page_head("For Attendees", f"Practical information for authors, delegates and guests attending {SITE_NAME} in {CONFERENCE['city']}.", "Attendees") + f'''<section class="attendees-section"><div class="container">
<div class="attendee-tabs{' attendee-tabs--five' if not SHOW_PUBLICATION else ''}" role="tablist" aria-label="Attendee information" data-attendee-tabs>
  <button class="active" type="button" role="tab" aria-selected="true" aria-controls="attendee-registration" data-attendee-tab="registration">Registration</button>
  <button type="button" role="tab" aria-selected="false" aria-controls="attendee-submission" data-attendee-tab="submission" tabindex="-1">Submission</button>
  <button type="button" role="tab" aria-selected="false" aria-controls="attendee-dates" data-attendee-tab="important-dates" tabindex="-1">Important dates</button>
  <button type="button" role="tab" aria-selected="false" aria-controls="attendee-stay" data-attendee-tab="accommodation" tabindex="-1">Accommodation</button>
  <button type="button" role="tab" aria-selected="false" aria-controls="attendee-programme" data-attendee-tab="programme" tabindex="-1">Programme</button>
{publication_tab_button}
</div>
<div class="attendee-panels">
  <article id="attendee-registration" class="attendee-panel" role="tabpanel" data-reveal><div class="panel-index">01</div><div><span class="section-label">Registration</span><h2>Registration fees</h2><p>Choose the applicable attendee category and registration period. Payment instructions and cancellation terms will be published before registration opens.</p>{registration_fee_table()}<div class="notice-line">Fees are shown in USD and VND as supplied by the conference organiser. Never transfer funds through a payment link that is not published on this official website.</div>{registration_information()}</div></article>
  <article id="attendee-submission" class="attendee-panel" role="tabpanel" hidden><div class="panel-index">02</div><div><span class="section-label">Paper submission · Microsoft CMT</span><h2>Paper Submission</h2><p>The full-paper submission deadline is <strong>{CONFERENCE['submission_deadline']}</strong>. Prepare and verify every file before uploading it to the official conference portal.</p>{paper_submission_details()}</div></article>
  <article id="attendee-dates" class="attendee-panel" role="tabpanel" hidden><div class="panel-index">03</div><div><span class="section-label">Important dates</span><h2>Conference timeline</h2><p>The full-paper submission deadline is <strong>{CONFERENCE['submission_deadline']}</strong> and the conference takes place on {CONFERENCE['conference_period']}.</p><div class="deadline-list full" data-deadlines></div></div></article>
  <article id="attendee-stay" class="attendee-panel" role="tabpanel" hidden><div class="panel-index">04</div><div><span class="section-label">Accommodation</span><h2>Stay in {CONFERENCE['city']}</h2><p>Hotel, airport transfer, visa and local transport guidance will be published with the venue information.</p><div class="fact-pair"><div><span>Host city</span><strong>{CONFERENCE['city']}, {CONFERENCE['country']}</strong></div><div><span>Venue</span><strong>Coming soon</strong></div></div><a class="btn primary" href="venue.html">Venue and travel <span>→</span></a></div></article>
  <article id="attendee-programme" class="attendee-panel" role="tabpanel" hidden><div class="panel-index">05</div><div><span class="section-label">Programme</span><h2>Conference in {CONFERENCE['conference_period']}</h2><p>The scientific programme will include keynote talks, technical sessions and opportunities for regional exchange. The detailed schedule will be published here.</p><div class="programme-placeholder"><span>{CONFERENCE['conference_period']}</span><p>Session schedule coming soon</p></div></div></article>
{publication_panel}
</div></div></section>'''

venue = page_head("Venue & Travel", f"Host-city and travel information for {SITE_NAME} in {CONFERENCE['city']}, {CONFERENCE['country']}.", "Venue") + '<section class="content">' + inner(f'''<span class="section-label">{CONFERENCE['region']}</span><h2>Welcome to {CONFERENCE['city']}</h2><p>{CONFERENCE['city']} provides a regional setting for exchange across computing, engineering, environmental research and agricultural practice.</p><div class="coordinate-rule"><span>{CONFERENCE['latitude']}° N</span><span>{CONFERENCE['longitude']}° E</span></div><div class="venue-map"><iframe title="Map of the {SITE_NAME} host city in {CONFERENCE['city']}" src="https://www.google.com/maps?q={CONFERENCE['latitude']},{CONFERENCE['longitude']}&amp;z=13&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe><div class="venue-map-caption"><div><strong>{CONFERENCE['city']}, {CONFERENCE['country']}</strong><small>Host-city map · venue details coming soon</small></div><a class="text-link" href="https://www.google.com/maps/search/?api=1&amp;query={CONFERENCE['latitude']},{CONFERENCE['longitude']}" target="_blank" rel="noopener noreferrer">Open in Google Maps <span>↗</span></a></div></div><h3>Host institution</h3><p><strong>{ORGANIZER}</strong></p><p>The conference facility and arrival instructions will be published here when available.</p><h3>Travel and accommodation</h3><p>Accommodation, airport transfer, visa and local transport guidance will be published with the venue information.</p><a class="btn primary" href="{CONFERENCE['organizer_url']}" target="_blank" rel="noopener noreferrer">Official organiser website <span>↗</span></a>''') + '</section>'

contact = page_head("Contact", f"Official contact information for {SITE_NAME}.", "Contact") + '<section class="content">' + inner(f'''<span class="section-label">Enquiries</span><h2>Get in touch</h2><p>Conference enquiries are coordinated by the host institution.</p><dl class="contact-list"><div><dt>Host institution</dt><dd>{ORGANIZER}</dd></div><div><dt>Conference website</dt><dd><a href="{html.escape(SITE_URL, quote=True)}" target="_blank" rel="noopener noreferrer">{html.escape(SITE_URL.removeprefix('https://').rstrip('/'))} ↗</a></dd></div><div><dt>Organiser website</dt><dd><a href="{CONFERENCE['organizer_url']}" target="_blank" rel="noopener noreferrer">{CONFERENCE['organizer_url'].removeprefix('https://').rstrip('/')} ↗</a></dd></div><div><dt>{SERIES} secretariat</dt><dd><a href="mailto:{html.escape(CONTACT_EMAIL, quote=True)}">{html.escape(CONTACT_EMAIL)}</a></dd></div></dl>''') + '</section>'

PAGES = {
    "index.html": (f"The {CONFERENCE['edition_ordinal']} International Conference", home, f"{SITE_NAME} — {NAME}. Hosted by {ORGANIZER}."),
    "committee.html": ("Conference Committee", committee, f"Committee information for {SITE_NAME}."),
    "keynote-speakers.html": ("Keynote Speakers", keynotes, f"Keynote speaker announcements for {SITE_NAME}."),
    "call-for-papers.html": ("Call for Papers", cfp, f"Research scope and submission information for {NAME}."),
    "important-dates.html": ("Important Dates", important, f"Official milestone information for {SITE_NAME}."),
    "registration.html": ("For Attendees", registration, f"Submission, registration, programme and travel information for {SITE_NAME} attendees."),
    "venue.html": ("Venue & Travel", venue, f"Host-city and venue information for {SITE_NAME} in {CONFERENCE['city']}."),
    "contact.html": ("Contact", contact, f"Official host institution and contact information for {SITE_NAME}."),
}

for filename, (title, body, description) in PAGES.items():
    (ROOT / filename).write_text(wrap(filename, title, body, description), encoding="utf-8")

site_data = {
    "timeZone": CONFERENCE["timezone"],
    "announcements": [],
    "deadlines": CONFERENCE["deadlines"],
    "sponsors": CONFERENCE["sponsors"],
}
(ROOT / "assets" / "site-data.js").write_text(
    "/* Generated from conference_config.py. */\nwindow.ICASA_SITE = "
    + json.dumps(site_data, ensure_ascii=False, indent=2)
    + ";\n",
    encoding="utf-8",
)

print(f"Built {len(PAGES)} pages in {ROOT}")

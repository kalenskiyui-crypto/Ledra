#!/usr/bin/env python3
"""Build the deployable index.html from the design canvas source (Main.dc.html).

Usage: python3 scripts/build.py path/to/Main.dc.html

- rewrites /_blob/<id> asset references to ./assets/<id>.<ext>
- adds the React runtime scripts the canvas runtime needs
- replaces the <title> with the full SEO <head> block below
"""
import os, re, sys, json

SITE = "https://ledra-landing-page-html-3.vercel.app"   # production domain, no trailing slash

TITLE = "Ledra — AI agents that write your enterprise reports"
DESC = ("Ledra is the AI reporting agent that connects to your ERP, CRM and data warehouse "
        "and delivers board-ready, source-linked reports in minutes, not weeks. Start free.")

FAQ = [
    ("How does Ledra connect to our data?", "Through native integrations with ERPs, CRMs, data warehouses and spreadsheets. Setup takes about 10 minutes and needs read-only access."),
    ("Can we trust numbers in AI-written reports?", "Every figure links back to its source row, so reviewers can verify any number in one click before anything is published."),
    ("Is our data used to train AI models?", "No. Your data is never used for training and stays isolated in your own workspace."),
    ("What exactly is a Ledra Agent?", "An agent owns a recurring report. It pulls data on schedule, drafts the report, routes it for approval and delivers it where your team works."),
    ("Which formats can Ledra export?", "PDF, Word, PowerPoint, Google Docs and Notion pages, plus direct delivery to Slack or email."),
    ("Do you offer private deployment?", "Yes. The Enterprise plan includes private cloud or on-premise deployment and custom data residency."),
]
PLANS = [("Free", "0"), ("Starter", "49"), ("Pro", "199"), ("Scale", "499")]


def jsonld():
    org = {"@type": "Organization", "@id": SITE + "/#org", "name": "Ledra", "url": SITE + "/",
           "logo": {"@type": "ImageObject", "url": SITE + "/logo-512.png", "width": 512, "height": 512}}
    site = {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Ledra",
            "publisher": {"@id": SITE + "/#org"}, "inLanguage": "en"}
    page = {"@type": "WebPage", "@id": SITE + "/#webpage", "url": SITE + "/", "name": TITLE,
            "description": DESC, "isPartOf": {"@id": SITE + "/#website"}, "inLanguage": "en",
            "primaryImageOfPage": {"@type": "ImageObject", "url": SITE + "/og-image.png", "width": 1200, "height": 630}}
    app = {"@type": "SoftwareApplication", "@id": SITE + "/#app", "name": "Ledra",
           "applicationCategory": "BusinessApplication", "operatingSystem": "Web",
           "description": DESC, "url": SITE + "/", "image": SITE + "/og-image.png",
           "publisher": {"@id": SITE + "/#org"},
           "offers": [{"@type": "Offer", "name": n, "price": p, "priceCurrency": "USD",
                       "url": SITE + "/#pricing"} for n, p in PLANS]}
    faq = {"@type": "FAQPage", "@id": SITE + "/#faq", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    return json.dumps({"@context": "https://schema.org", "@graph": [org, site, page, app, faq]},
                      ensure_ascii=False, indent=1)


def head():
    e = lambda s: s.replace("&", "&amp;").replace('"', "&quot;")
    return f"""<title>{e(TITLE)}</title>
<meta name="description" content="{e(DESC)}">
<link rel="canonical" href="{SITE}/">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="theme-color" content="#0A0A0A">
<meta name="color-scheme" content="dark">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Ledra">
<meta property="og:locale" content="en_US">
<meta property="og:url" content="{SITE}/">
<meta property="og:title" content="{e(TITLE)}">
<meta property="og:description" content="{e(DESC)}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Ledra — Reports that write themselves. AI reporting dashboard.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(TITLE)}">
<meta name="twitter:description" content="{e(DESC)}">
<meta name="twitter:image" content="{SITE}/og-image.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&amp;display=swap">
<link rel="preload" href="./vendor/react-dom.js" as="script">
<script type="application/ld+json">
{jsonld()}
</script>"""


def main(src):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html = open(src, encoding="utf-8").read()
    assets = {f.split(".")[0]: f for f in os.listdir(os.path.join(root, "assets"))}
    html = re.sub(r"/_blob/([0-9a-f]{32})", lambda m: "./assets/" + assets[m.group(1)], html)
    if "./vendor/react.js" not in html:
        html = html.replace('<script src="./support.js"></script>',
                            '<script src="./vendor/react.js"></script>\n<script src="./vendor/react-dom.js"></script>\n'
                            '<script src="./support.js"></script>', 1)
    html, n = re.subn(r"<title>.*?</title>", lambda m: head(), html, count=1, flags=re.S)
    assert n == 1, "no <title> found"
    open(os.path.join(root, "index.html"), "w", encoding="utf-8").write(html)
    print("wrote index.html", len(html), "bytes")


if __name__ == "__main__":
    main(sys.argv[1])

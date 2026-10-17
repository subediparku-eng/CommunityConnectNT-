"""
Fetch current Northern Territory warnings from the Bureau of Meteorology
and write them to warnings.json for CommunityConnectNT.

Why FTP and not the website:
    BOM's robots.txt disallows automated fetching of their web pages.
    The anonymous FTP service is the route they provide for this, so
    this script uses it. Nothing here needs an API key or an account.

Run it:
    python scripts/fetch_warnings.py

Output:
    warnings.json in the repository root.
"""

import ftplib
import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from io import BytesIO

# ---------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------

FTP_HOST = "ftp.bom.gov.au"
FTP_DIR = "/anon/gen/fwo"

# NT warning products start with IDD. Narrow this list once you have
# confirmed the exact product IDs you want -- step 1 prints them all.
NT_PREFIX = "IDD"

OUTPUT_FILE = "warnings.json"
TIMEOUT_SECONDS = 30

# Map BOM phenomena text to the hazard icons the app draws.
HAZARD_RULES = [
    ("cyclone", ["cyclone", "tropical low"]),
    ("flood", ["flood"]),
    ("fire", ["fire", "bushfire"]),
    ("storm", ["storm", "thunderstorm", "wind", "gale", "squall"]),
    ("heat", ["heat", "heatwave"]),
    ("power", ["power", "outage"]),
]

# Map BOM warning wording to the three Australian Warning System levels.
LEVEL_RULES = [
    ("emergency", ["emergency warning", "take shelter", "red alert"]),
    ("watch", ["watch and act", "warning", "watch", "yellow alert"]),
    ("advice", ["advice", "outlook", "blue alert"]),
]


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def classify(text, rules, default):
    """Return the first rule whose keywords appear in text."""
    lowered = text.lower()
    for name, keywords in rules:
        for word in keywords:
            if word in lowered:
                return name
    return default


def clean(text):
    """Collapse whitespace and trim."""
    return re.sub(r"\s+", " ", text or "").strip()


def first_text(root, *tags):
    """Return the text of the first tag found anywhere in the tree."""
    for tag in tags:
        node = root.find(f".//{tag}")
        if node is not None and node.text:
            return clean(node.text)
    return ""


# ---------------------------------------------------------------------
# Step 1 - connect and list the NT warning files
# ---------------------------------------------------------------------

def list_nt_files(ftp):
    print(f"1. Listing {FTP_DIR} for files starting with {NT_PREFIX}")
    names = ftp.nlst(FTP_DIR)

    nt_files = []
    for path in names:
        name = path.rsplit("/", 1)[-1]
        if name.startswith(NT_PREFIX) and name.endswith(".xml"):
            nt_files.append(name)

    nt_files.sort()
    print(f"   found {len(nt_files)} NT files")
    for name in nt_files:
        print(f"   - {name}")
    return nt_files


# ---------------------------------------------------------------------
# Step 2 - download one file into memory
# ---------------------------------------------------------------------

def download(ftp, name):
    buffer = BytesIO()
    ftp.retrbinary(f"RETR {FTP_DIR}/{name}", buffer.write)
    return buffer.getvalue()


# ---------------------------------------------------------------------
# Step 3 - pull the parts we need out of the XML
# ---------------------------------------------------------------------

def parse_warning(raw_xml, product_id):
    """
    BOM warning files share an <amoc> header block. The body format
    varies by product, so this reads the header reliably and takes
    whatever descriptive text it can find for the summary.
    """
    try:
        root = ET.fromstring(raw_xml)
    except ET.ParseError as error:
        print(f"   ! {product_id}: could not parse XML ({error})")
        return None

    phenomena = first_text(root, "phenomena", "product-type")
    issued = first_text(root, "issue-time-utc", "issue-time-local", "start-time-utc")
    status = first_text(root, "status")

    # Skip cancelled or routine non-warning products.
    if status.lower() in {"cancelled", "cancellation"}:
        return None

    # Title: the headline if there is one, otherwise the phenomena.
    title = first_text(root, "headline", "title", "text")
    if not title:
        title = phenomena or product_id

    # Summary: the longest text block in the document reads best.
    blocks = [clean(node.text) for node in root.iter() if node.text and len(clean(node.text)) > 40]
    summary = max(blocks, key=len) if blocks else ""
    if len(summary) > 320:
        summary = summary[:317].rsplit(" ", 1)[0] + "..."

    combined = f"{title} {phenomena} {summary}"

    return {
        "id": product_id,
        "level": classify(combined, LEVEL_RULES, "advice"),
        "hazard": classify(combined, HAZARD_RULES, "other"),
        "title": title[:140],
        "text": summary,
        "issued": issued,
        "source": "Bureau of Meteorology",
    }


# ---------------------------------------------------------------------
# Step 4 - put it together
# ---------------------------------------------------------------------

def main():
    print(f"Connecting to {FTP_HOST}")
    try:
        ftp = ftplib.FTP(FTP_HOST, timeout=TIMEOUT_SECONDS)
        ftp.login()  # anonymous
    except Exception as error:
        print(f"FTP connection failed: {error}")
        return 1

    warnings = []
    try:
        files = list_nt_files(ftp)

        print("2. Downloading and parsing")
        for name in files:
            product_id = name.replace(".xml", "")
            try:
                raw = download(ftp, name)
            except Exception as error:
                print(f"   ! {product_id}: download failed ({error})")
                continue

            warning = parse_warning(raw, product_id)
            if warning:
                warnings.append(warning)
                print(f"   + {product_id}: {warning['level']} / {warning['hazard']}")
    finally:
        try:
            ftp.quit()
        except Exception:
            ftp.close()

    # Most urgent first.
    order = {"emergency": 0, "watch": 1, "advice": 2}
    warnings.sort(key=lambda w: order.get(w["level"], 3))

    payload = {
        "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "Bureau of Meteorology anonymous FTP",
        "count": len(warnings),
        "warnings": warnings,
    }

    print(f"3. Writing {OUTPUT_FILE} with {len(warnings)} warnings")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)

    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

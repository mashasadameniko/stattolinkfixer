#!/usr/bin/env python3
import csv
import pywikibot
from pywikibot import pagegenerators

def main():
    site = pywikibot.Site("en", "wikipedia")
    site.login()

    # Load mappings
    mapping = {}
    with open("url_mapping.csv", newline="") as fh:
        for old, new in csv.reader(fh):
            mapping[old.strip()] = new.strip()

    # Iterate each archived URL
    for old_url, new_url in mapping.items():
        refs = pagegenerators.ReferringPageGenerator(old_url, site)
        for page in refs:
            text = page.text
            if old_url in text:
                new_text = text.replace(old_url, new_url)
                summary = (f"Replace archived link with live URL: "
                           f"{old_url} → {new_url}")
                page.text = new_text
                try:
                    page.save(summary=summary)
                    print(f"✔ Updated: {page.title()}")
                except Exception as e:
                    print(f"✖ Failed {page.title()}: {e}")

if __name__ == "__main__":
    main()

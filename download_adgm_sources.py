#!/usr/bin/env python3
"""
download_adgm_sources.py
Downloads ADGM official documents listed in data/data_sources_links.txt into data/adgm_sources/
Run locally where internet is available.
"""
import os, requests, time
from pathlib import Path

OUT = Path("data/adgm_sources")
OUT.mkdir(parents=True, exist_ok=True)

with open("data/data_sources_links.txt", "r", encoding="utf-8") as f:
    links = [line.strip() for line in f.readlines() if line.strip()]

for i, url in enumerate(links, start=1):
    try:
        print(f"Downloading {i}/{len(links)}: {url}")
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            filename = url.split("/")[-1].split('?')[0] or f"doc_{i}"
            out_path = OUT / filename
            with open(out_path, "wb") as wf:
                wf.write(r.content)
            print("Saved to:", out_path)
        else:
            print("Failed:", r.status_code, url)
    except Exception as e:
        print("Error downloading", url, e)
    time.sleep(1)
print("Done.")


"""Print ingest facts for shortlisted clips. Keys are <night>:<Cnnn> with night = 15,16,17,18,19,20
(Oct 15/16 share Media/ and Oct 19/20 reuse clip numbers, so the overview label alone is ambiguous).
Usage: .venv/bin/python tools/cand_table.py <reel>/analysis/ingest.json 17:C145 20:C061 ..."""
import json, os, sys

FOLDER = {"15": "Media", "16": "Media", "17": "Pujo 2026 Oct 17", "18": "Puja 2026 Oct 18", "19": "Pujo 2026 Oct 19", "20": "Pujo 2026 Oct 20"}


def key_of(row):
    stem = os.path.splitext(row["clip"])[0]
    c = stem[-4:]
    n = int(c[1:])
    path = os.path.realpath(row["path"])
    if "/Media/" in path:
        return ("15" if n <= 77 else "16") + ":" + c
    for k, v in FOLDER.items():
        if k in ("15", "16"):
            continue
        if f"/{v}" in path:
            return k + ":" + c
    return "?:" + c


rows = {}
for r in json.load(open(sys.argv[1])):
    k = key_of(r)
    rows.setdefault(k, r)  # Oct 19 clips also sit in the Oct 20 folder; keep the first
print("| key | file | dur | fps | shutter | WB | flicker (measured) | luma | flags |")
print("|---|---|---|---|---|---|---|---|---|")
for k in sys.argv[2:]:
    r = rows.get(k)
    if not r:
        print(f"| {k} | not found |")
        continue
    fl = ", ".join(f for f in r["flags"] if f != "8-bit")
    print(f"| {k} | {r['clip']} | {r['dur']:.1f} | {r['fps']} | {r['shutter']} | {r['wb_k']} | {r['flicker']} ({r['measured']}) | {r['luma']:.2f} | {fl} |")

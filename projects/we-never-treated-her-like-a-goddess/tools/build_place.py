"""EDL json -> frame-quantised placement for add_to_timeline_batch (V1 + linked A1) and a frame table.
Cut times are floored to the sequence frame (cuts land 0 to -1 frame before the clause onset).
Source in-points are converted to the clip's interpreted (25 fps) time: frames = src_s * native_fps.
Usage: python3 tools/build_place.py analysis/edl_v1.json analysis/premiere_ids.json analysis/place_v1.json"""
import json, math, sys

edl = json.load(open(sys.argv[1])); ids = json.load(open(sys.argv[2])); SEQ = edl["seq_fps"]
NATIVE = ids["native_fps"]
rows = [r for r in edl["rows"] if r["clip"]]
cuts = [math.floor(r["t0"] * SEQ + 1e-6) for r in rows] + [math.floor(rows[-1]["t1"] * SEQ + 1e-6)]
place, table = [], []
for i, r in enumerate(rows):
    f0, f1 = cuts[i], cuts[i + 1]
    sf0 = round(r["src"] * NATIVE[r["clip"]])  # source frame, played one per sequence frame after interpretation
    place.append({"projectItemId": ids["items"][r["clip"]], "trackIndex": 0, "time": f0 / SEQ,
                  "sourceInPoint": sf0 / SEQ, "sourceOutPoint": (sf0 + f1 - f0) / SEQ, "linkAudio": True})
    table.append({"n": r["n"], "clip": r["clip"], "f0": f0, "f1": f1, "src_f0": sf0})
json.dump(place, open(sys.argv[3], "w"), indent=1)
json.dump(table, open(sys.argv[3].replace(".json", "_frames.json"), "w"), indent=1)
for t in table:
    print(t["n"], t["clip"][-4:], t["f0"], t["f1"], t["f1"] - t["f0"], "src_f", t["src_f0"])
print("picture ends at frame", cuts[-1], "=", cuts[-1] / SEQ, "s")

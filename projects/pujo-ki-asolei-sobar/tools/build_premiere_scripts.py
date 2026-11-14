#!/usr/bin/env python3
"""Generate the Premiere ExtendScript files for the rough cut from the EDL + depth bakes.

Writes into analysis/:
  _es_import.jsx   bins + import (originals for tonal shots, depth bakes, VO guide, title, subtitle cards, end card, grain)
  _es_seq.jsx      1080x1920 30 fps sequence from title-alpha.mov (1080x1920 @30), tracks V1-V6 / A1-A3, emptied
  place_v1.json    rows for add_to_timeline_batch (filled with projectItem ids by _es_items.jsx output)
  _es_items.jsx    dumps name -> nodeId for every imported item (Rule 2 file output)
Every script targets this reel's project by path, never "whatever is active".
"""
import json
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
ROOT = REEL.parents[1]
PROJ = REEL / "premiere" / "pujo-ki-asolei-sobar.prproj"
OUT = REEL / "analysis" / "_es_out.txt"
edl = json.loads((REEL / "analysis" / "edl_v1c.json").read_text())
bakes = {b["n"]: b for b in json.loads((REEL / "renders" / "depth" / "bakes.json").read_text())}

HEAD = f'''var OUTF="{OUT}"; var PROJP="{PROJ}";
function proj(){{ for(var i=0;i<app.projects.numProjects;i++){{ if(app.projects[i].path==PROJP) return app.projects[i]; }} return null; }}
function save(o){{ var f=new File(OUTF); f.encoding="UTF-8"; f.open("w"); f.write(JSON.stringify(o)); f.close(); }}
'''

rows, originals, depth_files = [], [], []
for s in edl["shots"]:
    if s["n"] in bakes:
        b = bakes[s["n"]]; path = str(REEL / b["bake"]); depth_files.append(path)
        src_in, src_out = b["place_in"], b["place_out"]
    else:
        path = str(next((REEL / "raw" / "b-roll").glob(f"*_{s['clip']}.mov"))); originals.append(path)
        src_in, src_out = s["in"], s["out"]
        if s["clip"] == "C145":                      # interpreted 25 -> 30 fps: source times scale by 25/30
            src_in, src_out = round(src_in * 25 / 30, 3), round(src_out * 25 / 30, 3)
    rows.append({"n": s["n"], "file": Path(path).name, "start": s["start"], "end": s["end"], "src_in": src_in, "src_out": src_out})
originals = sorted(set(originals))
subs = sorted(str(p) for p in (REEL / "renders" / "overlays" / "subs").glob("sub_*.png"))
gfx = [str(REEL / "graphics" / "title" / "renders" / "title-alpha.mov"), str(REEL / "renders" / "overlays" / "endcard_handle.png")] + subs
audio = [str(REEL / "audio" / "ref_audio_vo.wav")]
tex = [str(ROOT / "assets" / "overlays" / "gemini_film_grain_16mm.mp4")]

js = lambda xs: json.dumps(xs)
(REEL / "analysis" / "_es_import.jsx").write_text(HEAD + f'''var out={{}}; try {{
var P=proj(); if(!P) throw "project not open: "+PROJP;
var root=P.rootItem; var names=["02_B-Roll","03_Graphics","04_Textures","06_Music","07_Depth"]; var bins={{}};
for(var i=0;i<names.length;i++){{ var f=null; for(var j=0;j<root.children.numItems;j++){{ if(root.children[j].name==names[i]&&root.children[j].type==2) f=root.children[j]; }} bins[names[i]]=f?f:root.createBin(names[i]); }}
out.ok=[P.importFiles({js(originals)},true,bins["02_B-Roll"],false), P.importFiles({js(depth_files)},true,bins["07_Depth"],false),
        P.importFiles({js(gfx)},true,bins["03_Graphics"],false), P.importFiles({js(audio)},true,bins["06_Music"],false),
        P.importFiles({js(tex)},true,bins["04_Textures"],false)];
out.counts={{}}; for(var k in bins) out.counts[k]=bins[k].children.numItems; out.project=P.name;
}} catch(e) {{ out.err=e.toString()+" line "+e.line; }} save(out);
''')
(REEL / "analysis" / "_es_items.jsx").write_text(HEAD + '''var out={items:[]}; try {
var P=proj(); if(!P) throw "project not open";
function walk(it,bin){ for(var i=0;i<it.children.numItems;i++){ var c=it.children[i]; if(c.type==2) walk(c,c.name); else out.items.push({name:c.name,id:c.nodeId,bin:bin}); } }
walk(P.rootItem,"root");
} catch(e) { out.err=e.toString(); } save(out);
''')
(REEL / "analysis" / "_es_seq.jsx").write_text(HEAD + '''var out={}; try {
var P=proj(); if(!P) throw "project not open";
var src=null; function find(it){ for(var i=0;i<it.children.numItems;i++){ var c=it.children[i]; if(c.type==2){ var r=find(c); if(r) return r; } else if(c.name=="title-alpha.mov") return c; } return null; }
src=find(P.rootItem);
var seq=P.createNewSequenceFromClips("Reel_pujo-ki-asolei-sobar_v1",[src],P.rootItem);
var s=seq.getSettings(); out.settings={w:s.videoFrameWidth,h:s.videoFrameHeight,fps:Math.round(100/s.videoFrameRate.seconds)/100};
for(var t=0;t<seq.videoTracks.numTracks;t++){ var tr=seq.videoTracks[t]; for(var k=tr.clips.numItems-1;k>=0;k--) tr.clips[k].remove(false,false); }
for(var t=0;t<seq.audioTracks.numTracks;t++){ var tr=seq.audioTracks[t]; for(var k=tr.clips.numItems-1;k>=0;k--) tr.clips[k].remove(false,false); }
out.id=seq.sequenceID; out.v=seq.videoTracks.numTracks; out.a=seq.audioTracks.numTracks;
P.activeSequence=seq;
} catch(e) { out.err=e.toString()+" line "+e.line; } save(out);
''')
(REEL / "analysis" / "place_v1.json").write_text(json.dumps(rows, indent=1))
print(f"originals {len(originals)}, depth {len(depth_files)}, gfx {len(gfx)}, rows {len(rows)}")
for r in rows: print(f"  {r['n']:>3} {r['file']:<34} {r['start']:6.2f}-{r['end']:6.2f}  src {r['src_in']:.3f}-{r['src_out']:.3f}")

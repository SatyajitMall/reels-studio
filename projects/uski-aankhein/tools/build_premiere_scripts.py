#!/usr/bin/env python3
"""Write the Premiere ExtendScript files for the uski-aankhein rough cut (v1, round 1b bake: renders/bakes_v2/V1_timeline_v2.mov).

Every script targets THIS reel's project by path (Premiere is shared with other reel sessions) and writes its result
to analysis/_es_out.txt (reality doc Rule 2). Patterns from pujo-ki-asolei-sobar's builder and the puja-night-2
ExtendScript CR (overwriteClip with Time objects; set end to close frame-snap gaps; read everything back).
  _es_import.jsx    bins + import: V1 bakes, V2 stock band, V4 grain, V5 title/end card, A3 music, A2 SFX
  _es_seq.jsx       Reel_uski-aankhein_v1 (1080x1920, 25 fps) from title-alpha.mov, emptied; then add tracks to V5 / A3
  _es_place.jsx     place everything at frame-exact times, blend modes, opacities, audio levels
  _es_readback.jsx  every track's clips (name, start/end frames, opacity, blend, scale, level) -> _es_out.txt
"""
import json
from pathlib import Path
REEL = Path(__file__).resolve().parents[1]; ROOT = REEL.parents[1]
PROJ = REEL / "premiere" / "uski-aankhein.prproj"; OUT = REEL / "analysis" / "_es_out.txt"
FILES = {
 "01_A-Roll": [str(REEL / "renders/bakes_v2/V1_timeline_v2.mov")],      # round 1b: one stabilised, primary-corrected V1 with dissolves baked
 "02_B-Roll": [str(REEL / "renders/stock/stock_band_v1.mov")],
 "03_Graphics": [str(REEL / "graphics/title/renders/title-alpha.mov"), str(REEL / "graphics/endcard/renders/endcard-alpha.mov")],
 "04_Textures": [str(REEL / "renders/texture/grain_25fps_v1.mov")],
 "05_SFX": [str(REEL / "audio/sfx/gemini_bass_drop_boom.wav")],
 "06_Music": [str(REEL / "references/ref_audio.wav")],
}
def lvl(db): return round(10 ** ((db - 15) / 20), 6)          # Premiere clip Level, linear (reality doc)
PLACE = {
 "v": [[0, "V1_timeline_v2.mov", 0, 550, None],                              # V1 0-22.00 s (frame 549 black)
       [1, "stock_band_v1.mov", 0, 104, {"opacity": 65, "blend": 22}],        # V2 Screen 65 %
         [3, "grain_25fps_v1.mov", 0, 549, {"opacity": 12, "blend": 19}],       # V4 Overlay 12 %
         [4, "title-alpha.mov", 15, 95, None],                                   # V5 title 0.60-3.80 s
         [4, "endcard-alpha.mov", 515, 549, None]],                              # V5 end card 20.60-21.96 s
 "a": [[2, "ref_audio.wav", 0, 550, lvl(0)],                                     # A3 music, 0 dB
       [1, "gemini_bass_drop_boom.wav", 197, 227, lvl(-14)],                     # A2 boom on the rhythm entry 7.88 s
       [1, "gemini_bass_drop_boom.wav", 490, 520, lvl(-14)]],                    # A2 boom on the freeze 19.60 s
}
HEAD = f'''var OUTF="{OUT}"; var PROJP="{PROJ}"; var SEQNAME="Reel_uski-aankhein_v1"; var FPS=25;
function proj(){{ for(var i=0;i<app.projects.numProjects;i++){{ if(app.projects[i].path==PROJP) return app.projects[i]; }} return null; }}
function save(o){{ var f=new File(OUTF); f.encoding="UTF-8"; f.open("w"); f.write(JSON.stringify(o)); f.close(); }}
function T(fr){{ var t=new Time(); t.seconds=fr/FPS; return t; }}
function seqByName(P){{ for(var i=0;i<P.sequences.numSequences;i++){{ if(P.sequences[i].name==SEQNAME) return P.sequences[i]; }} return null; }}
function findItem(it,name){{ for(var i=0;i<it.children.numItems;i++){{ var c=it.children[i]; if(c.type==2){{ var r=findItem(c,name); if(r) return r; }} else if(c.name==name) return c; }} return null; }}
function comp(c,n){{ for(var j=0;j<c.components.numItems;j++){{ if(c.components[j].displayName==n) return c.components[j]; }} return null; }}
'''
js = lambda x: json.dumps(x)
(REEL / "analysis/_es_import.jsx").write_text(HEAD + f'''var out={{}}; try {{
var P=proj(); if(!P) throw "project not open: "+PROJP;
var F={js(FILES)}; var root=P.rootItem; out.counts={{}};
for(var b in F){{ var bin=null; for(var j=0;j<root.children.numItems;j++){{ if(root.children[j].name==b&&root.children[j].type==2) bin=root.children[j]; }}
  if(!bin) bin=root.createBin(b); P.importFiles(F[b],true,bin,false); out.counts[b]=bin.children.numItems; }}
out.project=P.name;
}} catch(e) {{ out.err=e.toString()+" line "+e.line; }} save(out);
''')
(REEL / "analysis/_es_seq.jsx").write_text(HEAD + '''var out={}; try {
var P=proj(); if(!P) throw "project not open"; if(seqByName(P)) throw "sequence exists already";
var src=findItem(P.rootItem,"title-alpha.mov"); var seq=P.createNewSequenceFromClips(SEQNAME,[src],P.rootItem);
for(var t=0;t<seq.videoTracks.numTracks;t++){ var tr=seq.videoTracks[t]; for(var k=tr.clips.numItems-1;k>=0;k--) tr.clips[k].remove(false,false); }
for(var t=0;t<seq.audioTracks.numTracks;t++){ var tr=seq.audioTracks[t]; for(var k=tr.clips.numItems-1;k>=0;k--) tr.clips[k].remove(false,false); }
var s=seq.getSettings(); out.settings={w:s.videoFrameWidth,h:s.videoFrameHeight,fps:Math.round(100/s.videoFrameRate.seconds)/100};
out.id=seq.sequenceID; out.v=seq.videoTracks.numTracks; out.a=seq.audioTracks.numTracks; P.activeSequence=seq;
} catch(e) { out.err=e.toString()+" line "+e.line; } save(out);
''')
(REEL / "analysis/_es_place.jsx").write_text(HEAD + f'''var out={{v:[],a:[]}}; try {{
var P=proj(); if(!P) throw "project not open"; var seq=seqByName(P); if(!seq) throw "no sequence";
if(seq.videoTracks.numTracks<5||seq.audioTracks.numTracks<3) throw "need V5/A3, have V"+seq.videoTracks.numTracks+" A"+seq.audioTracks.numTracks;
var V={js(PLACE["v"])}, A={js(PLACE["a"])};
for(var i=0;i<V.length;i++){{ var r=V[i]; var it=findItem(P.rootItem,r[1]); if(!it) throw "missing "+r[1];
  var tr=seq.videoTracks[r[0]]; tr.overwriteClip(it,T(r[2]));
  var c=null; for(var k=0;k<tr.clips.numItems;k++){{ if(Math.round(tr.clips[k].start.seconds*FPS)==r[2]) c=tr.clips[k]; }}
  if(!c) throw "not placed "+r[1]; c.end=T(r[3]);
  var m=comp(c,"Motion"); for(var p=0;p<m.properties.numItems;p++){{ if(m.properties[p].displayName=="Scale") m.properties[p].setValue(100,true); }}
  if(r[4]){{ var op=comp(c,"Opacity"); op.properties[0].setValue(r[4].opacity,true); op.properties[1].setValue(r[4].blend,true); }}
  out.v.push([r[0],r[1],Math.round(c.start.seconds*FPS),Math.round(c.end.seconds*FPS)]); }}
for(var i=0;i<A.length;i++){{ var r=A[i]; var it=findItem(P.rootItem,r[1]); if(!it) throw "missing "+r[1];
  var tr=seq.audioTracks[r[0]]; tr.overwriteClip(it,T(r[2]));
  var c=null; for(var k=0;k<tr.clips.numItems;k++){{ if(Math.round(tr.clips[k].start.seconds*FPS)==r[2]) c=tr.clips[k]; }}
  if(!c) throw "not placed "+r[1]; if(Math.round(c.end.seconds*FPS)>r[3]) c.end=T(r[3]);
  var vol=comp(c,"Volume"); for(var p=0;p<vol.properties.numItems;p++){{ if(vol.properties[p].displayName=="Level") vol.properties[p].setValue(r[4],true); }}
  out.a.push([r[0],r[1],Math.round(c.start.seconds*FPS),Math.round(c.end.seconds*FPS)]); }}
seq.setInPoint(0); var e=new Time(); e.seconds=22.0; seq.setOutPoint(e.seconds);
}} catch(e) {{ out.err=e.toString()+" line "+e.line; }} save(out);
''')
(REEL / "analysis/_es_readback.jsx").write_text(HEAD + '''var out={v:[],a:[]}; try {
var P=proj(); if(!P) throw "project not open"; var seq=seqByName(P); if(!seq) throw "no sequence";
for(var t=0;t<seq.videoTracks.numTracks;t++){ var tr=seq.videoTracks[t]; for(var k=0;k<tr.clips.numItems;k++){ var c=tr.clips[k]; var r={t:t,name:c.name,s:Math.round(c.start.seconds*FPS),e:Math.round(c.end.seconds*FPS),fx:[]};
  for(var j=0;j<c.components.numItems;j++) r.fx.push(c.components[j].displayName);
  var op=comp(c,"Opacity"); if(op){ r.opacity=op.properties[0].getValue(); r.blend=op.properties[1].getValue(); }
  var m=comp(c,"Motion"); for(var p=0;p<m.properties.numItems;p++){ if(m.properties[p].displayName=="Scale") r.scale=m.properties[p].getValue(); }
  out.v.push(r); } }
for(var t=0;t<seq.audioTracks.numTracks;t++){ var tr=seq.audioTracks[t]; for(var k=0;k<tr.clips.numItems;k++){ var c=tr.clips[k]; var r={t:t,name:c.name,s:Math.round(c.start.seconds*FPS),e:Math.round(c.end.seconds*FPS)};
  var vol=comp(c,"Volume"); if(vol){ for(var p=0;p<vol.properties.numItems;p++){ if(vol.properties[p].displayName=="Level") r.level=vol.properties[p].getValue(); } }
  out.a.push(r); } }
out.inout=[seq.getInPoint(),seq.getOutPoint()]; out.id=seq.sequenceID;
} catch(e) { out.err=e.toString()+" line "+e.line; } save(out);
''')
print(json.dumps(PLACE, indent=0)[:1500])

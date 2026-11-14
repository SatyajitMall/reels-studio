#!/usr/bin/env python3
"""Write analysis/_es_<ver>_primary.jsx from analysis/grade_<ver>.json (per-clip primary, keyed by start frame).
Same Lumetri slot map as Phase 4 (_es_a1_primary.jsx); one Lumetri per clip, added by QE only if absent. C056 (651) keeps its v1 grade."""
import json, sys
from pathlib import Path
VER = sys.argv[1] if len(sys.argv) > 1 else 'v2'
SEQ = {'v2': '22d5e281-0a84-455e-adad-42840088fcc0', 'v3': '1d9d708a-c28d-4405-9f16-7ee26e70c830', 'v4': '3664acf0-2c15-4c1d-b20a-997a9553c52a'}[VER]
G = json.load(open(f'analysis/grade_{VER}.json'))
src = Path('analysis/_es_a1_primary.jsx').read_text()
src = src.replace('var SEQID="b8b22066-79e8-418f-805d-44da3c02dc95"', f'var SEQID="{SEQ}"')
start, end = src.index('var A1={'), src.index('var IDX=')
src = src[:start] + 'var A1=' + json.dumps({str(k): v for k, v in G.items()}) + ';\n' + src[end:]
src = src.replace('if(!A1[sf]) throw "no A1 row for start frame "+sf;', 'if(!A1[sf]){ if(sf==651) continue; throw "no A1 row for start frame "+sf; }')
Path(f'analysis/_es_{VER}_primary.jsx').write_text(src)
print('rows', len(G))

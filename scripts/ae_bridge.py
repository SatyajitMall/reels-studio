#!/usr/bin/env python3
"""Run ExtendScript in After Effects 2026 and get the result back as JSON.

How it works (verified on AE 26.5x89, 2026-10-17):
- AppleScript `DoScript <text>` runs a one-line loader in the running AE. The loader reads the
  generated .jsx from /tmp and evals it (passing a long multi-line script inline returned "1" and
  didn't run). Its reply is "0" (or
  "1" when AE refuses, e.g. a modal dialog is open), whatever ae.sdef says, so the script's return
  value is written to a JSON file and read here.
- Don't use `DoScriptFile`: on AE 26.5 it didn't run the file, returned "1", and left a modal
  dialog that blocked every later script until the director closed it.
- AE's ExtendScript has no JSON object, so a small stringify is prepended.
- Dialogs are suppressed while the script runs. The first call from a new app triggers macOS's
  Automation prompt ("… wants to control Adobe After Effects 2026"); the director must allow it.

As a module:   from ae_bridge import run_jsx;  run_jsx("return app.version;")
From the shell:
  ./.venv/bin/python scripts/ae_bridge.py verify            # AE reachable, version, project state
  ./.venv/bin/python scripts/ae_bridge.py effects NAME…     # can these effect match names be added?
  ./.venv/bin/python scripts/ae_bridge.py run file.jsx       # body of a function; `return` a value
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

APP = "Adobe After Effects 2026"

PRELUDE = r"""
function __q(s){return '"'+String(s).replace(/\\/g,'\\\\').replace(/"/g,'\\"').replace(/\n/g,'\\n').replace(/\r/g,'\\r').replace(/\t/g,'\\t')+'"';}
function __json(v){
  if (v===null||v===undefined) return 'null';
  var t=typeof v;
  if (t==='number') return isFinite(v)?String(v):'null';
  if (t==='boolean') return String(v);
  if (t==='string') return __q(v);
  if (v instanceof Array){var a=[];for(var i=0;i<v.length;i++)a.push(__json(v[i]));return '['+a.join(',')+']';}
  if (t==='object'){var o=[];for(var k in v){if(v.hasOwnProperty(k))o.push(__q(k)+':'+__json(v[k]));}return '{'+o.join(',')+'}';}
  return __q(String(v));
}
"""


def run_jsx(body: str, timeout_s: int = 600) -> dict:
    """Run `body` (the inside of a function; use `return`) in AE. Returns {"ok", "result"|"error", "line"}."""
    with tempfile.TemporaryDirectory(prefix="ae_bridge_", dir="/tmp") as tmp:
        out = Path(tmp) / "out.json"
        code = PRELUDE + f"""
app.beginSuppressDialogs();
var __out = new File({json.dumps(str(out))}); __out.encoding = "UTF-8";
var __res;
try {{ var __f = eval({json.dumps("(function(){" + body + chr(10) + "})")});  // eval so syntax errors are caught too
      __res = '{{"ok":true,"result":' + __json(__f()) + '}}'; }}
catch (e) {{ __res = '{{"ok":false,"error":' + __q(e.toString()) + ',"line":' + (e.line || 0) + '}}'; }}
app.endSuppressDialogs(false);
__out.open("w"); __out.write(__res); __out.close();
"""
        jsx = Path(tmp) / "run.jsx"
        jsx.write_text(code, encoding="utf-8")
        loader = (f"var __l = new File({json.dumps(str(jsx))}); __l.encoding = 'UTF-8'; __l.open('r'); "
                  f"var __src = __l.read(); __l.close(); eval(__src);")
        script = ["on run argv", f"with timeout of {timeout_s} seconds",
                  f'tell application "{APP}" to DoScript (item 1 of argv)', "end timeout", "end run"]
        args = [a for line in script for a in ("-e", line)]
        p = subprocess.run(["osascript", *args, loader], capture_output=True, text=True, timeout=timeout_s + 30)
        for _ in range(50):  # AE may still be writing when DoScript returns: wait for a complete result
            try:
                return json.loads(out.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                time.sleep(0.1)
        return {"ok": False, "error": f"no result; osascript said: {(p.stderr or p.stdout).strip()!r} "
                                      "(Automation permission denied, AE busy, or a modal dialog open?)"}


def verify() -> dict:
    return run_jsx("""
        var p = app.project;
        return {version: app.version, items: p.numItems, dirty: p.dirty,
                file: p.file ? p.file.fsName : null,
                renderQueueItems: p.renderQueue.numItems};
    """, timeout_s=30)


def check_effects(match_names: list[str]) -> dict:
    """Which match names can be added to a layer. Uses a throwaway comp that's removed afterwards.

    Don't enumerate app.effects: on AE 26.5 it ran for 5+ minutes and blocked every other script.
    """
    return run_jsx(f"""
        var names = {json.dumps(match_names)}, out = {{}};
        var comp = app.project.items.addComp("__ae_bridge_probe", 100, 100, 1, 1, 25);
        var layer = comp.layers.addSolid([0, 0, 0], "probe", 100, 100, 1);
        try {{
            for (var i = 0; i < names.length; i++) out[names[i]] = layer.Effects.canAddProperty(names[i]);
        }} finally {{
            var solid = layer.source, folder = solid ? solid.parentFolder : null;
            comp.remove(); if (solid) solid.remove();
            if (folder && folder !== app.project.rootFolder && folder.numItems === 0) folder.remove();  // AE's auto 'Solids' folder
        }}
        return out;
    """, timeout_s=60)


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] not in ("verify", "effects", "run"):
        sys.exit(__doc__)
    cmd = sys.argv[1]
    if cmd == "verify":
        r = verify()
    elif cmd == "effects":
        r = check_effects(sys.argv[2:])
    else:
        r = run_jsx(Path(sys.argv[2]).read_text())
    print(json.dumps(r, indent=1))
    sys.exit(0 if r.get("ok") else 1)


if __name__ == "__main__":
    main()

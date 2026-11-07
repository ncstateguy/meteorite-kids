#!/usr/bin/env python3
"""Build the dev copy of the game from the main file.

The main file (src/meteorite-kids-battle.html) is the only one you edit.
This script makes src/meteorite-kids-dev.html from it: story gates off,
everything unlocked, and the Dev tools panel added (tools/dev-tools.js).

Usage: python3 tools/build-dev.py [MAIN] [OUT]
Each replacement must match exactly once, or the build stops. That way a
change to the main file can never silently break the dev build.
"""
import pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE.parent / 'src'
MAIN = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else SRC / 'meteorite-kids-battle.html'
OUT = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else SRC / 'meteorite-kids-dev.html'

src = MAIN.read_text(encoding='utf-8')

def rep(a, b):
    global src
    n = src.count(a)
    if n != 1:
        sys.exit(f'build-dev: expected 1 match, found {n}:\n  {a[:90]}')
    src = src.replace(a, b)

# Title
rep('<title>Meteorite Kids Battle</title>', '<title>Dev · Meteorite Kids Battle</title>')
# Styles for the dev panel
rep('.modal-box h2{margin:0 0 6px}', '.modal-box h2{margin:0 0 6px}.modal-box h3{margin:14px 0 6px;font-size:14px;color:var(--accent)}.modal-box .row{flex-wrap:wrap;gap:6px}')
# Dev tools button, after the Exit button
rep('<button class="mini" id="exitBtn" hidden>Exit</button>\n', '<button class="mini" id="exitBtn" hidden>Exit</button>\n      <button class="mini" id="devBtn" style="border-color:var(--accent);color:var(--accent)">Dev tools</button>\n')
# Dev tools dialog, after the caption box
rep('<div class="cap" id="cap" hidden></div>\n', '<div class="cap" id="cap" hidden></div>\n    <div class="modal" id="devDlg" hidden><div class="modal-box" style="width:min(94%,920px);max-height:86vh;overflow:auto"><div class="row" style="justify-content:space-between;align-items:center"><h2 style="margin:0">Dev tools</h2><button id="devX">Close</button></div><p class="tip">Dev build. Press the backtick key (`) or the Dev tools button any time.</p><div id="devBody"></div></div></div>\n')
# Controller focus can move inside the dev dialog
rep("const root=!$('manualDlg').hidden?$('manualDlg'):", "const root=!$('manualDlg').hidden?$('manualDlg'):!$('devDlg').hidden?$('devDlg'):")
# Story gates off
rep('const STORY=true;', 'const STORY=false;')
rep("if(progress.ch12){b3.innerHTML=`Interlude", "if(true){b3.innerHTML=`Interlude")
# Dev panel code, after the exit-menu setup
rep("setInterval(()=>{$('exitBtn').hidden=TITLE.active},250);\n",
    "setInterval(()=>{$('exitBtn').hidden=TITLE.active},250);\n" + (HERE / 'dev-tools.js').read_text(encoding='utf-8'))

OUT.write_text(src, encoding='utf-8')
print(f'build-dev: wrote {OUT} ({len(src.encode())} bytes)')

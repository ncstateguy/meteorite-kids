#!/bin/bash
# Build the dev copy, then the GitHub Pages index.html (a full document head around the game file).
set -e
cd "$(dirname "$0")/.."
python3 tools/build-dev.py
{ printf '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<meta name="theme-color" content="#0d0b1a">\n</head>\n<body>\n'; cat src/meteorite-kids-battle.html; printf '\n</body>\n</html>\n'; } > index.html
echo built index.html $(wc -c < index.html)

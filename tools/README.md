# Tools and tests

**Edit only `src/meteorite-kids-battle.html`.** Everything else is built from it.

## Build and deploy

- `tools/deploy.sh` builds the dev copy, then `index.html` (what GitHub Pages serves).
- `tools/build-dev.py` builds `src/meteorite-kids-dev.html`: story gates off, everything unlocked, Dev tools panel added from `tools/dev-tools.js`. Every replacement must match exactly once, so if a main-file change breaks one, the build stops and says which. The dev copy is not committed.
- `tools/patch.py` is a safe find-and-replace helper for editing the game file. Each replacement must match the expected number of times, or nothing is written.

## Tests

All tests use Playwright and read `src/meteorite-kids-battle.html` unless `GAME=/path/to/file.html` is set. Screenshots and audio go to `tests/out/` (not committed).

| Test | What it checks |
|---|---|
| `node tests/errors.js [file]` | No script errors on load (exits 1 if any) |
| `node tests/smoke.js` | Every area enters, every battle starts, every scene plays |
| `node tests/part3-flow.js` | Part 3 story flow from the reunion to the end, including the Relic Road |
| `node tests/scenes.js` | Plays a list of scenes (edit the list in the file) |
| `node tests/playlog.js` | The playtest log records and opens |
| `node tests/teamhit.js` | Team-wide hit cap and the Crown Barrage shield rule |
| `node tests/defeat.js [keys]` | Defeat screen shows the short retry tip |
| `node tests/benchswap.js` | Ch 23 Swap button glows, names who is waiting, caption shows |
| `node tests/saveslots.js` | Save files stay separate across new game, load and reload |
| `node tests/forge.js` | Part 2 and 3 forge tiers unlock on time and cost the new materials |
| `node tests/signature.js` | Adult signature moves appear in the right fights and work |
| `node tests/textsize.js` | Text size cycles, scales menus and dialogue, is remembered, no sideways scroll on phones |
| `node tests/partygear.js` | Party gear slots open the forge (Back returns to Party) and find charms |
| `node tests/dev-panel.js` | The Dev tools panel opens in the dev copy |
| `node tests/render-songs.js` | Renders each song to WAV and reports levels |
| `python3 tests/balance.py N keys [tune] [profiles] [difficulty]` | Simulated boss fights: win rate, rounds, health left |
| `python3 tests/balance-patrols.py` | Simulated patrol fights |

Example: `python3 tests/balance.py 12 ch22,ch24 '' '' normal`

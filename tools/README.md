# Tools

Edit only `meteorite-kids-battle.html`. Never edit the dev copy by hand.

- `build-dev.py` builds `meteorite-kids-dev.html` from the main file: story gates off, everything unlocked, Dev tools panel added. Every replacement must match exactly once, so if a main-file change breaks one, the build stops and says which.
- `dev-tools.js` is the Dev tools panel code that `build-dev.py` adds.

```
python3 tools/build-dev.py [MAIN] [OUT]
```

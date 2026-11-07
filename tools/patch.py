"""Safe find-and-replace for patching the game file.

    from patch import Patch
    p = Patch()                       # src/meteorite-kids-battle.html by default
    p.rep('old text', 'new text')     # must match exactly once (or n=...)
    p.save()

Every replacement is checked first. If any count is wrong, nothing is written.
"""
import pathlib, sys

DEFAULT = pathlib.Path(__file__).resolve().parent.parent / 'src' / 'meteorite-kids-battle.html'

class Patch:
    def __init__(self, path=None):
        self.path = pathlib.Path(path or (sys.argv[1] if len(sys.argv) > 1 else DEFAULT))
        self.s = self.path.read_text(encoding='utf-8')

    def rep(self, a, b, n=1):
        c = self.s.count(a)
        if c != n:
            sys.exit(f'patch: expected {n} match(es), found {c}:\n  {a[:90]}')
        self.s = self.s.replace(a, b)

    def save(self):
        self.path.write_text(self.s, encoding='utf-8')
        print(f'patch: saved {self.path}')

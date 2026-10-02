#!/usr/bin/env python3
"""Generate en/index.html from index.html + i18n/en.json.

index.html (French) is the source of truth. Every translatable element carries
data-i18n="key" (or data-i18n-aria="key" for aria-label); this script swaps in
the English HTML and fails loudly if a key or a French string can't be found,
so the two pages can't silently drift apart.

Usage: python3 scripts/build-en.py           # write en/index.html
       python3 scripts/build-en.py --check   # exit 1 if en/index.html is stale
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC, DICT, OUT = ROOT / 'index.html', ROOT / 'i18n' / 'en.json', ROOT / 'en' / 'index.html'
BANNER = '<!-- GENERATED from index.html + i18n/en.json by scripts/build-en.py. Do not edit by hand. -->\n'


def build():
    html = SRC.read_text(encoding='utf-8')
    en = json.loads(DICT.read_text(encoding='utf-8'))
    errors = []

    for fr, tr in en['replace']:
        if fr not in html:
            errors.append(f'replace: French text not found: {fr[:70]!r}')
        html = html.replace(fr, tr)

    def swap_inner(m):
        key = m.group(3)
        if key not in en['strings']:
            errors.append(f'strings: missing key {key!r}')
            return m.group(0)
        return f'{m.group(1)}{en["strings"][key]}</{m.group(2)}>'

    html = re.sub(r'(<([a-z0-9]+)\b[^>]*\bdata-i18n="([^"]+)"[^>]*>).*?</\2>', swap_inner, html, flags=re.S)

    def swap_aria(m):
        key = m.group(2)
        if key not in en['attributes']:
            errors.append(f'attributes: missing key {key!r}')
            return m.group(0)
        return f'aria-label="{en["attributes"][key]}"{m.group(1)}'

    html = re.sub(r'aria-label="[^"]*"(\s+data-i18n-aria="([^"]+)")', swap_aria, html)

    if errors:
        sys.exit('build-en failed:\n  ' + '\n  '.join(errors))
    return html.replace('<!DOCTYPE html>\n', '<!DOCTYPE html>\n' + BANNER, 1)


if __name__ == '__main__':
    out = build()
    if '--check' in sys.argv:
        if not OUT.exists() or OUT.read_text(encoding='utf-8') != out:
            sys.exit('en/index.html is out of date: run python3 scripts/build-en.py')
        print('en/index.html is up to date')
    else:
        OUT.parent.mkdir(exist_ok=True)
        OUT.write_text(out, encoding='utf-8')
        print(f'wrote {OUT.relative_to(ROOT)}')

#!/usr/bin/env python3
"""Check skill packaging and evidence structure without network access or paid calls."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/higgsfield-director'
errors = []
text = (SKILL / 'SKILL.md').read_text()
front = re.match(r'^---\n(.*?)\n---\n', text, re.S)
if not front:
    errors.append('missing skill frontmatter')
else:
    keys = re.findall(r'^([a-z_]+):', front.group(1), re.M)
    if set(keys) != {'name', 'description'}:
        errors.append('skill frontmatter must contain only name and description')
    if 'name: higgsfield-director' not in front.group(1):
        errors.append('skill name mismatch')
words = len(text.split())
if words > 1300:
    errors.append(f'core skill exceeds 1300-word maintenance limit: {words}')
if len(text.splitlines()) > 180:
    errors.append('core skill exceeds 180-line maintenance limit')
linked = set()
for path in ROOT.rglob('*.md'):
    if '.git' in path.parts:
        continue
    body = path.read_text()
    if '\u2014' in body:
        errors.append(f'em dash in {path.relative_to(ROOT)}')
    if re.search(r'\b(?:TODO|FIXME)\b', body):
        errors.append(f'unresolved authoring marker in {path.relative_to(ROOT)}')
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', body):
        if '://' in target or target.startswith(('tool:', '#', 'mailto:')):
            continue
        target = target.split('#')[0]
        dest = (path.parent / target).resolve()
        if not dest.exists():
            errors.append(f'broken local link {path.relative_to(ROOT)} -> {target}')
        if path == SKILL / 'SKILL.md':
            linked.add(dest)
for path in (SKILL / 'references').glob('*.md'):
    if path.resolve() not in linked:
        errors.append(f'reference not directly linked from core: {path.name}')
for path in ROOT.rglob('*.json'):
    if '.git' in path.parts:
        continue
    try:
        json.loads(path.read_text())
    except (ValueError, UnicodeError) as error:
        errors.append(f'invalid JSON {path}: {error}')
sources = json.loads((ROOT / 'research/sources.json').read_text())['sources']
ids = [s['id'] for s in sources]
if len(ids) != len(set(ids)):
    errors.append('duplicate source IDs')
for row in sources:
    for key in ('id', 'title', 'url'):
        if not isinstance(row.get(key), str) or not row[key]:
            errors.append(f'invalid source field {row.get("id")}/{key}')
catalog = json.loads((ROOT / 'research/catalog-snapshot.json').read_text())
if not catalog['complete'] or catalog['count'] != len(catalog['items']):
    errors.append('catalog snapshot pagination/count mismatch')
if len({x['id'] for x in catalog['items']}) != len(catalog['items']):
    errors.append('duplicate catalog entries')
coverage = json.loads((ROOT / 'research/coverage.json').read_text())['entries']
if len(coverage) != len(catalog['items']) or {x['id'] for x in coverage} != {x['id'] for x in catalog['items']}:
    errors.append('coverage does not match observed catalog entries')
for entry in coverage:
    if not (SKILL / 'references' / entry['entry_reference']).is_file():
        errors.append(f'missing coverage reference for {entry["id"]}')
print(json.dumps({'ok': not errors, 'errors': errors, 'core_words': words,
                  'core_lines': len(text.splitlines()), 'reference_files': len(linked),
                  'source_records': len(sources), 'catalog_entries': len(catalog['items'])}, indent=2))
sys.exit(1 if errors else 0)

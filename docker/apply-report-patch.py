"""Apply the approved, hash-guarded HTML JSON escaping correction only."""
import difflib
import hashlib
import json
import sys
from pathlib import Path

before_sha = 'b8258dc83857b705e0fc538b779b3884cc4c9bdcdc6b34adec9b63b6b874af0a'
after_sha = '5f56ab2f96f3a2ec6d8dba23f265ab2085bad2700e25c3a92765128c11786811'
target, docs = map(Path, sys.argv[1:])
if target.is_symlink() or not target.is_file():
    raise SystemExit('report patch: expected a regular upstream module')
original = target.read_bytes()
if hashlib.sha256(original).hexdigest() != before_sha:
    raise SystemExit('report patch: upstream module identity mismatch; refusing to patch')
old = '    payload_json = json.dumps(payload)\n'
new = r'    payload_json = json.dumps(payload).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")' + '\n'
text = original.decode('utf-8')
if text.count(old) != 1:
    raise SystemExit('report patch: expected exactly one serialization line')
patched = text.replace(old, new).encode('utf-8')
if hashlib.sha256(patched).hexdigest() != after_sha:
    raise SystemExit('report patch: corrected module identity mismatch')
docs.mkdir(parents=True, exist_ok=True)
(docs/'plot_report.upstream.py').write_bytes(original)
diff = ''.join(difflib.unified_diff(text.splitlines(True), patched.decode().splitlines(True),
                                  fromfile='a/clipkit/plot_report.py', tofile='b/clipkit/plot_report.py'))
(docs/'report-json-escape.patch').write_text(diff, encoding='utf-8')
(docs/'report-patch.json').write_text(json.dumps({
    'name': 'TAFFISH HTML JSON escaping', 'upstream_version': '2.16.1',
    'module': 'clipkit/plot_report.py', 'original_sha256': before_sha,
    'patched_sha256': after_sha, 'scope': 'JSON embedding only; no algorithm or report data changes',
}, indent=2) + '\n', encoding='utf-8')
target.write_bytes(patched)
print('report patch: applied verified one-line JSON escaping correction')

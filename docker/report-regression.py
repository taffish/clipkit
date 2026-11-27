"""Exercise the HTML boundary and compare the corrected reporter with upstream."""
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

import clipkit.plot_report as patched
from clipkit import clipkit

docs = Path(__file__).resolve().parent
original_path = docs/'plot_report.upstream.py'
receipt = json.loads((docs/'report-patch.json').read_text())
assert hashlib.sha256(original_path.read_bytes()).hexdigest() == receipt['original_sha256']
assert hashlib.sha256(Path(patched.__file__).read_bytes()).hexdigest() == receipt['patched_sha256']
spec = importlib.util.spec_from_file_location('clipkit._taffish_original_report', original_path)
original = importlib.util.module_from_spec(spec); spec.loader.exec_module(original)

class Scripts(HTMLParser):
    def __init__(self):
        super().__init__(); self.scripts=[]; self.active=None
    def handle_starttag(self, tag, attrs):
        if tag=='script':
            self.active={'attrs':dict(attrs),'text':''}; self.scripts.append(self.active)
    def handle_data(self, text):
        if self.active is not None: self.active['text']+=text
    def handle_endtag(self, tag):
        if tag=='script': self.active=None

def raw_payload(html):
    return json.loads(html.split('<script id="payload" type="application/json">',1)[1].split('</script>\n  <script>\n    const data',1)[0])

labels = ['ordinary', 'quote\'"&<>中文', '</script><script>window.TAF_UNTRUSTED=1</script>',
          '</ScRiPt><script>window.TAF_UNTRUSTED=2</script>', '<!--<script>', 'Unicode\u2028line\u2029paragraph']
with tempfile.TemporaryDirectory(prefix='clipkit-report-', dir=os.environ.get('TMPDIR','/tmp')) as temp:
    root=Path(temp)
    run, stats=clipkit(raw_alignment='>one\nACGTACGT\n>two\nACGTA-GT\n',mode='gappy',gaps=0.5,sequence_type='nt')
    before_rows=run.msa.seq_records.copy(); before_stats=dict(stats.summary)
    for i,label in enumerate(labels):
        run.msa.header_info[0]['id']=label
        args=dict(msa=run.msa,mode='gappy',gaps=0.5,sequence_type='nt',ambiguity_handling='missing')
        old=root/f'original-{i}.html'; new=root/f'patched-{i}.html'
        original.write_trim_plot_report(str(old),**args); patched.write_trim_plot_report(str(new),**args)
        parser=Scripts(); html=new.read_text(); parser.feed(html)
        assert len(parser.scripts)==2, (i,'extra script element')
        data=json.loads(next(s['text'] for s in parser.scripts if s['attrs'].get('id')=='payload'))
        assert data['preview']['rows'][0]['label']==label, (i,'label changed')
        assert data==raw_payload(old.read_text()), (i,'report data changed')
        assert (run.msa.seq_records==before_rows).all() and stats.summary==before_stats
    # Run the real CLI against the same input/arguments in independent directories.
    # The control differs only in its report writer; analysis code is identical.
    control='import importlib,importlib.util; s=importlib.util.spec_from_file_location("clipkit._report_control",'+repr(str(original_path))+'); r=importlib.util.module_from_spec(s); s.loader.exec_module(r); c=importlib.import_module("clipkit.clipkit"); c.write_trim_plot_report=r.write_trim_plot_report; from clipkit.cli import main; main()'
    outputs=[]
    for name,entry in [('upstream',[sys.executable,'-c',control]),('corrected',[sys.executable,'-m','clipkit'])]:
        work=root/name; work.mkdir()
        (work/'input.fa').write_text('>'+labels[2]+'\nACGTACGT\n>two\nACGTA-GT\n')
        argv=entry+['input.fa','-m','gappy','-g','0.5','-o','output.fa','-l','-c','--report_json','report.json','--plot_trim_report','report.html']
        res=subprocess.run(argv,cwd=work,capture_output=True,text=True)
        if res.returncode:
            print(res.stdout,res.stderr,file=sys.stderr); raise SystemExit(res.returncode)
        data=json.loads((work/'report.json').read_text()); data.pop('runtime_seconds')
        outputs.append(([ (work/f).read_bytes() for f in ['output.fa','output.fa.log','output.fa.complement'] ],data,raw_payload((work/'report.html').read_text())))
    assert outputs[0]==outputs[1], 'CLI output or statistics changed'
print('REPORT_ESCAPE_OK: 6 exact label roundtrips; report data, alignment, complement, log and statistics unchanged')

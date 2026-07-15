# clipkit

`clipkit` packages ClipKIT for TAFFISH. ClipKIT trims multiple sequence
alignments for phylogenetic and phylogenomic analysis while preserving
phylogenetically informative sites.

Package identity:

- name: `clipkit`
- command: `taf-clipkit`
- kind: `tool`
- version: `2.13.0-r1`
- image: `ghcr.io/taffish/clipkit:2.13.0-r1`
- upstream: `JLSteenwyk/ClipKIT` tag `v2.13.0`
- upstream commit: `fb95e1b0d376cf3d03550666b550e704d253540a`
- runtime version: `clipkit 2.13.0`
- TAFFISH app license: Apache-2.0
- upstream license: MIT

## What This App Packages

The image installs the official PyPI `clipkit==2.13.0` wheel into a Python 3.11
virtual environment. The official PyPI source distribution is retained for
README, package metadata, and license provenance. Both artifacts are pinned by
SHA-256:

| Artifact | SHA-256 |
| --- | --- |
| `clipkit-2.13.0-py3-none-any.whl` | `4b52400df748d6d0ee7bb5e133465bd8ae5c7cc1fb95698896bce5e323ca4495` |
| `clipkit-2.13.0.tar.gz` | `a766e67e04d495ec17f635cf9904a802b6a552f2a6b09586252539ed9f862c56` |
| upstream `test.ecomp` fixture | `f9f9b2a1084757586a797708a5198156347164516393462a04a5cd624d568065` |

GitHub release assets and PyPI artifacts are separate builds with different
digests. This app intentionally uses the PyPI URLs and PyPI-published digests
listed above; checksums from the GitHub release page must not be substituted.

Runtime packages remain pinned to the validated Python 3.11 combination:

- `clipkit==2.13.0`
- `biopython==1.87`
- `numpy==1.26.4`
- `zstandard==0.25.0`

`zstandard` is included because zstd-encoded Evolutionary Compression
(`.ecomp`) archives require the optional module. Other `.ecomp` encodings are
handled by ClipKIT itself.

## Upstream 2.13.0 Changes

ClipKIT 2.13.0 adds opt-in masking of terminal, internal, or all in-frame stop
codons before alignment statistics and codon-aware trimming. The CLI option is
`--remove_stop_codons {terminal,internal,all}`; the Python API accepts the same
three values. DNA and RNA stop codons are recognized case-insensitively, and
terminal stops may be followed by trailing gap codons.

The feature requires nucleotide input, codon-aware processing, and an alignment
length divisible by three. Runtime text, log files, JSON reports, and Python API
results expose terminal, internal, and total masked-stop counts. Masking remains
disabled unless requested. Dependency bounds and external runtime requirements
are unchanged from 2.12.2.

## Scope

ClipKIT supports smart-gap, gap-fraction, entropy, composition-bias,
heterotachy, parsimony-informative, custom-site, codon-position, and related
trimming modes. It can optionally mask in-frame nucleotide stop codons and emit
logs, complementary alignments, JSON summaries, and standalone HTML trim
reports.

This app does not include an aligner, phylogenetic tree inference software,
model selection, downstream workflows, or reference datasets. Input must
already be a multiple sequence alignment.

## Usage

Run ClipKIT explicitly through TAFFISH command mode:

```sh
taf-clipkit clipkit alignment.fa -o alignment.clipkit.fa
taf-clipkit clipkit alignment.fa -m smart-gap -o smart-gap.fa
taf-clipkit clipkit alignment.fa -m gappy -g 0.8 -o gappy.fa
taf-clipkit clipkit alignment.fa -m kpic -o kpic.fa
taf-clipkit clipkit alignment.fa -m c3 -co -o no-third-codon.fa
taf-clipkit clipkit archive.ecomp -of fasta -o trimmed.fa
taf-clipkit clipkit coding.fa -m gappy -g 0.9 -s nt -co \
  --remove_stop_codons all --report_json stop-codons.json \
  -o coding.masked.fa
```

Generate provenance and report outputs:

```sh
taf-clipkit clipkit alignment.fa -l -c \
  --report_json report.json \
  --plot_trim_report report.html \
  -o trimmed.fa
```

Access wrapper and upstream help:

```sh
taf-clipkit --help
taf-clipkit -- --help
taf-clipkit clipkit --help
taf-clipkit -- --version
```

## Command Mode

The upstream CLI requires its input alignment as the first positional argument.
Because TAFFISH automatic command mode treats a first non-option argument as an
executable, use:

```sh
taf-clipkit clipkit alignment.fa -o trimmed.fa
```

Do not use `taf-clipkit alignment.fa ...`; that would try to execute a program
named `alignment.fa`. Explicit command mode also exposes the packaged Python
interpreter for script files:

```sh
taf-clipkit python analysis.py
```

## Inputs and Outputs

ClipKIT accepts FASTA, Clustal, MAF, Mauve, PHYLIP, Stockholm, and `.ecomp`
alignments through its upstream parsers. Output defaults to the input format;
use `-of fasta` or another supported format to override it.

Depending on options, ClipKIT writes the trimmed alignment, a per-site log,
the removed-site complementary alignment, JSON run metadata, and an HTML trim
report. Stop-codon masking counts appear in runtime, log, and JSON output when
the feature is enabled. Outputs are ordinary user files in the selected working
directory.

## Platform and Resources

The app targets native `linux/amd64` and `linux/arm64`. The Python package is
architecture-neutral; NumPy, Biopython, and zstandard provide compiled wheels
for both declared platforms. Memory use scales with alignment cells. ClipKIT
retains the 2.12.2 construction and counting optimizations for larger MSAs.

No network, database, model, or external reference is needed at runtime.

## Testing

Independent offline smoke covers:

- exact ClipKIT version, Python imports, source provenance, and native libraries
- stop-codon masking through the CLI and Python API, including output sequence
  and JSON counts
- real FASTA trimming with log, complement, JSON, and HTML report outputs
- validate-only mode and `.ecomp` decoding to FASTA
- a deterministic matrix above one million alignment cells that exercises the
  new batched count path and checks gap, entropy, composition, and frequency
  results

Dockerfile build-time checks intentionally use only normal CLI markers and a
tiny alignment. Stop-codon output assertions, the larger optimization-path
test, and HTML report generation stay in runtime smoke so multi-architecture
buildx/QEMU builds are not burdened by unnecessarily strong build-time tests.

Smoke validates packaging and representative execution, not every mode or
biological interpretation on production alignments.

## License and Citation

The TAFFISH app packaging is Apache-2.0. ClipKIT retains its MIT license, whose
text is included in the image.

Please cite Steenwyk et al., *ClipKIT: a multiple sequence alignment trimming
software for accurate phylogenomic inference*, PLOS Biology (2020), DOI
`10.1371/journal.pbio.3001007`.

Upstream resources:

- <https://github.com/JLSteenwyk/ClipKIT>
- <https://github.com/JLSteenwyk/ClipKIT/releases/tag/v2.13.0>
- <https://jlsteenwyk.com/ClipKIT/>

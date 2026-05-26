# clipkit

ClipKIT packaged as a TAFFISH tool app.

ClipKIT trims multiple sequence alignments for phylogenetic and phylogenomic
analysis. It keeps phylogenetically informative sites and can remove sites by
smart-gap, gap-fraction, entropy, composition-bias, heterotachy, parsimony
informativeness, custom-site, codon-position, and related modes.

## Package Identity

- Name: `clipkit`
- Command: `taf-clipkit`
- TAFFISH version: `2.12.0-r1`
- Kind: `tool`
- Container image: `ghcr.io/taffish/clipkit:2.12.0-r1`
- Upstream: `JLSteenwyk/ClipKIT` tag `v2.12.0`
- Upstream commit: `feb0a07903542f1b6b127b12d42065d93cd9f3e8`
- Runtime version: `clipkit --version` prints `clipkit 2.12.0`
- Upstream license: MIT
- TAFFISH packaging license: Apache-2.0

## What Is Included

The image installs ClipKIT 2.12.0 into a Python 3.11 virtual environment from
the PyPI wheel pinned by SHA256:

`41bbc7637f34faaeb6d564496bdd41ccd7ce3465219c6b7a4291524520edd4de`

The upstream PyPI source distribution is also downloaded and pinned by SHA256
so that upstream README, package metadata and MIT license text can be retained
in the image:

`e6fa1aa08bff0bf3962c38622ac3193dc9fd7c7adb4341058b34288e97c9ce80`

The upstream `test.ecomp` fixture is downloaded from the same GitHub tag and
pinned by SHA256 for `.ecomp` smoke coverage:

`f9f9b2a1084757586a797708a5198156347164516393462a04a5cd624d568065`

Runtime Python packages are version-pinned:

- `clipkit==2.12.0`
- `biopython==1.87`
- `numpy==1.26.4`
- `zstandard==0.25.0`

`zstandard` is included because ClipKIT can read Evolutionary Compression
(`.ecomp`) archives and upstream notes that zstd-encoded `.ecomp` payloads need
the optional Python module. Other `.ecomp` payload encodings are handled by
ClipKIT itself.

## Usage

Run ClipKIT's upstream CLI directly:

```bash
taf-clipkit clipkit alignment.fa -o alignment.clipkit.fa
taf-clipkit clipkit alignment.fa -m smart-gap -o smart-gap.fa
taf-clipkit clipkit alignment.fa -m gappy -g 0.8 -o gappy.fa
taf-clipkit clipkit alignment.fa -m kpic -o kpic.fa
taf-clipkit clipkit alignment.fa -m c3 -co -o no-third-codon.fa
taf-clipkit clipkit alignment.fa -l --report_json report.json --plot_trim_report report.html
taf-clipkit clipkit archive.ecomp -of fasta -o trimmed.fa
```

Wrapper help and upstream help are different:

```bash
taf-clipkit --help
taf-clipkit -- --help
taf-clipkit clipkit --help
taf-clipkit -- --version
```

Because this is a normal tool app, TAFFISH command mode is enabled. You can
also run tools in the same container environment explicitly:

```bash
taf-clipkit clipkit --version
taf-clipkit python -c 'import clipkit; print("ok")'
```

ClipKIT's upstream CLI requires the input alignment as the first positional
argument. With TAFFISH command mode enabled, `taf-clipkit alignment.fa ...`
means "run an executable named `alignment.fa` inside the container". Use the
explicit command-mode form `taf-clipkit clipkit alignment.fa ...` for normal
trimming. Use `taf-clipkit -- --help` and `taf-clipkit -- --version` only for
option-leading upstream calls.

## Boundaries

This package exposes ClipKIT itself plus the Python runtime needed by its
documented formats. It does not include multiple-sequence aligners, tree
inference tools, model-selection tools, downstream phylogenomic workflows, or
reference datasets.

ClipKIT works on existing alignments; it does not create the alignment. For raw
sequences, first align them with a separate tool such as MAFFT, MUSCLE, or
another aligner, then pass the aligned file to `taf-clipkit clipkit`.

ClipKIT supports FASTA, Clustal, MAF, Mauve, PHYLIP, Stockholm, and `.ecomp`
formats through its upstream parser. Output format defaults to the input
format; use `-of fasta` or another supported format when a different output
format is needed.

The smoke tests cover version binding, upstream help, Python imports,
dynamic-library sanity, source checksum provenance, a real FASTA trimming path
with log/complement/JSON/HTML-report output, validate-only mode, and `.ecomp`
input converted to FASTA. They do not replace biological validation of every
trimming mode on large production alignments.

## Reproducibility

- Upstream repository: `https://github.com/JLSteenwyk/ClipKIT`
- Upstream release: `https://github.com/JLSteenwyk/ClipKIT/releases/tag/v2.12.0`
- Upstream tag: `v2.12.0`
- Upstream tag commit: `feb0a07903542f1b6b127b12d42065d93cd9f3e8`
- Upstream wheel used by this image: PyPI `clipkit-2.12.0-py3-none-any.whl`
- Wheel SHA256: `41bbc7637f34faaeb6d564496bdd41ccd7ce3465219c6b7a4291524520edd4de`
- Upstream source used for docs: PyPI `clipkit-2.12.0.tar.gz`
- Source SHA256: `e6fa1aa08bff0bf3962c38622ac3193dc9fd7c7adb4341058b34288e97c9ce80`
- Upstream `.ecomp` fixture: `https://raw.githubusercontent.com/JLSteenwyk/ClipKIT/v2.12.0/test.ecomp`
- Fixture SHA256: `f9f9b2a1084757586a797708a5198156347164516393462a04a5cd624d568065`
- Build base: `python:3.11-slim-bookworm`
- Native platforms: `linux/amd64`, `linux/arm64`
- Citation: Steenwyk et al. ClipKIT: a multiple sequence alignment trimming
  software for accurate phylogenomic inference. PLOS Biology, 2020.
- DOI: `10.1371/journal.pbio.3001007`

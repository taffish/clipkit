# ClipKIT

`clipkit` packages ClipKIT for TAFFISH: trimming existing multiple sequence
alignments for phylogenetic and phylogenomic analysis.

- Command: `taf-clipkit`; kind: `tool`
- Candidate: `2.16.1-r1`
- Image: `ghcr.io/taffish/clipkit:2.16.1-r1`
- Upstream: [ClipKIT v2.16.1](https://github.com/JLSteenwyk/ClipKIT/releases/tag/v2.16.1)
- Commit: `4e2834c001fa2c82c5921ee7e52b4a58b59e3508`
- Packaging license: Apache-2.0; ClipKIT license: MIT

## Installation

After this exact version is published to the Hub, install it with
`taf install clipkit 2.16.1-r1`. For an unpublished local checkout,
maintainers can use `taf install --from .` from the app root instead.
TAFFISH and a working Docker, Podman or Apptainer backend are prerequisites;
the image supplies Python and the ClipKIT dependencies.

## Usage

Run from a writable project directory. Include the executable before the
alignment: a leading non-option argument selects TAFFISH command mode.

```sh
taf-clipkit clipkit alignment.fa -m smart-gap -o trimmed.fa
taf-clipkit clipkit alignment.fa -m gappy -g 0.8 -o gappy.fa
taf-clipkit clipkit ambiguous.fa -s nt --ambiguity_handling fractional -o aware.fa
taf-clipkit clipkit coding.fa -m gappy -g 0.9 -s nt -co \
  --remove_stop_codons all -o coding.masked.fa
taf-clipkit clipkit alignment.fa --validate_only --report_json check.json
taf-clipkit clipkit archive.ecomp -of fasta -o decoded.fa
```

Generate a trimmed alignment, per-site log, complementary alignment and reports:

```sh
taf-clipkit clipkit alignment.fa -o trimmed.fa -l -c \
  --report_json report.json --plot_trim_report report.html
```

Existing outputs may be overwritten. Use distinct input/output names and
create output directories first. For spaces, retain quotes in the argument
passed to the generated shell:

```sh
taf-clipkit clipkit '"input alignment.fa"' -o '"trimmed alignment.fa"'
```

`taf-clipkit alignment.fa ...` would incorrectly try to execute the alignment.
The packaged Python environment and upstream help are also accessible:

```sh
taf-clipkit python analysis.py
taf-clipkit --help
taf-clipkit -- --help
taf-clipkit clipkit --help
taf-clipkit -- --version
```

This app does not align sequences, infer trees, choose models, or run a
downstream scientific workflow. The CLI and Python API expose the upstream
trimming algorithms, modes and defaults.

## Inputs and Outputs

| Input | Use | Notes |
| --- | --- | --- |
| Multiple sequence alignment | Required | FASTA, Clustal, MAF, Mauve, PHYLIP, Stockholm or `.ecomp` |
| Custom-site file | Optional `-a` input | Position and `keep`/`trim` instructions for CST mode |
| Clade/tree-related inputs | Optional mode-specific inputs | User-supplied analysis inputs; see upstream help |
| Legacy `.ecomp` sidecar | Required for that legacy encoding | Keep matching metadata beside the archive |

Output normally keeps the input format; use `-of fasta` or another supported
format to override it. `-l` writes `OUTPUT.log`; `-c` writes
`OUTPUT.complement`. JSON records settings, counts and status.
`--validate_only` does not produce a trimmed alignment. Stop-codon masking
counts appear in runtime/log/JSON output.

ECOMP's gzip fallback checks gzip integrity but does not validate its separate
`checksum_sha256` metadata field; this inherited upstream behavior is not
changed here. Verify externally supplied archives against the provider's
whole-file hash. This package does not certify arbitrary input metadata.

Memory grows with alignment size; there is no fixed production-size guarantee.
The optional thread count is an upstream request, not a promise of linear
speedup. Failed runs can leave partial outputs: inspect errors and retry into
a fresh output location rather than treating file existence as success.

Upstream returns exit status 0 for some input validation failures, including
missing files and unreadable alignment formats, while printing an error and
producing no alignment. This package preserves that CLI behavior. Automation
must check the diagnostic and validate the expected output, not rely on exit
status alone. Use a fresh output path so an old file cannot masquerade as a
successful result.

## HTML Reports and Hosted Service

`--plot_trim_report report.html` generates the upstream standalone report.
Open it in a host browser; it starts no service and opens no container port.
It includes per-site tracks with hover values, an alignment preview, and
separate PNG export buttons. JavaScript/styles are embedded; only the optional
citation link needs a network connection.

The preview shows at most 25 sequences and 240 columns; the per-site tracks
describe the original alignment. Long tables scroll horizontally on narrow
screens. PNG previews truncate names to 36 characters; original names remain
in the alignment and report data. There is no upstream zoom, filtering,
upload form or multi-page dashboard.

Upstream also advertises a [hosted ClipKIT service](https://clipkit.genomelybio.com/).
It is independent of the CLI and is not bundled or called here. Its service
and data-handling terms are separate. This app does not upload alignments.

## Resources and Runtime Writes

No database, model, reference download or runtime network is required.
Alignments, custom-site files and clade inputs are project inputs, not an
installed catalog. No resource installer, automatic shared-library discovery
or persistent cache is added. The small bundled upstream `test.ecomp`
fixture is only for packaging verification.

The CLI reads supplied inputs and writes requested alignment/report/log files,
not its installation tree. Temporary scratch needs writable `/tmp`.
Ordinary-user execution does not require root. To share existing inputs, their
owner grants readers directory traversal and file read permission; each reader
writes outputs in their own project directory.

For host-owned Docker outputs, set
`TAFFISH_DOCKER_RUN_ARGS="--user $(id -u):$(id -g)"` for the command.
For rootless Podman, use
`TAFFISH_PODMAN_RUN_ARGS="--userns=keep-id --user $(id -u):$(id -g)"`.
Apptainer already runs as the invoking user. These are per-command choices;
they do not change shared directory permissions or the image's defaults.

For an existing readable `/srv/alignments` directory:

```sh
TAFFISH_CONTAINER_BACKEND=docker \
TAFFISH_DOCKER_RUN_ARGS='--volume /srv/alignments:/shared:ro' \
  taf-clipkit clipkit /shared/alignment.fa -o trimmed.fa

TAFFISH_CONTAINER_BACKEND=podman \
TAFFISH_PODMAN_RUN_ARGS='--volume /srv/alignments:/shared:ro' \
  taf-clipkit clipkit /shared/alignment.fa -o trimmed.fa

TAFFISH_CONTAINER_BACKEND=apptainer \
TAFFISH_APPTAINER_RUN_ARGS='--bind /srv/alignments:/shared:ro' \
  taf-clipkit clipkit /shared/alignment.fa -o trimmed.fa
```

These optional mounts do not install anything into `/srv`. Work from your own
writable project directory. Docker/Podman virtual machines must also be able
to access the host path. Do not change ownership or relabel a shared project
tree merely to make a container test pass.

## Version and Compatibility

2.16.0 optimizes residue counting, alignment copies and FASTA/ECOMP I/O.
2.16.1 consolidates CLI/API defaults, ECOMP validation/decoding and ends-only
trimming. These are upstream implementation changes, not local algorithm
patches. This app retains Python 3.12, Biopython 1.87, NumPy 1.26.4 and
zstandard 0.25.0. Record mode and options when comparing older results;
upstream benchmark claims do not replace validation on your own data.

The IUPAC policies introduced in 2.14.0 remain available:

- `missing` (default) treats recognized ambiguity symbols as unavailable for
  applicable counts and statistics.
- `fractional` distributes symbols over possible states for supported
  statistics; KPI/KPIC classification remains conservative.
- `literal` treats non-gap symbols as distinct states and helps reproduce
  pre-2.14 interpretations.

Configured gap characters take precedence; kept alignment symbols are not
rewritten. Default nucleotide `N/X` and protein `X` are gaps; to expand them
fractionally, choose an appropriate custom gap set such as `-gc '?*-'`.
In codon mode, KPI/KPIC can remove a whole codon for one singleton site.
Upstream discourages those modes for selection analyses. Biological
suitability remains the user's decision.

## Build and Provenance

### Report-only safety correction

This package applies one disclosed change to `clipkit/plot_report.py`: after
JSON serialization, `<`, `>` and `&` are encoded as JSON Unicode escapes before
embedding the payload in HTML. This prevents sequence names such as `</script>`
from ending the data element. Parsing the JSON restores the original names;
the trimming algorithms, report data, statistics and output alignments are
unchanged relative to the unpatched 2.16.1 reporter. Official 2.16.1 still
needs this correction; it is not an upstream release fix.

The hash-guarded patch generator is `docker/apply-report-patch.py`. The image
retains the exact diff (`report-json-escape.patch`), original report module,
before/after hashes (`report-patch.json`) and regression script under
`/opt/clipkit/share/doc/clipkit`. The regression compares six special-name
roundtrips and real CLI outputs against the original report writer; only the
elapsed-time field is excluded from byte-independent statistics comparison.

### Fixed inputs

Native targets are `linux/amd64` and `linux/arm64`. The official PyPI wheel
provides ClipKIT; zstandard supplies optional `.ecomp` zstd decoding.
No compiler is needed in the final image. Upstream README/metadata are under
`/opt/clipkit/share/doc/clipkit`; its MIT license is under
`/opt/clipkit/share/licenses/clipkit`.

| Input | Fixed identity |
| --- | --- |
| Python 3.12.16 slim Bookworm multi-platform base | `sha256:44cf1793efa7c7a476bb0f2cff81443f4a072c90c1cb127e2924933daa3e8c64` |
| `clipkit-2.16.1-py3-none-any.whl` | `08c27dd017852dded330a04946ec09f323c05215ef7aa8bfb1cfc59e946e6e85` |
| `clipkit-2.16.1.tar.gz` | `9de2b3273560618fa8624733ef2aaecc604deedeb5105c74af9ec12b5f4969a0` |
| `test.ecomp`, fixed commit | `f9f9b2a1084757586a797708a5198156347164516393462a04a5cd624d568065` |

Native dependency wheels are version/hash-locked in `docker/requirements.lock`.
PyPI artifacts and GitHub release files are separate builds; do not exchange
their checksums. Fixed hashes detect drift but cannot ensure upstream files
remain available. Missing artifacts require a reviewed successor candidate,
not silently dropping verification. The Dockerfile records this boundary.

The Action remains byte-identical to the TAFFISH 0.12.0 `taf new` template
with native amd64/arm64 runners; this update does not modify it.
Build-time tests use only version/help/import/linkage and a tiny alignment;
HTML rendering and larger regression matrices run after building.

## Troubleshooting

- Input treated as a command: include `clipkit` before the path.
- Spaces fail: preserve inner quotes as in the usage example.
- Permission denied: use your own writable output directory, not a read-only
  shared input mount or the installation tree.
- `.ecomp` fails: check the archive and matching legacy sidecar; never rename
  unrelated metadata just to satisfy the parser.
- Older results differ: record mode, gap definition, codon settings and
  ambiguity policy; `literal` is not the current default.

## Validation Status

The 2.16.1-r1 candidate passed fresh native builds and actual generated-wrapper
tests on ARM64 Docker/Podman and xjp native amd64 Docker/Podman/Apptainer.
The current image identities passed 198 exact manifest checks and 140 wrapper
checks, including ordinary-user/read-only execution, paths with spaces,
invalid-input recovery, repeated runs and shared read-only inputs. New-version
regressions cover CLI/API defaults, ends-only trimming and ECOMP integrity
boundaries. These results do not reuse the previous candidate's acceptance.

The final standalone reports passed browser rendering, literal-name and narrow
layout checks; direct offline opening, hover and both PNG exports were also
confirmed by the maintainer. Publication remains manual and has not occurred.
Rendering and larger regressions are post-build checks, not fragile ARM64
Dockerfile build gates.

Final Docker image sizes are 234602188 bytes (ARM64) and 224710015 bytes
(amd64); the amd64 SIF is 70905856 bytes. Python and native Python dependencies
account for most of the image. Build tools, downloaded wheel/source staging
and the application venv's pip are not retained. Base-image notices and
standard-library files remain intact.

The retained smoke suite covers exact identity/imports/libraries, CLI and
Python ambiguity handling, stop-codon masking, FASTA/log/complement/JSON/HTML
outputs, validation, `.ecomp`, mixed-case equivalence, a deterministic
matrix above one million cells, and the report-only escaping regression.
These are packaging tests, not scientific validation on production data.

## License and Citation

TAFFISH packaging is Apache-2.0; ClipKIT retains MIT. NumPy, Biopython,
zstandard, Python and system libraries retain their own notices in installed
distributions/base layers. No production datasets or models are bundled.

Cite Steenwyk et al., *ClipKIT: a multiple sequence alignment trimming
software for accurate phylogenomic inference*, PLOS Biology (2020),
[doi:10.1371/journal.pbio.3001007](https://doi.org/10.1371/journal.pbio.3001007).
See [upstream documentation](https://jlsteenwyk.com/ClipKIT/) for methods and
the complete option reference.

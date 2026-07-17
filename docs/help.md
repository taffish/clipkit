taf-clipkit 2.13.1-r1

Purpose:
  Run ClipKIT 2.13.1 to trim existing multiple sequence alignments for
  phylogenetic and phylogenomic analysis.

Usage:
  taf-clipkit clipkit ALIGNMENT [CLIPKIT-OPTIONS...]
  taf-clipkit -- --help
  taf-clipkit -- --version
  taf-clipkit COMMAND [ARGS...]

Common workflows:
  taf-clipkit clipkit alignment.fa -o alignment.clipkit.fa
  taf-clipkit clipkit alignment.fa -m smart-gap -o smart-gap.fa
  taf-clipkit clipkit alignment.fa -m gappy -g 0.8 -o gappy.fa
  taf-clipkit clipkit alignment.fa -m kpic -o kpic.fa
  taf-clipkit clipkit codon.fa -m c3 -co -o no-third-codon.fa
  taf-clipkit clipkit archive.ecomp -of fasta -o trimmed.fa
  taf-clipkit clipkit coding.fa -m gappy -g 0.9 -s nt -co \
    --remove_stop_codons all --report_json stops.json -o coding.masked.fa

Reports and provenance:
  taf-clipkit clipkit alignment.fa -l -c --report_json report.json \
    --plot_trim_report report.html -o trimmed.fa

Main upstream options:
  -o, --output FILE             Output alignment.
  -m, --mode MODE               Select the trimming mode.
  -g, --gaps FLOAT              Set the gap threshold.
  -if, --input_file_format FMT  Override input format detection.
  -of, --output_file_format FMT Select output format.
  -s, --sequence_type nt|aa     Set sequence type.
  -a, --auxiliary_file FILE     Auxiliary input for modes such as cst.
  -l, --log                     Write a per-site log.
  -c, --complementary           Write trimmed-away sites.
  -co, --codon                  Trim codons as units.
  --remove_stop_codons MODE     Mask terminal, internal or all in-frame stops.
  -eo, --ends_only              Trim only alignment ends.
  -t, --threads N               Request a thread count.
  --dry_run                     Compute without writing normal outputs.
  --validate_only               Validate input and settings only.
  --report_json [FILE]          Write a machine-readable run report.
  --plot_trim_report [FILE]     Write a standalone HTML trim report.

Modes:
  smart-gap, entropy, gappy, block-gappy, gappyout, composition-bias,
  heterotachy, kpic, kpic-smart-gap, kpic-gappy, kpi, kpi-smart-gap,
  kpi-gappy, cst and c3.

Inputs:
  FASTA, Clustal, MAF, Mauve, PHYLIP, Stockholm or .ecomp alignment.
  The input must already be aligned; ClipKIT is not an aligner.

Key outputs:
  Trimmed alignment, optional per-site log and complementary alignment,
  optional JSON summary, and optional HTML trim report. Stop-codon masking
  counts are reported in runtime, log and JSON output when enabled.

Command mode:
  Use "taf-clipkit clipkit alignment.fa ..." for normal trimming.
  "taf-clipkit alignment.fa ..." would try to execute alignment.fa because
  the first non-option argument activates TAFFISH command mode.
  The packaged environment also exposes Python for script files:
    taf-clipkit python analysis.py

Version 2.13.1:
  This performance patch preserves existing trimming behavior and public APIs.
  It reduces repeated column counting in gappy/smart-gap and KPI/KPIC combined
  modes, while preserving mixed-case behavior. Stop-codon, entropy,
  composition-bias and codon-site paths are also faster.

Stop-codon masking since 2.13.0:
  --remove_stop_codons masks terminal, internal or all in-frame DNA/RNA stop
  codons before trimming. It requires nucleotide input, codon mode and an
  alignment length divisible by three. Masking is disabled by default.

Platform and resources:
  Native linux/amd64 and linux/arm64 are supported.
  Memory scales with alignment cells; no database or runtime network is needed.

Boundaries:
  Aligners, phylogenetic inference, model selection, downstream workflows and
  reference datasets are not included.

Detailed documentation:
  https://github.com/taffish/clipkit
  https://jlsteenwyk.com/ClipKIT/

Wrapper options:
  taf-clipkit --help       Show this TAFFISH help.
  taf-clipkit --version    Show TAFFISH wrapper version.
  taf-clipkit --compile    Print generated shell code.
  taf-clipkit -- --help    Pass option-leading arguments to ClipKIT.

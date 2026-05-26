taf-clipkit 2.12.0-r1

ClipKIT 2.12.0 packaged for TAFFISH. ClipKIT trims multiple sequence
alignments for phylogenetic and phylogenomic analysis.

Usage:
  taf-clipkit clipkit alignment.fa [clipkit options]
  taf-clipkit clipkit [arguments...]
  taf-clipkit python [arguments...]

Wrapper options:
  taf-clipkit --help       Show this TAFFISH help text
  taf-clipkit --version    Show TAFFISH package version
  taf-clipkit --compile    Print generated shell code instead of running
  taf-clipkit -- ...       Pass option-leading arguments to clipkit

Default upstream command:
  clipkit

Upstream help and version:
  taf-clipkit -- --help
  taf-clipkit -- --version
  taf-clipkit clipkit --help
  taf-clipkit clipkit --version

Common workflows:
  Default smart-gap trimming:
      taf-clipkit clipkit alignment.fa -o alignment.clipkit.fa

  Gap-fraction trimming:
      taf-clipkit clipkit alignment.fa -m gappy -g 0.8 -o gappy.fa

  Keep parsimony informative and constant sites:
      taf-clipkit clipkit alignment.fa -m kpic -o kpic.fa

  Codon-aware third-position removal:
      taf-clipkit clipkit codon-alignment.fa -m c3 -co -o no-third-codon.fa

  Log, JSON summary and HTML trim report:
      taf-clipkit clipkit alignment.fa -l --report_json report.json \
        --plot_trim_report report.html -o trimmed.fa

  Evolutionary Compression archive to FASTA:
      taf-clipkit clipkit archive.ecomp -of fasta -o trimmed.fa

Main upstream options:
  -o, --output FILE             output file
  -m, --mode MODE               smart-gap, entropy, gappy, block-gappy,
                                gappyout, composition-bias, heterotachy,
                                kpic, kpic-smart-gap, kpic-gappy, kpi,
                                kpi-smart-gap, kpi-gappy, cst or c3
  -g, --gaps FLOAT              gap threshold
  -if, --input_file_format FMT  input format
  -of, --output_file_format FMT output format
  -s, --sequence_type nt|aa     sequence type
  -a, --auxiliary_file FILE     auxiliary file for modes such as cst
  -l, --log                     write per-site log
  -c, --complementary           write trimmed-away complement alignment
  -co, --codon                  trim codons as units
  -eo, --ends_only              trim only alignment ends
  -t, --threads N               requested thread count
  --dry_run                     compute trimming and stats without writing
  --validate_only               validate input/settings without trimming
  --report_json [FILE]          write machine-readable run report
  --plot_trim_report [FILE]     write HTML trim plot report

Command mode:
  TAFFISH command mode is enabled. If the first argument is a non-option
  executable name, it is run inside the same container environment:

      taf-clipkit clipkit --version
      taf-clipkit clipkit alignment.fa -o trimmed.fa
      taf-clipkit python -c 'import clipkit; print("ok")'

  Because upstream ClipKIT requires the input alignment as the first positional
  argument, taf-clipkit alignment.fa ... is interpreted as command mode and
  will try to run an executable named alignment.fa. Use taf-clipkit clipkit
  alignment.fa ... for normal trimming. Use taf-clipkit -- --help and
  taf-clipkit -- --version for option-leading upstream calls.

Packaged runtime:
  Python 3.11 virtual environment with clipkit 2.12.0, Biopython, NumPy and
  zstandard. The zstandard module is included for zstd-encoded .ecomp archives.

Formats:
  ClipKIT supports FASTA, Clustal, MAF, Mauve, PHYLIP, Stockholm and .ecomp
  inputs through its upstream parser. Output defaults to the input format; use
  -of when a specific output format is required.

Boundaries:
  This app packages ClipKIT itself. It does not include aligners, phylogenetic
  tree inference tools, model-selection tools, downstream workflows or
  reference datasets.

Citation:
  Steenwyk et al. ClipKIT: a multiple sequence alignment trimming software for
  accurate phylogenomic inference. PLOS Biology, 2020.
  DOI: 10.1371/journal.pbio.3001007

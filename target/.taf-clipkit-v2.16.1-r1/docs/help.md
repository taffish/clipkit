taf-clipkit 2.16.1-r1

Purpose:
  Trim an existing multiple sequence alignment with ClipKIT.

Usage:
  taf-clipkit clipkit ALIGNMENT [OPTIONS...]
  taf-clipkit -- --help
  taf-clipkit -- --version

Common tasks:
  taf-clipkit clipkit alignment.fa -m smart-gap -o trimmed.fa
  taf-clipkit clipkit alignment.fa -m gappy -g 0.8 -o trimmed.fa
  taf-clipkit clipkit alignment.fa -o trimmed.fa -l -c \
    --report_json report.json --plot_trim_report report.html
  taf-clipkit clipkit alignment.fa --validate_only --report_json check.json
  taf-clipkit clipkit archive.ecomp -of fasta -o trimmed.fa
  taf-clipkit clipkit coding.fa -s nt -co --remove_stop_codons all \
    -m gappy -g 0.9 -o coding.masked.fa
  taf-clipkit python analysis.py

Required inputs:
  An aligned FASTA, Clustal, MAF, Mauve, PHYLIP, Stockholm or .ecomp file.
  Legacy .ecomp files also need their matching metadata sidecar beside them.

Common options:
  -o FILE                 Output alignment (existing files can be overwritten).
  -m MODE                 Trimming mode; see upstream --help for all modes.
  -g FLOAT                Gap threshold for applicable modes.
  -s nt|aa                Sequence type.
  -if FORMAT / -of FORMAT Input/output format override.
  --ambiguity_handling missing|fractional|literal
                          IUPAC handling; default: missing.
  -a FILE                 Auxiliary input, such as custom-site instructions.
  -co                     Trim nucleotide codons as units.
  --remove_stop_codons terminal|internal|all
                          Mask in-frame stops in nucleotide codon mode.
  -l / -c                 Write the per-site log / removed-site alignment.
  --report_json [FILE]     Write run metadata.
  --plot_trim_report [FILE] Write a standalone HTML report.

Key outputs:
  Trimmed alignment; optional .log, .complement, JSON and HTML files.
  Open the HTML in a host browser; its two PNG buttons export the plots.

Immediate notes:
  Always include "clipkit" before the input path; a bare path selects a command.
  Work in a writable project directory and choose distinct output names.
  Some upstream input errors return status 0; check diagnostics and output.
  For paths with spaces, preserve inner quotes through the wrapper:
    taf-clipkit clipkit '"input alignment.fa"' -o '"trimmed alignment.fa"'
  No runtime download, database or model is needed.
  KPI/KPIC with -co can remove a whole codon for one singleton site;
  upstream does not recommend those modes for selection analyses.

More help:
  taf-clipkit clipkit --help
  https://github.com/taffish/clipkit

Wrapper options:
  taf-clipkit --help       Show this usage help.
  taf-clipkit --version    Show wrapper metadata.
  taf-clipkit --compile    Print generated shell code.
  taf-clipkit -- --help    Pass option-leading arguments to ClipKIT.

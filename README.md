# pysster_playbox

## Foreword
This repository contains a small toolkit designed to swiftly split an arbitrary fasta sequence up to be compatible with a fixed input size of pysster models. The split input intended to be regenerated into continuos signal over the input ready for visualisation in the genomic browser of choice. 

## Usage

### Setup
One would need to setup the environment and install pysster. Due to old dependencies, it is recommended to setup a separate environemt for pysster to avoid conflict with newer python packages:
```bash
git clone https://github.com/melonheader/pysster_playbox.git
cd pysster_playbox
conda env create -f pysster_playbox/auxiliary/pysster.yaml
```
### Main tool
The package contains three scripts to:
1) split the input fasta into windows
2) run predictions
3) reformat `pysster` outptu into `wiggle`
```bash
python pwm_score/scripts/prep_fasta.py --help
usage: prep_fasta.py [-h] [-fi FASTA_IN] [-sl SPLIT_LENGTH] [-ss SLIDE_SIZE] [-fo FASTA_OUT]

A script to prepare a fasta file input for pysster processing

options:
  -h, --help            show this help message and exit
  -fi FASTA_IN, --fasta-in FASTA_IN
  -sl SPLIT_LENGTH, --split-length SPLIT_LENGTH
  -ss SLIDE_SIZE, --slide-size SLIDE_SIZE
  -fo FASTA_OUT, --fasta-out FASTA_OUT

python pysster_playbox/scripts/psst_predict.py --help
usage: psst_predict.py [-h] [-m MODEL_PATH] [-o OUTPUT_DIR] [-s SUFFIX] [--fasta-in FASTA_IN [FASTA_IN ...]]

Simple script to run pysster predict over a selected sequence split

optional arguments:
  -h, --help            show this help message and exit
  -m MODEL_PATH, --model-path MODEL_PATH
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
  -s SUFFIX, --suffix SUFFIX
  --fasta-in FASTA_IN [FASTA_IN ...]

python pysster_playbox/scripts/preds_to_wig.py --help
usage: preds_to_wig.py [-h] -i INPUT [INPUT ...] -o OUTPUT_DIR -g GENOME_POSITION -s SPAN

Convert CSV to WIG format

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT [INPUT ...], --input INPUT [INPUT ...]
                        Input CSV files (supports globbing, e.g., '*.csv')
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Path to output WIG file
  -g GENOME_POSITION, --genome-position GENOME_POSITION
                        Genomic position (e.g., chr1:1000)
  -s SPAN, --span SPAN  Span of each WIG entry (window size)
```
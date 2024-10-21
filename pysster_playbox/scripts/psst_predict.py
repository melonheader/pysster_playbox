#!/usr/bin/env python
from pathlib import Path
import argparse
from pysster import Data, Model
from pysster import utils
"""
Simple script to run pysster predict over a selected sequence split.
"""

parser = argparse.ArgumentParser(description='Simple script to run pysster predict over a selected sequence split')
parser.add_argument('-m', '--model-path', type=str, default=None)
parser.add_argument('-o', '--output-dir', default='.')
parser.add_argument('-s', '--suffix', default='')
parser.add_argument('--fasta-in', nargs='+')
args = parser.parse_args()

model_path = Path(args.model_path)
out_path = Path(args.output_dir)

pyss_data = Data.Data(args.fasta_in, alphabet='ACGT')
pyss_model = utils.load_model(model_path)
pyss_preds = pyss_model.predict(pyss_data, "all")

if args.suffix:
    args.suffix='_' + args.suffix
with open(str(out_path.joinpath('predictions' + args.suffix + '.csv')), 'w') as f:
    print('score_0,score_1,score_2', file=f)
    for (s_0, s_1, s_2) in pyss_preds:
        print(f'{s_0},{s_1},{s_2}', file=f)
#!/usr/bin/env python
import pandas as pd
import argparse
import glob
import os

"""
A script reprocess predictions to wiggle format that can visualised in genomic browsers. 
"""

def parse_args():
    parser = argparse.ArgumentParser(description="Convert CSV to WIG format")
    parser.add_argument("-i", "--input", required=True, nargs='+', help="Input CSV files (supports globbing, e.g., '*.csv')")
    parser.add_argument("-o", "--output-dir", required=True, help="Path to output WIG file")
    parser.add_argument("-g", "--genome-position", type=str, required=True, help="Genomic position (e.g., chr1:1000)")
    parser.add_argument("-s", "--span", type=int, required=True, help="Span of each WIG entry (window size)")
    args = parser.parse_args()
    input_files = []
    for pattern in args.input:
        input_files.extend(glob.glob(pattern))
    if not input_files:
        raise FileNotFoundError("No prediction tables found matching the provided patterns.")
    args.input = input_files
    return args

def csv_to_wig(csv_file, output_file, genome_position, span, track_name):
    chrom, start_pos = genome_position.split(':')
    start_pos = int(start_pos)
    df = pd.read_csv(csv_file)
    scores = df['score_0']
    with open(output_file, 'w') as wig_file:
        wig_file.write(f"track type=wiggle_0 name={track_name}\n")
        wig_file.write(f"variableStep chrom={chrom} span={span}\n")
        current_start = start_pos
        for score in scores:
            wig_file.write(f"{current_start}\t{score}\n")
            current_start += span

if __name__ == "__main__":
    args = parse_args()
    for csv_file in args.input:
        base_name = os.path.basename(csv_file)
        if base_name.startswith("predictions_"):
            base_name = base_name[len("predictions_"):]
        base_name = os.path.splitext(base_name)[0]
        output_file = os.path.join(args.output_dir, base_name + ".wig")
        print(f"Processing {csv_file} -> {output_file}")
        csv_to_wig(csv_file, output_file, args.genome_position, args.span, base_name)
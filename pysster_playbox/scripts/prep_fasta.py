#!/usr/bin/env python
from pathlib import Path
import argparse
import os

"""
A script to prepare a fasta file input for pysster processing. Given that pysster predicts on the per-sequence basis and
the trained models have an input size of 400, fasta input needs to be cut into splits prior to predictions and then
reassembled to generate a continuous signal over the input sequence. Ths size of the sliding window is controlled by
the -ss argument (defaults to 20 bases).
"""

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-fi', '--fasta-in', type=str, default=None)
    parser.add_argument('-sl', '--split-length', type=int, default=400)
    parser.add_argument('-ss', '--slide-size', type=int, default=20)
    parser.add_argument('-fo', '--fasta-out', type=str, default=None)
    args = parser.parse_args()
    return args

def read_fasta(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        header = lines[0].strip().strip(">")
        sequence = ''.join(line.strip() for line in lines[1:])
    return header, sequence

def write_fasta(file_path, header, sequences):
    with open(file_path, 'w') as file:
        for i, seq in enumerate(sequences):
            file.write(f">{header}_part_{i+1}\n")
            file.write(f"{seq}\n")

def pad_right(sequence, length):
    return sequence + ('N' * length)
def pad_left(sequence, length):
    return ('N' * length) + sequence

def split_sequence(sequence, length, slide):
    side_window = int((length - slide) / 2)
    subsequences = []
    for seq_start in range(0, len(sequence), slide):
        seq_end = seq_start + slide
        lhs_start = int(seq_start - side_window)
        rhs_end = int(seq_end + side_window)
        if lhs_start < 0:
            lhs_start = 0
        if rhs_end > len(sequence):
            rhs_end = len(sequence)
        subseq = sequence[lhs_start:rhs_end]
        ##
        lhs_length = seq_start - lhs_start
        if lhs_length < side_window:
            subseq = pad_left(subseq, side_window - lhs_length)
        rhs_length = rhs_end - seq_end 
        if rhs_length < side_window:
            subseq = pad_right(subseq, side_window - rhs_length)
        subsequences.append(subseq)
    return subsequences

def split_fa(input_fasta, output_fasta, split_length, slide_size):
    header, sequence = read_fasta(input_fasta)
    subsequences = split_sequence(sequence, split_length, slide_size)
    write_fasta(output_fasta, header, subsequences)

if __name__ == "__main__":
    args = parse_args()
    split_fa(input_fasta=Path(args.fasta_in), output_fasta=Path(args.fasta_out), split_length=args.split_length, slide_size=args.slide_size)
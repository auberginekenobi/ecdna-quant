#!/bin/python3


import argparse
import os
import gzip

parser = argparse.ArgumentParser()
parser.add_argument('SORT_FILE')
parser.add_argument('OUT_ROOT')
parser.add_argument('BARCODES')
args=parser.parse_args()

#SORT_FILE="test_atac_fragments.bed"
SORT_FILE=args.SORT_FILE #"rcmb56_ht_atac_fragments.bed"
OUT_ROOT=args.OUT_ROOT #"RCMB56-ht/"
BARCODES=args.BARCODES

# Get list of valid barcodes
valid_barcodes=set()
with gzip.open(BARCODES, 'rt') as f:
	for line in f:
		valid_barcodes.add(line.strip())

PREV=None
with open(SORT_FILE,'r') as f:
	for line in f:
		bc = line.split()[3]
		if bc in valid_barcodes:
			if bc != PREV:
				if PREV != None:
					g.close()
				out_dir=os.path.join(OUT_ROOT,bc)
				if not os.path.exists(out_dir):
					os.makedirs(out_dir)
				outfile=os.path.join(out_dir,bc+'.bed')
				g=open(outfile,'w')
				PREV=bc
			g.write(line)

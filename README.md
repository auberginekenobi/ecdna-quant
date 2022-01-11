# ecdna-quant

Quantify ecDNA in 10X single-cell ATAC (scATAC-seq) sequencing.

Owen Chapman
University of California San Diego

## Description

This module estimates the abundance of a known extrachromosomal circular DNA sequence (ecDNA) in single cells from 10x Genomics scATAC-seq data. The approach counts reads mapping to the ecDNA region, then compares this value to an empirically derived null distribution of read coverage elsewhere in the genome. ecDNA+ cells are identified which have significantly greater scATAC-seq coverage than expected by the null. 

## Materials

To use this module, the following are required:
- 10X Genomics single-cell ATAC-seq (scATAC-seq) data
- Genomic co-ordinates of an ecDNA amplification in your sample. We have used [AmpliconArchitect](https://github.com/virajbdeshpande/AmpliconArchitect) to generate these data from bulk WGS.

## Installation & Dependencies

Currently, this module is a bash script with python 3 dependencies. Future versions will include a containerized Docker version.

Dependencies:

- python 3
-- argparse
-- gzip
-- pyranges
-- pandas
-- seaborn
-- matplotlib
-- statsmodels
- bedtools 2

## Usage



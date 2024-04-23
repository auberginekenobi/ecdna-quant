# ecdna-quant

Quantify ecDNA in 10X single-cell ATAC (scATAC-seq) sequencing.

Owen Chapman
University of California San Diego

## Description

This module estimates the abundance of a known extrachromosomal circular DNA sequence (ecDNA) in single cells from 10x Genomics scATAC-seq data. The approach counts reads mapping to the ecDNA region, then compares this value to an empirically derived null distribution of read coverage elsewhere in the genome. ecDNA+ cells are identified which have significantly greater scATAC-seq coverage than expected by the null. 

## Materials

To use this module, the following are required:
- Single-cell or spatial sequencing data such as that produced by the 10X Genomics single-cell ATAC-seq (scATAC-seq) workflow. 
- Genomic co-ordinates of an ecDNA amplification in your sample. We have used [AmpliconArchitect](https://github.com/AmpliconSuite/AmpliconArchitect) to generate these data from bulk WGS.  

## Installation & Dependencies

Currently, this module is a bash script with python 3 dependencies. Compatible with Linux (Ubuntu 16) and Mac OS (M1) operating systems. Future versions may include a proper package and containerized Docker version if I ever get around to it.

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

Copy the example `config` file to your desired project directory and edit to point to paths of the required files. Set the `$ECQ_HOME` environment variable to the root directory for this repository, eg. `Users/ochapman/software/ecdna-quant`. Run using the command `$ECQ_HOME/src/ecdna-quant config`.

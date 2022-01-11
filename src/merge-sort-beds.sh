#!/bin/bash

# USAGE
# generate-exclude-bed.sbatch bed1 bed2 ...

# DEPENDENCIES
# bedtools2

# Generate exclude .bed
module load cpu/0.15.4 gcc/10.2.0 bedtools2
cat $@ | awk -v OFS='\t' '{print $1, $2, $3}' | bedtools sort -i - | bedtools merge -i -

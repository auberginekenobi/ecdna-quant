#!/bin/bash

# USAGE
# merge-sort-beds.sh bed1 bed2 ...

# DEPENDENCIES
# bedtools2

# Generate exclude .bed
cat $@ | awk -v OFS='\t' '{print $1, $2, $3}' | bedtools sort -i - | bedtools merge -i -

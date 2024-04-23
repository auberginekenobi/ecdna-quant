import argparse

# args
parser = argparse.ArgumentParser('Find the total length of regions in a bed file.')
parser.add_argument('bedfile',help='bedfile')
args = parser.parse_args()

def bed_length(file):
    with open(file,'r') as f:
        length = 0
        for line in f:
            if line.startswith('#'):
                continue
            else:
                cols = line.split('\t')
                length += int(cols[2]) - int(cols[1])
        return length

try:
    print(bed_length(args.bedfile))
except:
    raise ValueError("This doesn't look like a .bed file.")
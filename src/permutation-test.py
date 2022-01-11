import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.multitest import multipletests

def load_counts(file, ecDNA_len):
    '''
    Loads output of count-fragments. format is barcode \t count.
    returns: pd.Series of index: barcode
    '''
    s = pd.read_csv(file,sep='\t',index_col=0)
    #s = select_qc_passed_cells(s)
    s /= ecDNA_len
    return s.squeeze()

def load_backgrounds(file):
    '''
    Loads output of count-fragments. 
    returns: dataframe
    rows: barcodes
    column: random permutation region
    access as df[barcode.bam]
    '''
    df = pd.read_csv(file,sep='\t',index_col=0)
    #df = select_qc_passed_cells(df)
    return df

def estimate_pvalues(observed,backgrounds):
    '''
    For each cell:
    Estimates an empirical p-value as the fraction of permutation regions with 
    greater scATAC-seq depth than the query.
    Computes a z-score from the sample standard deviation of the permutations.
    Parameters:
     - observed (pd.Series). Read counts at the ecDNA locus. See load_counts.
     - backgrounds (pd.DataFrame). Read counts at the permutation regions.
       See load_backgrounds.
    Returns: long-form pd.DataFrame with the following columns:
       "Observed" "empirical p-val" "z-score"
    '''
    # Set up dataframe of observed featurecounts    
    df = pd.DataFrame(observed)
    df.columns=['Observed']
    
    # Estimate empirical p
    bg=backgrounds
    df['empirical p-val']=observed.index.map(lambda x: ((observed[x] <= bg.loc[x]).sum()+1) / (len(bg.loc[x])+1))
    
    # Sample standard deviation
    df['z-score']=observed.index.map(lambda x: abs(observed[x] - bg.loc[x].mean())/bg.loc[x].std())
    
    return df

def gen_histograms(observed,backgrounds,outfile_prefix=None):
    '''
    For an arbitrary 36 cells,
    Plot a histogram of the empirical null distribution against the actual 
    density of scATAC reads at the ecDNA locus.
    Parameters:
     - observed (pd.Series). Read counts at the ecDNA locus. See load_counts.
     - backgrounds (pd.DataFrame). Read counts at the permutation regions.
       See load_backgrounds.
     - outfile_prefix (str). Provide a path or filename (minus the extension)
       to save .svg and .png files.
    '''
    w=6
    h=6
    df = estimate_pvalues(observed,bg)
    observed=observed.loc[df.index]
    backgrounds=backgrounds.loc[df.index]
    fig,axes = plt.subplots(h,w, figsize=(20,20))
    for i in range(h*w):
        sns.histplot(ax=axes[i//h,i%h],data=backgrounds.iloc[i,:],binwidth=1)
        # observed value
        axes[i//h,i%h].axvline(df.iloc[i,0],c='red')
        text = 'empirical p<'+str(round(df.iloc[i,1],3))
        axes[i//h,i%h].text(0.9,0.8,text,horizontalalignment='right',transform=axes[i//h,i%h].transAxes)
    if outfile_prefix != None:
        fig.savefig(outfile_prefix+'.svg')
        fig.savefig(outfile_prefix+'.png')
        
def classify(fgs,bg):
    '''
    Iterator for estimate_pvalues. Performs estimate_pvalues on a list of ecDNAs.
    Parameters:
     - fgs (list of pd.Series). Read counts at the ecDNA locus. See load_counts.
     - bg (pd.DataFrame). Read counts at the permutation regions.
       See load_backgrounds.
    '''
    classifications = pd.DataFrame()
    for i in range(len(fgs[0:])):
        df = estimate_pvalues(fgs[i],bg)
        e = multipletests(df['empirical p-val'],alpha=0.10,method='fdr_bh')
        base='ecDNA'+str(i+1)
        classifications[base+"_z-score"] = df['z-score']
        classifications[base+"_p-val"] = df['empirical p-val']
        classifications[base+"_q-val"] = e[1]
        classifications[base+"_status"] = e[0]
    return classifications

#######################

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--ecdna_counts',nargs='+',help="1+ ecDNA counts files from count-fragments.py", required=True)
    parser.add_argument('--bg_counts',help="Counts file for the background regions from count-fragments",required=True)
    parser.add_argument('--ecdna_lengths',nargs='+',help="Length in Mbp of each ecDNA.",required=True)
    parser.add_argument('--put_file')
    args = parser.parse_args()

    fgs = [load_counts(f) for f in args.ecdna_counts]
    bg = load_backgrounds(args.bg_counts)
    for i in range(len(fgs)):
        gen_histograms(fgs[i],bg,'ecDNA'+str(i+1))
    c = classify(fgs,bg)
    c.to_csv(args.out_file,sep='\t')
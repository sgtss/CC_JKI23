#!/usr/bin/env python

import os
import pandas as pd
import seaborn as sb

# change working dir to CC3 and store in a variable for use later
os.chdir(os.path.normpath(os.path.join(os.path.dirname(__file__), '../')))
wrk_dir = os.getcwd()

# path to metadata file, Admixture Q file and plot file
mfile = f'{wrk_dir}{"/data/maize_samples.txt"}'
qfile = f'{wrk_dir}{"/data/maize.3.Q"}'
pfile = f'{wrk_dir}{"/results/maize.3.pdf"}'

# read files in pandas dataframes
df_meta = pd.read_csv(mfile, sep='\t')                                      # reading and storing metadat
df_Q = pd.read_csv(qfile, sep=' ', header=None)                             # reading and storing Q values

# set column headers (ancestory fractions as frac for K=3), concatanate both dataframes and filter for maize 
df_Q.columns = ["Frac{}".format(i) for i in range(1, df_Q.shape[1]+1)]      # looping through columns, increment by +1 and setting column name
df_comb = pd.concat([df_meta, df_Q], axis=1)                                # concatenating both dataframes, as both are same size; otherwise use merge
df_comb = df_comb[df_comb['species'] == 'Zea mays ssp. mays']               # filtering for maize samples only

# index by sample id, sort by altitude and save as new df
df_comb.set_index('sample_id', inplace=True)                                # setting sample_id as index
dfcomb_sorted = df_comb.sort_values(['altitude'], ascending=True)           # sorting by altitude values (ascending)
dfc_sortd_alt = dfcomb_sorted.loc[:, ['Frac1', 'Frac2', 'Frac3']]           # storing in new df

avsq_plot = dfc_sortd_alt.plot.bar(stacked=True, 
                      figsize=(25,5), 
                      width=1, 
                      color=sb.color_palette("Paired", 3), 
                      fontsize='x-small', 
                      edgecolor='black', 
                      linewidth=0.5
                      )


# We can save this plot using the command below:
avsq_plot.figure.savefig(pfile, bbox_inches='tight')


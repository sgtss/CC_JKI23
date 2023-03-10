#!/usr/bin/env python

import os
import pandas as pd

# change working dir to CC3 and store in a variable for use later
os.chdir(os.path.normpath(os.path.join(os.path.dirname(__file__), '../')))
wrk_dir = os.getcwd()

# path to metadata file, Admixture Q file and plot file
mfile = f'{wrk_dir}{"/data/maize_samples.txt"}'                             # provided metadata file
qfile = f'{wrk_dir}{"/data/maize.3.Q"}'                                     # provided Admixture Q-output file
cfile = f'{wrk_dir}{"/data/maize.3.comb.txt"}'                              # combined file generated by script
rfile = f'{wrk_dir}{"/data/maize.3.Q.filt.txt"}'                            # sorted and filtered file (may be use for pophelper R script)
pfile = f'{wrk_dir}{"/results/maize.3.pdf"}'                                # plot in pdf format


# read files in pandas dataframes
df_meta = pd.read_csv(mfile, sep='\t')                                      # reading and storing metadat
df_Q = pd.read_csv(qfile, sep=' ', header=None)                             # reading and storing Q values

# set column headers (ancestory fractions as frac for K=3), concatanate both dataframes and filter for maize 
df_Q.columns = ["Frac{}".format(i) for i in range(1, df_Q.shape[1]+1)]      # looping through columns, increment by +1 and setting column name
df_comb = pd.concat([df_meta, df_Q], axis=1)                                # concatenating both dataframes, as both are same size; otherwise use merge
df_comb = df_comb[df_comb['species'] == 'Zea mays ssp. mays']               # filtering for maize samples only

# index by sample id, sort by altitude and save as new df
dfc_sorted = df_comb.sort_values(['altitude'], ascending=True)              # sorting by altitude values (ascending)
dfc_sorted.set_index('sample_id', inplace=True)                             # setting sample_id as index
dfc_sortd_alt = dfc_sorted.loc[:, ['Frac1', 'Frac2', 'Frac3']]              # extracting sample_id and fract in new df

# Save dataframes to csv files, which may be used with R in needed
dfc_sorted.to_csv(cfile, sep=" ", index=True, float_format='%.7f')          # saving sorted and combined (all data) file as csv 
dfc_sortd_alt.to_csv(rfile, sep=" ", index=True, float_format='%.7f')       # saving extracted data to new file as csv 

# Generate Plot with altitude sorted data frame for maize samples 
AvsQ_plot = dfc_sortd_alt.plot.bar(stacked=True, figsize=(24,4), width=1, fontsize='x-small', edgecolor='black', linewidth=1)
AvsQ_plot.set_title('Maize Ancestory Fractions (Q) estimates (for K=3) across sampling altitudes')
AvsQ_plot.set_ylabel('Q estimates')
AvsQ_plot.set_xlabel('Samples (Sorted by altitude, ascending left to right)')
AvsQ_plot.set_xticklabels(dfc_sortd_alt.index)
AvsQ_plot.spines[['top', 'left', 'right']].set_visible(False)

# Save plot as pdf
AvsQ_plot.figure.savefig(pfile, bbox_inches='tight')                        # saving plot as .pdf file


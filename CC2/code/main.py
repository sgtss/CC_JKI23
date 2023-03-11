#!/usr/bin/env python

import os, argparse, subprocess
import pandas as pd

# standard ftp link for information of NCBI REFSEQ assemblies
refseq_asmb_ftp = "ftp://ftp.ncbi.nlm.nih.gov/genomes/ASSEMBLY_REPORTS/assembly_summary_refseq.txt"

# change working dir to CC2 and store in a variable for use later
os.chdir(os.path.normpath(os.path.join(os.path.dirname(__file__), '../')))
wrk_dir = os.getcwd()

# set path to dirs for download and log file
# TODO: change to os.mkdir to avoid dir dont exist error
dnd_dir = f'{wrk_dir}{"/data/downloads/"}'                  # dir to download seq files
log_file = f'{wrk_dir}{"/data/log.txt"}'                    # file to log output of bash subprocess

refseq_asmb_sum = dnd_dir + 'assembly_summary_refseq.txt'   # path to local copy of NCBI assembly info file 

# Initializing default input parameters
mode = 'DWNLD'              # Script mode; DWNLD: download files from NCBI or LOCAL

loc_list = None             # Txt file containg list of path to fasta files 

ref_org_name = None         # Taxonomic name of reference organism to search
ref_asmb_id = None          # NCBI assembly name of reference organism; failsafe, more accurate
ref_asmb_ftp = None         # FTP link to NCBI assembly name of reference organism
ref_fasta_loc = None        # Path to fasta file for reference organism

sub_org_name = None         # Taxonomic name of subject organism to search
sub_asmb_id = None          # NCBI assembly name of subject organism; failsafe, more accurate
sub_asmb_ftp = None         # FTP link to NCBI assembly name of subject organism
sub_fasta_loc = None        # Path to fasta file for subject organism

seq_type = 'protein'        # sequence type; protein or mRNA
query_no = 100              # No. of query sequences to search

# read local copy of NCBI assembly info file and store in pandas dataframe
df_refseq = pd.read_csv(refseq_asmb_sum, sep='\t', skiprows=1, low_memory=False)    # skip top row; maybe close extra chrome tabs

'''
ref_org_name = "Nostoc flagelliforme CCNUN1"
ref_asmb_id = "ASM281357v1"
sub_org_name = "Nostoc punctiforme PCC 73102"
sub_asmb_id = "ASM2002v1"
'''
# find ftp link of the org
# gets col: organism_name or asm_name from get_data()
# similarly, gets qvalue: ref/sub_org_name or ref/sub_asmb_id from user input via get_data()
# sets trail for seq_type provided by user
# generates ftp link based on above inputs
def find_ftp_link(col, qvalue):

    # holds sequence trailing keyword to download from NCBI
    # sub folder structure on NCBI varies, however unique file exists with standard trail
    # better use wildcard search
    trail = '/*_protein.faa.gz'
    if seq_type == 'mrna': trail = '/*_cds_from_genomic.fna.gz'

    # find ftp_path for the organism from refsec assembly list 
    ref_asmb_ftp = ((((df_refseq.loc[       # select row from df_refseq where:
    (df_refseq[col] == qvalue)              # value in asm_name column matches to user assembly id of reference org
    ]).reset_index(drop=True)               # reset index of this row to 0 and discard old index values
    ).at[0,'ftp_path']                      # select value of ftp_path column in this row
    ).replace('https', 'ftp')               # replace https with ftp, to enable regex search
    ) + trail                               # evade possible subfolder issues

    print(ref_asmb_ftp)

# process user input to download seq data
def get_data(id, name, n):

    # create log file to store output
    with open(log_file,'w') as lf:

        # download NCBI REFSEC assemblies information file
        # runs everytime scripped is invoked to update to latest version of above
        # subprocess.run(["wget", "-P", dnd_dir, refseq_asmb_ftp], check=True, stdout=lf, text=True)
        
        # if download mode is reuqested
        if mode == 'DWNLD':

            if name: find_ftp_link('organism_name', name)   # find ftp link for ref/sub org name
            elif id: find_ftp_link('asm_name', id)          # find ftp link for ref/sub asmb id
            else: print('org name or asmb id not found')

            if n == 1: print('save as ref')                 # save as ref seq file
            elif n == 2: print('save as sub')               # save as sub seq file
            else: print('neither')

        # else if local mode is reuqested
        elif mode == 'LOCAL':
            print('local mode, check files')

        # Or if mode can not be established
        else:
            print('Houston, the problem just got bigger')


#subprocess.run(["wget", "-P", dnd_dir, ref_asmb_ftp], check=True, stdout=lf, text=True)


        return

# testing
ref_asmb_id = "ASM281357v1"
#ref_org_name = "Nostoc flagelliforme CCNUN1"
#sub_org_name = "Nostoc punctiforme PCC 73102"
sub_asmb_id = "ASM2002v1"

# 1 for ref and 2 for sub
# execute         
#get_data(ref_asmb_id, ref_org_name, 1)
get_data(sub_asmb_id, sub_org_name, 2)
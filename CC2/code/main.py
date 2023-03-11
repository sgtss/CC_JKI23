#!/usr/bin/env python

import os, argparse, subprocess
import pandas as pd

refseq_asmb_ftp = "ftp://ftp.ncbi.nlm.nih.gov/genomes/ASSEMBLY_REPORTS/assembly_summary_refseq.txt"

# change working dir to CC3 and store in a variable for use later
os.chdir(os.path.normpath(os.path.join(os.path.dirname(__file__), '../')))
wrk_dir = os.getcwd()
dnd_dir = f'{wrk_dir}{"/data/downloads/"}' 
log_file = f'{wrk_dir}{"/data/log.txt"}'

refseq_asmb_sum = dnd_dir + 'assembly_summary_refseq.txt'

# Initializing default input parameters
mode = 'DWNLD'              # Script mode; DWNLD: download files from NCBI or LOCAL

dnd_list = None             # Txt file containg list of fasta files to download 
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



df_refseq = pd.read_csv(refseq_asmb_sum, sep='\t', skiprows=1, low_memory=False)
#print(df_refseq)

ref_org_name = "Nostoc flagelliforme CCNUN1"
ref_asmb_id = "ASM281357v1"
ref_org_name = "Nostoc punctiforme PCC 73102"
ref_asmb_id = "ASM2002v1"

# find ftp_path for the organism from refsec assembly list 
ref_asmb_ftp = ((((df_refseq.loc[                        # select row from df_refseq where:
    (df_refseq['organism_name'] == ref_org_name) &      # value in organism_name column matches to user reference org AND
    (df_refseq['asm_name'] == ref_asmb_id)              # value in asm_name column matches to user assembly id of reference org
    ]).reset_index(drop=True)   	                    # reset index of this row to 0 and discard old index values
    ).at[0,'ftp_path']                                  # select value of ftp_path column in this row
    ).replace('https', 'ftp')
    ) + '/*_' + seq_type + '.faa.gz'


# replace https with ftp



#_protein.faa.gz
#_cds_from_genomic.fna.gz
#wget ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/215/GCF_000001215.4_Release_6_plus_ISO1_MT/*protein.faa.gz

#wget -P dnd_dir refseq_asmb_ftp
#ftp://ftp.ncbi.nlm.nih.gov/genomes/ASSEMBLY_REPORTS/assembly_summary_refseq.txt
#refseq_asmb_sum = dnd_dir + 'assembly_summary_refseq.txt'

print(ref_asmb_ftp)
#print(ref_asmb_ftp)


def get_data():

    # create log file to store output
    with open(log_file,'w') as lf:

        # call mmseqs easy-rbh function (via subprocess) and pass search args
        #subprocess.run(["wget", "-P", dnd_dir, refseq_asmb_ftp], check=True, stdout=lf, text=True)
        #subprocess.run(["wget", "-P", dnd_dir, ref_asmb_ftp], check=True, stdout=lf, text=True)




        return

# execute         
get_data()
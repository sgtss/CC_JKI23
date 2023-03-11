#!/usr/bin/env python

import os, argparse, subprocess
import pandas as pd

# standard ftp link for information of NCBI REFSEQ assemblies
refseq_asmb_info_ftp = "ftp://ftp.ncbi.nlm.nih.gov/genomes/ASSEMBLY_REPORTS/assembly_summary_refseq.txt"

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

loc_list = 'none'           # Txt file containg list of path to fasta files 

ref_org_name = 'none'       # Taxonomic name of reference organism to search
ref_asmb_id = 'none'        # NCBI assembly name of reference organism; failsafe, more accurate
ref_fasta_loc = 'none'      # Path to fasta file for reference organism

sub_org_name = 'none'       # Taxonomic name of subject organism to search
sub_asmb_id = 'none'        # NCBI assembly name of subject organism; failsafe, more accurate
sub_fasta_loc = 'none'      # Path to fasta file for subject organism

seq_type = 'protein'        # sequence type; protein or mRNA
query_no = 100              # No. of query sequences to search

# temp variable storing path of the file downloaded by wget
dnd_file_path = 'none'
refseq_ftp = 'none'       # FTP link to NCBI assembly

ref_org_name = "Nostoc flagelliforme CCNUN1"
ref_asmb_id = "ASM281357v1"
sub_org_name = "Nostoc punctiforme PCC 73102"
sub_asmb_id = "ASM2002v1"

# find ftp link of the org
# gets col: organism_name or asm_name from get_data()
# similarly, gets qvalue: ref/sub_org_name or ref/sub_asmb_id from user input via get_data()
# sets trail for seq_type provided by user
# generates ftp link based on above inputs
def find_ftp_link(col, qvalue):

    global refseq_ftp           # TODO not the optimal way; DEBUG
    # read local copy of NCBI assembly info file and store in pandas dataframe
    df_refseq = pd.read_csv(refseq_asmb_sum, sep='\t', skiprows=1, low_memory=False)    # skip top row; maybe close extra chrome tabs

    # holds sequence trailing keyword to download from NCBI
    # sub folder structure on NCBI varies, however unique file exists with standard trail
    # better use wildcard search
    trail = '/*_protein.faa.gz'
    if seq_type == 'mrna': trail = '/*_cds_from_genomic.fna.gz'

    # find ftp_path for the organism from refsec assembly list 
    refseq_ftp = ((((df_refseq.loc[       # select row from df_refseq where:
    (df_refseq[col] == qvalue)              # value in asm_name column matches to user assembly id of reference org
    ]).reset_index(drop=True)               # reset index of this row to 0 and discard old index values
    ).at[0,'ftp_path']                      # select value of ftp_path column in this row
    ).replace('https', 'ftp')               # replace https with ftp, to enable regex search
    ) + trail                               # evade possible subfolder issues

    return()

# run wget as subprocess and download files
# requires dnd_dir as path to download dir
# required ftp_path as NCBI path to file
# requires rw as file rewite flag
def dnd_files(tgt_dir, ftp_path, orw):

    global dnd_file_path

    # create log file to store output
    with open(log_file,'r+') as lf:

        # clear file content if rerun
        lf.truncate(0)

        if orw:

            flag = '-N'

            print('orw is on')
            
            # download NCBI REFSEC assemblies information file
            # runs everytime scripped is invoked to update to latest version of above
            # file is overwritten every time
            subprocess.run(['wget',                         # call wget as subprecess
                            flag,                            # overwrite
                            '-nv',                          # switch wget output to non-verbose
                            '--dont-remove-listing',        # keep ftp folder listing
                            '-P',                           # save in specified folder
                            tgt_dir,                        # path to download dir
                            ftp_path],                      # NCBI ftp path
                            check=True,                     # raise error if command fails
                            stderr=lf,                      # recored stderr to log file (wget uses stderr for stdout)
                            stdout=lf,                      # record anything in stdout from subprocess
                            text=True)                      # record as text and not binary
            
        else:
            print('orw is off')

            #downloading fasta files, not overwrting as need it for fire path
            subprocess.run(['wget', '-nv', '--dont-remove-listing', '-P', tgt_dir, ftp_path], check=True, stderr=lf, stdout=lf, text=True) 
            
        # this is a hack to get downloaded file location
        # there are better solutions, but ftp mode does not support them
        # go to top of log file, 
        # find 2nd line in wget output
        # extract path between ""
        # and save as downloaded file path
        lf.seek(0) 
        Lines = lf.readlines()
        if len(Lines) == 2: dnd_file_path = str(((Lines[1]).split('"')[1::2])[0])
        elif len(Lines) == 1: print('NCBI REFSEQ assembly info file is updated')
        else: print('wget failed for some reason')
        lf.close()

# process user input to download seq data
def get_data(id, name, n):

        global ref_fasta_loc, sub_fasta_loc    
        
        # if download mode is reuqested
        if mode == 'DWNLD':

            print('Download mode is selected')              # user prompt

            # set overwrite flag for wget
            owrm = True
            ftp_link_found = False

            print('Downloading NCBI REFSEQ assembly info file')              # user prompt
            
            # download NCBI REFSEQ assembly info file
            dnd_files(dnd_dir, refseq_asmb_info_ftp, owrm)

            print('Searching for ftp links in NCBI REFSEQ assembly info file')              # user prompt
            # generate ftp links based on user input
            if name: find_ftp_link('organism_name', name)   # find ftp link for ref/sub org name
            elif id: find_ftp_link('asm_name', id)          # find ftp link for ref/sub asmb id
            else: print('org name or asmb id not found')

            print('refseq search', refseq_ftp)
            print('downloaded file', dnd_file_path)
            #print(refseq_ftp)

            # differentiate as REF or SUBJ and download fasta files
            if refseq_ftp != 'none':
                
                #set overwrite to false
                owrm = False
                
                # if downloading ref fasta file
                if n == 1: 
                    print('saving as ref')                 # save as ref seq file
                    # download NCBI REFSEQ assembly info file
                    dnd_files(dnd_dir, refseq_ftp, owrm)
                    ref_fasta_loc = dnd_file_path
                    print('REF:', ref_fasta_loc)

                elif n == 2: 
                    print('saving as sub')               # save as sub seq file
                    # download NCBI REFSEQ assembly info file
                    dnd_files(dnd_dir, refseq_ftp, owrm)
                    sub_fasta_loc = dnd_file_path
                    print('SUB:', sub_fasta_loc)

                else: print('neither')
            else: print('Ftp path not found')

        # else if local mode is reuqested
        elif mode == 'LOCAL':
            print('local mode, check files')

        # Or if mode can not be established
        else:
            print('Houston, the problem just got bigger')

        return

# execute         
get_data(ref_asmb_id, ref_org_name, 1)
get_data(sub_asmb_id, sub_org_name, 2)



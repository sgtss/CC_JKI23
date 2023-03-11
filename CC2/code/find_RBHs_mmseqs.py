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

mmseqs_log_file = f'{wrk_dir}{"/data/mmseqs_log.txt"}'      # file to log output of bash mmseqs subprocess
qry_file = f'{wrk_dir}{"/data/Ex100_sub.faa"}'
rbh_list = f'{wrk_dir}{"/results/Ex100_RBHs.tsv"}'
tmp_fldr = f'{wrk_dir}{"/tmp"}'

refseq_asmb_sum = dnd_dir + 'assembly_summary_refseq.txt'   # path to local copy of NCBI assembly info file 

# Initializing default input parameters
mode = 'DWNLD'              # Script mode; DWNLD: download files from NCBI or LOCAL

#loc_list = 'none'           # Txt file containg list of path to fasta files 

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

#ref_org_name = "Nostoc flagelliforme CCNUN1"
#ref_asmb_id = "ASM281357v1"
#sub_org_name = "Nostoc punctiforme PCC 73102"
#sub_asmb_id = "ASM2002v1"

# Stores text for instructions
INFO_REF = '[REQUIRED] Name of reference organism, for eg. "Nostoc flagelliforme CCNUN1"'
INFO_REF_AN = '[REQUIRED] NCBI Assembly ID of reference organism assembly, for eg. ASM281357v1'
INFO_SUB = '[REQUIRED] Name of subject organism, for eg. "Nostoc punctiforme PCC 73102"'
INFO_SUB_AN = '[REQUIRED] NCBI Assembly ID of reference organism assembly, for eg. ASM2002v1'
INFO_TYP = '[REQUIRED] Sequence type, for eg. Protein or mRNA'
INFO_QNS = 'Number of sequences to search, for eg. 100'
INFO_REF_FL = '[REQUIRED] path to sequences file of reference organism, for eg. /path/to/ref.fasta'
INFO_SUB_FL = '[REQUIRED] path to sequences file of subject organism, for eg. /path/to/subj.fasta'

# parse user provided args
def getArgs():

    # TODO not the optimal way; DEBUG REQUIRED, instantiate class
    global ref_org_name, ref_asmb_id, ref_fasta_loc, sub_org_name, sub_asmb_id, sub_fasta_loc, seq_type, query_no

    # Parse arguments and validate
    parser = argparse.ArgumentParser(description='Find RBHs.')
    parser.add_argument('-t', metavar='SEQ_TYPE', choices=['protein','mrna'], type=str.lower, help=INFO_TYP)
    parser.add_argument('-q', metavar='NUM_QUERY_SEQ', type=int, help=INFO_QNS)    
    
    # args for download mode
    modeD = parser.add_argument_group('Download', 'Download sequences from NCBI REFSEQ')
    modeD.add_argument('-r', metavar='REFERENCE_ORG', type=str, help=INFO_REF)
    modeD.add_argument('-rn', metavar='REF_ASMB_NAME', type=str, help=INFO_REF_AN)    
    modeD.add_argument('-s', metavar='SUBJECT_ORG', type=str, help=INFO_SUB)
    modeD.add_argument('-sn', metavar='SUB_ASMB_NAME', type=str, help=INFO_SUB_AN)
    
    # args for local mode
    modeL = parser.add_argument_group('Local', 'Use pre-Download sequences files')
    modeL.add_argument('-rf', metavar='REF_FILE', type=argparse.FileType('r', encoding='utf-8'), help=INFO_REF_FL)
    modeL.add_argument('-sf', metavar='SUB_FILE', type=argparse.FileType('r', encoding='utf-8'), help=INFO_REF_FL)
    
    return parser.parse_args()

args = getArgs()
print(args)

# assigning args to vars
ref_org_name = args.r
ref_asmb_id = args.rn
ref_fasta_loc = args.rf
sub_org_name = args.s
sub_asmb_id = args.sn
sub_fasta_loc = args.sf
seq_type = args.t
query_no = args.q

#print('after assignment', ref_org_name, ref_asmb_id, ref_fasta_loc, sub_org_name, sub_asmb_id, sub_fasta_loc, seq_type, query_no)


# find ftp link of the org
# gets col: organism_name or asm_name from get_data()
# similarly, gets qvalue: ref/sub_org_name or ref/sub_asmb_id from user input via get_data()
# sets trail for seq_type provided by user
# generates ftp link based on above inputs
def find_ftp_link(col, qvalue):

    global refseq_ftp           # TODO not the optimal way; DEBUG REQUIRED
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
def download_files_NCBI(tgt_dir, ftp_path):

    global dnd_file_path                # TODO not the optimal way; DEBUG REQUIRED

    # create log file to store output
    with open(log_file,'r+') as lf:

        # clear file content if rerun
        lf.truncate(0)
        
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

# this function unpacks and updates file paths for REF and SUB files
def process_downloaded_files(file_path):

    global ref_fasta_loc, sub_fasta_loc

    #downloading fasta files, not overwrting as need it for fire path
    subprocess.run(['gunzip', '-k', file_path], check=True)

# process user input to download seq data
def get_data(id, name, n):

        global ref_fasta_loc, sub_fasta_loc                 # TODO not the optimal way; DEBUG REQUIRED
        
        # if download mode is reuqested
        if mode == 'DWNLD':

            print('Searching for ftp links in NCBI REFSEQ assembly info file')              # user prompt
            # generate ftp links based on user input
            if name: find_ftp_link('organism_name', name)   # find ftp link for ref/sub org name
            elif id: find_ftp_link('asm_name', id)          # find ftp link for ref/sub asmb id
            else: print('Error: org name or asmb id not found')             # user prompt

            print('REFSEQ Search:', refseq_ftp)
            #print('Downloaded file', dnd_file_path)
            #print(refseq_ftp)

            # differentiate as REF or SUBJ and download fasta files
            if refseq_ftp != 'none':
                
                # if downloading ref fasta file
                if n == 1: 
                    #print('Saving as ref')                 # save as ref seq file
                    # download NCBI REFSEQ assembly info file
                    download_files_NCBI(dnd_dir, refseq_ftp)
                    process_downloaded_files(dnd_file_path)
                    ref_fasta_loc = dnd_file_path[:-3]
                    print('Succesfully downloaded REF fasta file :', ref_fasta_loc)

                elif n == 2: 
                    #print('saving as sub')                 # save as sub seq file
                    # download NCBI REFSEQ assembly info file
                    download_files_NCBI(dnd_dir, refseq_ftp)
                    process_downloaded_files(dnd_file_path)
                    sub_fasta_loc = dnd_file_path[:-3]
                    print('Succesfully downloaded SUB fasta file :', sub_fasta_loc)

                else: print('neither')
            else: print('Ftp path not found')

        # else if local mode is reuqested
        elif mode == 'LOCAL':
            print('local mode, check files')

        # Or if mode can not be established
        else:
            print('Houston, the problem just got bigger')

        return
    
# find RBHs using mmseqs2
def run_mmseqs_easy():

    # create log file to store output
    with open(mmseqs_log_file,'w') as mlf:

        # call mmseqs easy-rbh function (via subprocess) and pass search args
        subprocess.run(["mmseqs", "easy-rbh", ref_fasta_loc, qry_file, rbh_list, tmp_fldr],
                    check=True, stdout=mlf, text=True)
        mlf.close()
# execute         
#run_mmseqs_easy()

# clean download dir
def housekeeping():

    if not os.listdir(dnd_dir):
        print("Download Dir is empty")
    else:    
        print("cleaning Download Dir")
        for f in os.listdir(dnd_dir):
            os.remove(os.path.join(dnd_dir, f))
    return
housekeeping()

# download NCBI REFSEQ assembly info file
print('Downloading NCBI REFSEQ assembly info file')              # user prompt
download_files_NCBI(dnd_dir, refseq_asmb_info_ftp)

if ref_org_name != 'none' or ref_asmb_id != 'none' :
    get_data(ref_asmb_id, ref_org_name, 1)
if sub_org_name != 'none' or sub_asmb_id != 'none': 
    get_data(sub_asmb_id, sub_org_name, 2)
else:
    print('Please provide REF and SUB info')




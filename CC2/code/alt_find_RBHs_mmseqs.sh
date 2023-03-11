#!/bin/bash -l
<< 'BC1'

##############################################################################

Author:          Shrikant Sharma
Last updated:    03/06/2023
License:         Free to use, modify etc 

###############################################################################

#! MMseqs2 is expected to be installed on your system. if not, please follow the following GitHub link to see installation instructions..
https://github.com/soedinglab/MMseqs2
https://github.com/soedinglab/MMseqs2/wiki#reciprocal-best-hit-using-mmseqs-rbh 

This bash script identifies Reciprocal Blast Hits (RBHs) using MMseqs2 program.

### USAGE: This script requires XXX arguments. 

ARG1: Path of file containg list of links to download sequence files (can be AA or mRNA and not both) in fasta format.

ARG2: Path to .fasta file of Reference organism, for eg. 
/home/user/folder/reference.fasta 

ARG3: Path to .fasta file of Subject organism, for eg. same as above  

###############################################################################
BC1

set -e
#set -x

# Basic VARs

TIMESTAMP="$(date)"                             # Store current date and time in VARIABLE
CURRENT_DIR="$(pwd)"                            # Store current dir in VARIABLE
#BASE=$HOME                                      # Store PATH in VARIABLE [$HOME],

#printf "$TIMESTAMP | Current Dir : $CURRENT_DIR \n"
#printf "$BASE"

BASE_DIR="CC_JKI23/CC2"
#WORK_DIR="alt_mmseqs"
DATA_DIR="data/mmseqs_data"
RESULTS_DIR="results"
TMP_DIR="tmp"

DOWN_FILE="download_list.txt"
MODE="protien"              # can be protein or mRNA
NSEQS=100                   # number of extracted query sequences to search

REF_FILE="REF_Nostoc_flagelliforme_CCNUN1.faa"
SUBJT_FILE="SUBJ_Nostoc_punctiforme_PCC_73102.faa"
QUERY_FILE="Ex100_SUBJ_Nostoc_punctiforme_PCC_73102.faa"

mkdir -p $BASE_DIR/$DATA_DIR
mkdir -p $BASE_DIR/$DATA_DIR/$TMP_DIR

cd $BASE_DIR

wget -P $DATA_DIR/$TMP_DIR/ -i $DATA_DIR/download_list.txt

# pick first n seqs from file
awk "/^>/ {n++} n>$NSEQS {exit} {print}" $DATA_DIR/$SUBJT_FILE > $DATA_DIR/$QUERY_FILE

# mmseqs2 easy-rbh
# mmseqs easy-rbh Aproteins.fasta Bproteins.fasta ABrbh tmp
mmseqs easy-rbh $DATA_DIR/$REF_FILE $DATA_DIR/$QUERY_FILE $DATA_DIR/Ex100_Rbh.tsv $DATA_DIR/tmp
mmseqs easy-rbh $DATA_DIR/$REF_FILE $DATA_DIR/$SUBJT_FILE $DATA_DIR/All_Rbh.tsv $DATA_DIR/tmp
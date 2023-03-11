#!/usr/bin/env python

import os
import pandas as pd

refseq_asmb_sum = "/home/s2/PlayGround/GitHub_Base/CC_JKI23/CC2/data/assembly_summary_refseq.txt"

df_refseq = pd.read_csv(refseq_asmb_sum, sep='\t', skiprows=1, low_memory=False)
print(df_refseq)

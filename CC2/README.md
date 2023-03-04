# **Challenge Two - Applied bioinformatics**

A defining analysis in bioinformatics is searching for similar sequences for a set of query nucleotide or amino acid sequences e.g. using Blast . Reciprocal Best Hits (RBH) are a common proxy for orthology in comparative genomics (see this article ). Essentially, a RBH is found when the proteins encoded by two genes, each in a different genome, find each other as the best scoring match in the other genome. NCBI's BLAST is the software most usually used for the sequence comparisons necessary to find RBHs.

**TASK ONE:** 
Download any two Nostoc bacterial genomes from NCBI , use one complete genome (the “reference”) and of the other only a small fraction e.g. one hundred genes (the “subject”).

**TASK TWO:** 
Write a simple pipeline that identifies the RBH for the “subject” genes. You can use Blast , Blat , Diamond or any other sequence similarity search tool .

**NOTES:**
You will receive extra points if you use shell commands like cut , sort , awk , and comm to identify the RBH from the results of the sequence similarity searches.
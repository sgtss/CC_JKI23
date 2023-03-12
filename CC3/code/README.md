This folder contains coding files/scripts for CC3.

*USAGE: python code/plotQ.py*

The script takes 2 input files, 

/data/maize_samples.txt :   provided metadata file
/data/maize.3.Q :           provided admixture q estimates file

> imports into pandas dataframes
> concatanates, filters for maize samples, sorts by altitude and save as new files (can be used with R scripts)
> generates stacked plot: x=alitude, y= Q fractions; and saves as pdf

Output files:

/data/maize.3.Q.filt.txt :  filtered and sorted maize Q file with sample_ids as index
/data/maize.3.comb :        filtered and sorted file with all data, can be used for geoploting

/results/maize.3pdf :       plot file
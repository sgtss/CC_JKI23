# **Challenge Three - Data visualization and interpretation**

Genetic diversity within species is often structured geographically, reflecting both current ecological and historical drivers of genetic differentiation. Thus population structure, and admixture among populations, should be accounted for when searching for functional diversity within species.

**Provided data:** 
In this link you can find the Q-output and sample metadata of an Admixture (a popular software to infer population structure) analysis, performed on maize and teosinte samples. In the table stored in file “ maize.3.Q ”, each row represents a sample, in the same order as in the also provided “ maize_samples.txt ” metadata file.

**TASK ONE:** 
Considering only the maize samples, plot the Q estimates and the altitude at which each sample was collected. You can make the plot and order the samples however you deem appropriate.

COMPLETED

Please see code, data and results folder.

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

**TASK TWO:**
Besides the code and plot, provide a short biological interpretation (max 50 words) of the admixture analysis and plotted results.

The samples appear to follow the trend based on altitude. Altitude based admixture analysis (for K=3) somewhat seperates samples, with fraction 1 being predominant in lower altitudes wereas, fraction 3 is dominated in higher altitude samples, with some outliers. There can be 2 origins, Frac 1 and 3, whereas frac 2 seems to signify crossover. 
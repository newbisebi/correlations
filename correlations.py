"""
Python3
Sébastien Mariaux - July 2018

Create a correlation table with p-values
"""
import itertools
import pandas as pd
from pandas import DataFrame
import numpy as np
import scipy
from scipy import stats

def create_empty_table(variables_list):
    """Set the correlation table to be filled 
    Columns and row indexes are based on variables names
    """
    tuples = [(var, stat)  for var in variables_list for stat in ['corr', 'p']]
    index = pd.MultiIndex.from_tuples(tuples, names=['Variable', 'Stat'])
    df = pd.DataFrame(index=index, columns=variables_list).fillna('-')
    return df

def compute_pearson(x, y):
    """
    Compute the pearson correlation and the p-value between x and y;
    returns corr and p as strings with adequate formating
    """
    corr, p = scipy.stats.pearsonr(x, y)
    if p < 0.001:
        corr = "%.3f***"%corr
    elif p < 0.005:
        corr = "%.3f**"%corr
    elif p < 0.01:
        corr = "%.3f*"%corr
    else:
        corr = "%.3f"%corr
    p = "(%.3f)"%p
    return corr, p


def make_table(df, variables, both_side=True, export=False, export_name='correlations'):
    corr_table = create_empty_table(variables)
    
    #Values on the diagonal : corr = 1 and p = 0
    for x in variables:
        corr_table.loc[(x, 'corr'), x] = "1.000***"
        corr_table.loc[(x, 'p'), x] = "(0.000)"
    
    for (x, y) in itertools.combinations(variables, 2):
        corr, p = compute_pearson(df[x], df[y])
        corr_table.loc[(y, 'corr'), x] = corr
        corr_table.loc[(y, 'p'), x] = p
        if both_side:
            corr_table.loc[(x, 'corr'), y] = corr
            corr_table.loc[(x, 'p'), y] = p
            
    #Export to Excel
    if export :
        out = "{}.xlsx".format(export_name)
        corr_table.to_excel(out)
        
    return corr_table



if __name__ == '__main__':

    #Random data
    means = 10, 20, 15, 32
    stdevs = 4, 2, 8, 5

    df = pd.DataFrame(
        np.random.normal(loc=means, scale=stdevs, size=(50, 4)),
        columns=['a', 'b', 'c', 'd'])

    #Correlations
    df = make_table(df, df.columns.values, both_side=False, export=True, export_name='correlations')
    print(df)

import pandas as pd
import numpy as np
from scipy import stats

def windowed_cross_correlation(df, col1, col2, window_size,winc=2,lag=1):
    """
    Perform windowed cross-correlation between two columns of a DataFrame.

    Parameters:
    - df: pandas DataFrame
    - col1: str, the name of the first column
    - col2: str, the name of the second column
    - window_size: int, size of the window for the cross-correlation

    Returns:
    - result_df: pandas DataFrame with windowed cross-correlation values
    """
    # Ensure the specified columns exist in the DataFrame
    if col1 not in df.columns or col2 not in df.columns:
        raise ValueError("Specified columns not found in the DataFrame")
    # Calculate cross-correlation for each window
    cross_correlation_values = []
    index=0
    combinations=lag*2+1
    dict={}
    for columns in [n for n in range(-lag,lag+1,1)]:
        dict[columns]=[]
    for index_inc in range(0,df.shape[0],winc):
        start_one=winc+index_inc
        for i in range(-lag,lag+1,1):
            if start_one+window_size<=df.shape[0]:
                if i<=0:
                    window1 = df[col1].iloc[start_one:start_one+window_size].values
                    window2 = df[col2].iloc[start_one+i:start_one+i+window_size].values
                    cross_corr=stats.pearsonr(window1, window2)
                    dict[i].append(cross_corr[0])
                else:
                    window1 = df[col1].iloc[start_one-i:start_one+window_size-i].values
                    window2 = df[col2].iloc[start_one:start_one+window_size].values
                    #print(index_inc,len(window1),len(window2))
                    cross_corr=stats.pearsonr(window1, window2)
                    dict[i].append(cross_corr[0])
            else:
                print("-")
    result_df = pd.DataFrame(dict)

    return result_df

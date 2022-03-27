#!/usr/bin/python3
import pandas as pd
import numpy as np

def remove_outlier(df_in, col_name):
    q1 = df_in[col_name].quantile(0.25)
    q3 = df_in[col_name].quantile(0.75)
    iqr = q3-q1 #Interquartile range
    fence_low  = q1-1.5*iqr
    fence_high = q3+1.5*iqr
    df_out = df_in.loc[(df_in[col_name] > fence_low) & (df_in[col_name] < fence_high)]
    return df_out


def main():
    df = pd.DataFrame({'Data':np.random.normal(size=200)})
    df_filtered = remove_outlier(df,'Data')
    df.to_csv('df.csv',encoding='utf8')
    df_filtered.to_csv('df_filtered.csv',encoding='utf8')

def alternative(df, q=0.05):
    upper = df.quantile(1-q)
    lower = df.quantile(q)
    mask = (df < upper) & (df > lower)
    return mask

def drop_outliers(df, field_name):
    distance = 1.5 * (np.percentile(df[field_name], 75) - np.percentile(df[field_name], 25))
    df.drop(df[df[field_name] > distance + np.percentile(df[field_name], 75)].index, inplace=True)
    df.drop(df[df[field_name] < np.percentile(df[field_name], 25) - distance].index, inplace=True)
    print(df)
#t = pd.DataFrame({'train': [1,1,2,3,4,5,6,7,8,9,9],
#                  'y': [1,0,0,1,1,0,0,1,1,1,0]})
#### This works
np.random.seed([3, 1415])
df = pd.DataFrame(
    np.random.normal(size=(20, 8)),
    columns=list('ABCDEFGH')
)


print(df.mask((df - df.mean()).abs() > 2 * df.std()))
print(df.mask((df - df.mean()).abs() > 2 * df.std()).dropna())
df_filtered = df.mask((df - df.mean()).abs() > 2 * df.std()).dropna()

#### end of working part
#mask = alternative(t['train'], 0.1)
#print(t)
#print(t[mask])

#drop_outliers(t, 'train')
#main()

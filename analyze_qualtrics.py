import pandas as pd
import pingouin as pg
from typing import Dict, List


# read all Qualtrics data
df = pd.read_csv('data.csv')

# remove unncessary rows
df = df[df['Status'] != 'Survey Preview'].copy()
df = df.drop(index=0)  # remove 2nd row
df = df.drop(index=1)  # remove 3rd row

# replace strings with numbers
for i in range(1, 8):
    df = df.replace('^[A-Za-z\s]*{}$'.format(i), i, regex=True)
df = df.applymap(lambda x: pd.to_numeric(x, errors='ignore'))

# compare initial vs. final impressions
impression_data: Dict[str, List] = {
    'pid': [],
    'IV': [],
    'DV': [],
}

for index, row in df.iterrows():
    impression_data['pid'].extend([row['ResponseId'], row['ResponseId']])
    impression_data['IV'].extend(['before', 'after'])
    impression_data['DV'].extend([row['Q28'], row['Q29']])

impression_df = pd.DataFrame(impression_data)
description = impression_df['DV'].mean()
print(description)
result = pg.pairwise_tests(data=impression_df, dv='DV', within='IV', subject='pid')
print(result)

print(df)
import pandas as pd
import pingouin as pg
import matplotlib.pyplot as plt
from typing import Dict, List
import argparse

# Create the parser
parser = argparse.ArgumentParser(description='What to visualize')

# Add the flags
parser.add_argument('-e', '--errorbars', action='store_true', help='Enable error bars.')
parser.add_argument('-p', '--pvalues', action='store_true', help='Show p values.')

# Parse the arguments
args = parser.parse_args()

# read all Qualtrics data
df = pd.read_csv('data.csv')

# remove unncessary rows
df = df[df['Status'] != 'Survey Preview'].copy()
df = df.drop(index=0)  # remove 2nd row
df = df.drop(index=1)  # remove 3rd row

# replace strings with numbers
for i in range(1, 8):
    df = df.replace(r'^[A-Za-z\s]*{}$'.format(i), i, regex=True)
df = df.map(lambda x: pd.to_numeric(x, errors='ignore'))

# calculate number of subjects
n: int = len(df)

def format_df_for_pg(raw_df: pd.DataFrame, comparison1: str, comparison2: str):

    # compare initial vs. final impressions
    data: Dict[str, List] = {
        'pid': [],
        'IV': [],
        'DV': [],
    }

    for index, row in df.iterrows():
        data['pid'].extend([row['ResponseId'], row['ResponseId']])
        data['IV'].extend(['1', '2'])
        data['DV'].extend([row[comparison1], row[comparison2]])

    new_df = pd.DataFrame(data)
    means = [
        new_df[new_df['IV'] != '1']['DV'].mean(),
        new_df[new_df['IV'] != '2']['DV'].mean()
    ]
    stderr = [
        new_df[new_df['IV'] != '1']['DV'].std()/n,
        new_df[new_df['IV'] != '2']['DV'].std()/n
    ]
    return new_df, means, stderr

prepost_df, prepost_means, prepost_stderr = format_df_for_pg(df, 'Q28', 'Q29')
prepost_result = pg.pairwise_tests(data=prepost_df, dv='DV', within='IV', subject='pid')

# compare usability and confidence
# SUS GPT-4o mini
SUS_gpt_cols = ['1_Q17', '1_Q18', '1_Q19', '1_Q20', '1_Q21', '1_Q22', '1_Q23', '1_Q24', '1_Q25', '1_Q26']
SUS_mpa_cols = ['2_Q17', '2_Q18', '2_Q19', '2_Q20', '2_Q21', '2_Q22', '2_Q23', '2_Q24', '2_Q25', '2_Q26']
rosas_gpt_cols = ['1_Q8', '1_Q12', '1_Q13', '1_Q14', '1_Q15', '1_Q16']
rosas_mpa_cols = ['2_Q8', '2_Q12', '2_Q13', '2_Q14', '2_Q15', '2_Q16']
df['ave_sus_gpt'] = df[SUS_gpt_cols].mean(axis=1)
df['ave_sus_mpa'] = df[SUS_mpa_cols].mean(axis=1)
df['ave_rosas_gpt'] = df[rosas_gpt_cols].mean(axis=1)
df['ave_rosas_mpa'] = df[rosas_mpa_cols].mean(axis=1)
SUS_df, SUS_means, SUS_stderr = format_df_for_pg(df, 'ave_sus_gpt', 'ave_sus_mpa')
SUS_result = pg.pairwise_tests(data=SUS_df, dv='DV', within='IV', subject='pid')
rosas_df, rosas_means, rosas_stderr = format_df_for_pg(df, 'ave_rosas_gpt', 'ave_rosas_mpa')
rosas_result = pg.pairwise_tests(data=rosas_df, dv='DV', within='IV', subject='pid')

# graph everything
fig, axs = plt.subplots(1, 3, figsize=(12, 4))
if args.errorbars:
    axs[0].bar(['before study', 'after study'], prepost_means, yerr=prepost_stderr, color=["#64dfe4", "#157f92"])
    axs[1].bar(['GPT-4o mini', 'MyPatriotAI'], SUS_means, yerr=SUS_stderr, color=["#e67f2b", "#ee5252"])
    axs[2].bar(['GPT-4o mini', 'MyPatriotAI'], rosas_means, yerr=rosas_stderr, color=["#e67f2b", "#ee5252"])
else:
    axs[0].bar(['before study', 'after study'], prepost_means, color=["#64dfe4", "#157f92"])
    axs[1].bar(['GPT-4o mini', 'MyPatriotAI'], SUS_means, color=["#e67f2b", "#ee5252"])
    axs[2].bar(['GPT-4o mini', 'MyPatriotAI'], rosas_means, color=["#e67f2b", "#ee5252"])

axs[0].set_title('Likely to Choose MyPatriotAI')
axs[0].set_ylabel('score')

axs[1].set_title('System Usability')
axs[1].set_ylabel('score')

axs[2].set_title('Competence')
axs[2].set_ylabel('score')

if args.pvalues:
    axs[0].text(0, -1, 'p={}'.format(prepost_result['p-unc'].iloc[0]), fontsize=12, color='red')
    axs[1].text(0, -1, 'p={}'.format(SUS_result['p-unc'].iloc[0]), fontsize=12, color='red')
    axs[2].text(0, -1, 'p={}'.format(rosas_result['p-unc'].iloc[0]), fontsize=12, color='red')

plt.tight_layout()
plt.show()

print(df)
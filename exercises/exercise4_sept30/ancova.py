import pandas as pd
import pingouin as pg

# Load CSV (assumed to be in same directory)
df = pd.read_csv("ancova.csv")

# Assume columns: one numeric DV column ("value") and one categorical grouping column ("group")
aov = pg.ancova(dv="Perceived Intelligence", between="Planner", covar="Age", data=df)
print("=== One-way ANOVA ===")
print(aov)

# Pairwise comparisons controlling for Age (covariate)
posthoc = pg.pairwise_tukey(
    data=df,
    dv='Perceived Intelligence',
    between='Planner'
)

print(posthoc)
import pandas as pd
import pingouin as pg

# Load CSV (assumed to be in same directory)
df = pd.read_csv("anova.csv")

# Assume columns: one numeric DV column ("value") and one categorical grouping column ("group")
aov = pg.anova(dv="Perceived Intelligence", between="Planner", data=df, detailed=True)
print("=== One-way ANOVA ===")
print(aov)

# Tukey HSD posthoc
tukey = pg.pairwise_tukey(dv="Perceived Intelligence", between="Planner", data=df)
print("\n=== Tukey HSD ===")
print(tukey)
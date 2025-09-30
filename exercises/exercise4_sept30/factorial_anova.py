import pandas as pd
import pingouin as pg

# Load CSV (assumed to be in same directory)
df = pd.read_csv("factorial_anova.csv")

# Factorial ANOVA
aov = pg.anova(dv="Perceived Intelligence", between=["Planner", "Task"], data=df, detailed=True)
print("=== Factorial ANOVA ===")
print(aov)

# Tukey HSD posthoc (for both factors)
tukey = pg.pairwise_tukey(dv="Perceived Intelligence", between="Planner", data=df)
print("\n=== Tukey HSD for Planner ===")
print(tukey)

tukey_task = pg.pairwise_tukey(dv="Perceived Intelligence", between="Task", data=df)
print("\n=== Tukey HSD for Task ===")
print(tukey_task)
import pandas as pd
import pingouin as pg

# Load CSV (assumed to be in the same directory)
df = pd.read_csv("rm_anova.csv")

# Repeated-measures ANOVA
# Columns expected:
#   - Subject ID column: "Participant ID"
#   - Within-subject factor: "Planner"
#   - Dependent variable: "Perceived Intelligence"
aov = pg.rm_anova(dv="Perceived Intelligence",
                  within="Planner",
                  subject="Participant ID",
                  data=df,
                  detailed=True)
print("=== Repeated-Measures ANOVA ===")
print(aov)

# Posthoc comparisons for within-subject designs:
# Tukey HSD is not applicable for repeated-measures in pingouin.
# Instead, use paired t-tests with multiple-comparison correction (e.g., Holm).
posthoc = pg.pairwise_ttests(dv="Perceived Intelligence",
                             within="Planner",
                             subject="Participant ID",
                             data=df,
                             padjust="holm",       # multiple-comparison correction
                             effsize="cohen",      # effect size
                             parametric=True,
                             return_desc=False)
print("\n=== Posthoc (paired t-tests with Holm correction) ===")
print(posthoc[["A","B","T","dof","p-unc","p-corr","p-adjust"]])
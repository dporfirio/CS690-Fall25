import pandas as pd
from scipy.stats import chi2_contingency

# Load the CSV file
data = pd.read_csv("chi2.csv")

# Build contingency table (Planner x Success)
table = pd.crosstab(data["Planner"], data["Success"])
print("Contingency Table:\n", table)

# Pearson chi-square test of independence
chi2, p, dof, expected = chi2_contingency(table, correction=False)

print("\nPearson Chi2:", chi2)
print("p-value:", p)
print("Degrees of freedom:", dof)
print("Expected frequencies:\n", expected)
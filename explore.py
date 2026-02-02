import pandas as pd

# Load the cleaned dataset
df = pd.read_csv("db_main.csv")

# Basic info
print("Dataset Info:")
print(df.info())

# Preview first few rows
print("\nFirst 5 rows:")
print(df.head())

# Summary statistics (mostly for numeric/emotion columns)
print("\nSummary statistics:")
print(df.describe())

# Check for missing values
print("\nMissing values per column:")
print(df.isna().sum())

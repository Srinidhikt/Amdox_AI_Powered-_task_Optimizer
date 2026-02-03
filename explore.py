import pandas as pd
df = pd.read_csv("db_main.csv")
print("Dataset Info:")
print(df.info())

# previewing the first few rows for emotion detection
print("\nFirst 5 rows:")
print(df.head())
print("\nSummary statistics:")
print(df.describe())

# check for missing values to avoid the errors
print("\nMissing values per column:")
print(df.isna().sum())

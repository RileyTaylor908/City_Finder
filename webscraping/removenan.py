import pandas as pd

df = pd.read_csv('quality_of_life_metrics.csv')

print("Original DataFrame:")
print(df)

# Exlude columns with 'Comp' in the name
columns = [col for col in df.columns if 'Comp' not in col]

# Remove missing data columns
df_cleaned = df.dropna(subset=columns, how='any')

print("\nDataFrame after removal:")
print(df_cleaned)

df_cleaned.to_csv('cleaned_qual_of_life.csv', index=False)

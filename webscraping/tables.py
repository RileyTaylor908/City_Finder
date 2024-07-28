import pandas as pd

url = "https://www.nestpick.com/generation-z-city-index-2019/"

tables = pd.read_html(url)

# Print tables to determine which one to use
print(f"Number of tables: {len(tables)}")
for i, table in enumerate(tables):
    print(f"\nTable {i}:")
    print(table.head())

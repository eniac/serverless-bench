import time
IMPORT_START_TIME = time.time()
import numpy as np
import pandas as pd
IMPORT_END_TIME = time.time()
print(f"<import {IMPORT_END_TIME - IMPORT_START_TIME} seconds>")

def handler(event, context):
    event = {"seed": 42}
    # Set a seed for reproducibility
    np.random.seed(event["seed"])
    
    # Create a random DataFrame of size 100 with 4 columns
    df = pd.DataFrame({
        'A': np.random.randint(1, 100, size=100),   # Random integers between 1 and 100
        'B': np.random.randn(100),                  # Random numbers from a normal distribution
        'C': np.random.rand(100),                   # Random floats between 0 and 1
        'D': np.random.randint(0, 2, size=100)      # Random binary values (0 or 1)
    })
    
    # 1. Display basic statistics of the DataFrame
    print("Basic Statistics:")
    print(df.describe())
    
    # 2. Sort the DataFrame by column 'A'
    sorted_df = df.sort_values(by='A')
    print("\nSorted DataFrame (by column 'A'):")
    print(sorted_df.head())
    
    # 3. Filter rows where column 'B' is greater than 0
    filtered_df = df[df['B'] > 0]
    print("\nFiltered rows where column 'B' > 0:")
    print(filtered_df.head())
    
    # 4. Add a new column 'E' which is column 'A' squared
    df['E'] = df['A'] ** 2
    print("\nDataFrame with new column 'E' (A squared):")
    print(df.head())
    
    # 5. Group by column 'D' and calculate mean for each group
    grouped_means = df.groupby('D').mean()
    print("\nGrouped by column 'D' with mean values:")
    print(grouped_means)

    return {"import_time": IMPORT_END_TIME - IMPORT_START_TIME}
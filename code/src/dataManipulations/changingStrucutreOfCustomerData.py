import pandas as pd

# Load the CSV file
file_path = "../data/enriched_accounts_new.csv"  # Replace with your actual file path
df = pd.read_csv(file_path)

# Split the first column into four separate columns
df[['CustomerID', 'CustGender', 'CustAccountBalance', 'TransactionDateTime']] = df.iloc[:, 0].str.split(',', expand=True)

# Drop the original first column
df = df.drop(columns=df.columns[0])

# Save the modified DataFrame back to a CSV file (optional)
df.to_csv("../data/enriched_accounts_new_individual_components.csv", index=False)

# Display the first few rows
print(df.head())

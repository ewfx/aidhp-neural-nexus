import pandas as pd
import random

# List of CSV files
csv_files = [
    "bank_loans.csv", "credit_cards.csv", "debit_cards.csv",
    "home_loans.csv", "mortgage_loans.csv", "synthetic_bank_services_dataset.csv"
]

# Path to data folder
data_path = "../data/ProductsData/"

# Collect all unique product names
possibleProducts = set()

for file in csv_files:
    df = pd.read_csv(data_path + file)
    possibleProducts.update(df["Product Name"].dropna().unique())

# Convert set to list
possibleProducts = list(possibleProducts)

# Load enriched_accounts.csv
accounts_df = pd.read_csv("../data/enriched_accounts.csv")

# Function to randomly select products for each user
def random_services():
    return ", ".join(random.sample(possibleProducts, random.randint(1, min(5, len(possibleProducts)))))

# Add new column "servicesUsed"
accounts_df["servicesUsed"] = accounts_df.apply(lambda _: random_services(), axis=1)

# Save the updated file
accounts_df.to_csv("../data/enriched_accounts_new.csv", index=False)

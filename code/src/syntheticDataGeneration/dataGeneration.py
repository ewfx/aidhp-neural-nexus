import pandas as pd
import random
import numpy as np
from faker import Faker

# Initialize Faker for generating fake job titles
fake = Faker()

# Load the existing accounts.csv
accounts_df = pd.read_csv("../data/accounts.csv", delimiter='\t')

# Generate new columns with random values
accounts_df["User_Profile"] = np.random.choice(["Student", "Young Professional", "Retired", "Self-Employed"], len(accounts_df))
accounts_df["Age"] = np.random.randint(20, 71, size=len(accounts_df))
accounts_df["Gender"] = np.random.choice(["Male", "Female"], len(accounts_df))
accounts_df["Marital_Status"] = np.random.choice(["Married", "Single", "Divorced", "Widowed"], len(accounts_df))
accounts_df["Income_Level"] = np.random.choice(["Low", "Medium", "High"], len(accounts_df))
accounts_df["Education_Level"] = np.random.choice(["High School", "College", "University"], len(accounts_df))
accounts_df["Occupation"] = [fake.job() for _ in range(len(accounts_df))]
accounts_df["Residential_Status"] = np.random.choice(["Rent", "Own"], len(accounts_df))
accounts_df["Dependents"] = np.random.randint(0, 6, size=len(accounts_df))
accounts_df["Debt_to_Income"] = np.round(np.random.uniform(0.1, 0.5, size=len(accounts_df)), 2)
accounts_df["Credit_Bureau_Score"] = np.round(np.random.uniform(300, 850, size=len(accounts_df)), 0)
accounts_df["Credit_History"] = np.random.choice(["Good", "Bad", "Moderate"], len(accounts_df))

# Add new inquiry-related columns with True/False values
accounts_df["Recent_Personal_Loan_Inquiry_6M"] = np.random.choice([True, False], len(accounts_df))
accounts_df["Recent_Credit_Card_Inquiry_6M"] = np.random.choice([True, False], len(accounts_df))
accounts_df["Recent_Mortgage_Inquiry_6M"] = np.random.choice([True, False], len(accounts_df))
accounts_df["Recent_Personal_Loan_Inquiry_1Y"] = np.random.choice([True, False], len(accounts_df))
accounts_df["Recent_Credit_Card_Inquiry_1Y"] = np.random.choice([True, False], len(accounts_df))
accounts_df["Recent_Mortgage_Inquiry_1Y"] = np.random.choice([True, False], len(accounts_df))

# Save the modified data to a new CSV file
accounts_df.to_csv("../data/enriched_accounts.csv", index=False)

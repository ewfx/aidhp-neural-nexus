import numpy as np
import pandas as pd

df = pd.read_csv('../data/financial_chatbot_interactions.csv')
df_2 = pd.read_csv('../data/creditCardTransactions.csv')
l = df_2['User'].unique().tolist()
print(type(l))
print(len(l))

creditUsers = list(range(1, 1864))

# Create mapping
user_mapping = dict(zip(creditUsers, l)) # creditUserID -> transactionUserID

df['User_ID'] = df['User_ID'].replace(user_mapping)

print(df.head(3))

df.to_csv('../data/financial_chatbot_interactions_with_creditCardUsers.csv', index=False)
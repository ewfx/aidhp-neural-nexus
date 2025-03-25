import pandas as pd
from sentence_transformers import SentenceTransformer
import os
from pinecone import Pinecone, ServerlessSpec

def createCustomerEmbeddings():

    # Loading and Manipulation
    df = pd.read_csv("../data/enriched_accounts_new_individual_components.csv")
    print(len(df))
    df.dropna(inplace=True)


    # Get API key
    with open("../apiKey/pineconeAPI.txt", "r") as file:
        PINECONE_API_KEY = file.read().strip()

    # Initialize Pinecone
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index_name = "bank-customers-info"

    # Create an index if it doesn't exist
    if index_name not in pc.list_indexes():
        pc.create_index(index_name, dimension=768, 
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        ) )  # Adjust based on embedding model

    # Connect to the index
    index = pc.Index(index_name)

    # Load embedding model
    model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")  # 768

    for idx, row in df.iterrows():
        text_data = f"{row['CustomerID'].split(",")[0]} {row['CustGender']} {row['CustAccountBalance']} {row['TransactionDateTime']} " \
                    f"{row['User_Profile']} {row['Age']} {row['Gender']} {row['Marital_Status']} {row['Income_Level']} " \
                    f"{row['Education_Level']} {row['Occupation']} {row['Residential_Status']} {row['Dependents']} " \
                    f"{row['Debt_to_Income']} {row['Credit_Bureau_Score']} {row['Credit_History']} " \
                    f"{row['Recent_Personal_Loan_Inquiry_6M']} {row['Recent_Credit_Card_Inquiry_6M']} " \
                    f"{row['Recent_Mortgage_Inquiry_6M']} {row['Recent_Personal_Loan_Inquiry_1Y']} " \
                    f"{row['Recent_Credit_Card_Inquiry_1Y']} {row['Recent_Mortgage_Inquiry_1Y']} {row['servicesUsed']}"

        embedding = model.encode(text_data).tolist()  # Convert to list

        metadata = {
            "CustomerID": row["CustomerID"].split(",")[0],
            "CustGender": row["CustGender"],
            "CustAccountBalance": row["CustAccountBalance"],
            "TransactionDateTime": row["TransactionDateTime"],
            "User_Profile": row["User_Profile"],
            "Age": row["Age"],
            "Gender": row["Gender"],
            "Marital_Status": row["Marital_Status"],
            "Income_Level": row["Income_Level"],
            "Education_Level": row["Education_Level"],
            "Occupation": row["Occupation"],
            "Residential_Status": row["Residential_Status"],
            "Dependents": row["Dependents"],
            "Debt_to_Income": row["Debt_to_Income"],
            "Credit_Bureau_Score": row["Credit_Bureau_Score"],
            "Credit_History": row["Credit_History"],
            "Recent_Personal_Loan_Inquiry_6M": row["Recent_Personal_Loan_Inquiry_6M"],
            "Recent_Credit_Card_Inquiry_6M": row["Recent_Credit_Card_Inquiry_6M"],
            "Recent_Mortgage_Inquiry_6M": row["Recent_Mortgage_Inquiry_6M"],
            "Recent_Personal_Loan_Inquiry_1Y": row["Recent_Personal_Loan_Inquiry_1Y"],
            "Recent_Credit_Card_Inquiry_1Y": row["Recent_Credit_Card_Inquiry_1Y"],
            "Recent_Mortgage_Inquiry_1Y": row["Recent_Mortgage_Inquiry_1Y"],
            "servicesUsed": row["servicesUsed"],
        }

        index.upsert([(str(row["CustomerID"].split(",")[0]), embedding, metadata)])  # Using index as ID

        if idx % 10 == 0:
            print(f"Processed {idx} records")

        print(f"Finished processing {len(df)} records")

def findSimilarUsers(CustomerID, k=3):

    with open("../apiKey/pineconeAPI.txt", "r") as file:
        PINECONE_API_KEY = file.read().strip()

    pc = Pinecone(api_key=PINECONE_API_KEY)
    index_name = "bank-customers-info"
    index = pc.Index(index_name)

    # Get the query corresponding to CustomerID
    customer_results = index.query(
        id=CustomerID,  # Querying using CustomerID
        top_k=k,  # Retrieve only this user's vector
        include_values=True
    )
    similarCustomers = [match['id'] for match in customer_results['matches']]
    return similarCustomers
    



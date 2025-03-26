import pandas as pd
from sentence_transformers import SentenceTransformer
# import pinecone
import os
from pinecone import Pinecone, ServerlessSpec

# Loading and Manipulation
df = pd.read_csv("../data/ProductsData/merged_output.csv")
print(len(df))
# df = df[["Product name", "Description", "Category"]]
df.dropna(inplace=True)


# Get API key
with open("../apiKey/pineconeAPI.txt", "r") as file:
    PINECONE_API_KEY = file.read().strip()

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "banking-services-and-products-recommendations"

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
# model = SentenceTransformer("all-MiniLM-L6-v2") # 384
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2") # 768

for idx, row in df.iterrows():
    text_data = f"{row['Product Name']} {row['Description']} {row['Category']}"
    embedding = model.encode(text_data).tolist()  # Convert to list
    metadata = {
        "product_name": row["Product Name"],
        "description": row["Description"],
        "category": row["Category"],
    }
    index.upsert([(str(idx), embedding, metadata)])  # Using index as ID
    if idx % 10 == 0:
        print(f"Processed {idx} products")

print(f"Finished processing {len(df)} products")

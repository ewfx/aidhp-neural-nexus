# Collaborative filtering using LLM and Embeddings

# Summary: 
#   - Objective: This action can be used to generate product recommendations for a given user based on the similarity with other users.
#   - The user's personal characteristics like Age, Income etc. are used to find similar users.
#   - Based on the set of similar users, we will try to get the products similar to the user characteristics (If the occupation is student, we can suggest something like student credit cards)
#   - The user profiles and the similar products are then passed to the DeepSeek Chatbot to generate the final refined recommendations.

# How to use this,
#          from collaborativeFilteringLLM import collaborativeFiltering
#          collaborativeFiltering("C1015616")  # customer ID as string

# UI Page - Should be shown in the recommendations Page of the application


import sys
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from deepseek_chatbot import generateDeepSeekChatBotResponse
from pinecone import Pinecone, ServerlessSpec

sys.path.append('../pushingData2VectorDB')
from customerInfoToVectorDB import findSimilarUsers


def generateUserQuery(similarUsers, CustomerID):
    # Get the records of similar users from database
    df = pd.read_csv("../data/enriched_accounts_new_individual_components.csv")
    # similarUsersRecords = df[df['CustomerID'].isin(similarUsers) & (df['CustomerID'] != CustomerID)]
    similarUsersRecords = df[df['CustomerID'].isin(similarUsers)]
    output_text = f"THESE ARE THE SET OF USERS WHO ARE SIMILAR TO CUSTOMER {CustomerID}:\n\n{{\n"
    ind = 0
    for index, row in similarUsersRecords.iterrows():
        output_text += f"CUSTOMER {ind + 1}\n"
        for col in similarUsersRecords.columns:
            output_text += f"    {col}: {row[col]},\n"
        output_text += "\n"
        ind += 1

    output_text += "}"
    return output_text

def collaborativeFiltering(CustomerID):
    # Step1: Get similar customers
    similarUsers = findSimilarUsers(CustomerID, k=6)
    # Step2: Get the records of similar users from database
    initialPrompt = generateUserQuery(similarUsers, CustomerID)
    # Step3: Generate the final query to get a list of products from product database
    query = '''
            SUGGEST WHAT KIND OF FINANCIAL PRODUCTS WILL THESE SET OF CUSTOMERS LIKE BASED ON THEIR FEATURES. 

            SET OF CUSTOMERS: {initialPrompt}
    '''
    model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2") # 768
    embedding = model.encode(query).tolist()  # Convert to list

    # Query Pinecone
    with open("../apiKey/pineconeAPI.txt", "r") as file:
        PINECONE_API_KEY = file.read().strip()

    pc = Pinecone(api_key=PINECONE_API_KEY)
    index_name = "banking-services-and-products-recommendations"

    index = pc.Index(index_name)
    results = index.query(
        vector=embedding,
        top_k=7,
        include_metadata=True
    )
    metadata_list = [match['metadata'] for match in results['matches']]
    
    recommendationPrompt = f'''
    THESE ARE THE GROUP OF SIMILAR USERS AND RECOMMENDING PROUDCTS TO THIS GROUP WILL INCREASE THE IMPACT. CHOOSE THE TOP 3 financial PRODUCTS THAT ARE HIGHLY RELEVANT TO THE CONVERSATION FROM THE SET OF PRODUCTS: 
    {metadata_list} 

    SET OF SIMILAR USERS: {query}

    IF YOU FEEL THAT IT IS NOT RELEVEANT, JUST SAY 'YOU CAN CHECK OUT ABOUT DIFFERENT PRODUCTS IN OUR WEBSITE
    '''
    recommendedProductsAnswer = generateDeepSeekChatBotResponse(recommendationPrompt)
    print("Recommendations by DeepSeek Chatbot: ")
    print(recommendedProductsAnswer) # take this answer and display in ui


# Sample query
# collaborativeFiltering("C1015616")
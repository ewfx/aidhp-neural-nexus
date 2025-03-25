# The periodicSummaryUpdate() function updates the transaction summaries (both credit and debit) for each user periodically. 
# Based on those transaction summaries, we can recommend products to the user (If someone makes many luxury transaction, we can recommend him a luxury credit card)
# NOTE: for simplicity, only 10 user's summaries are updated

# How to use this
#          periodicSummaryUpdate()  # call this function to update the summaries every week/month depending on the traffic
#          getRecommendations("C5533885")  # call this function to get product recommendations for a user based on his transaction summaries


import pandas as pd
import os
import numpy as np
from huggingface_hub import InferenceClient  # Ensure correct import
from deepseek_chatbot import generateDeepSeekChatBotSummarizer, generateDeepSeekChatBotResponse
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec


# File paths
previous_txn_path = "../data/previousTransactionHistory.csv"
credit_card_txn_path = "../data/creditCardTransactions.csv"
summary_output_path = "../data/Summary/userTransactionsSummary.csv"

def load_data():
    previous_txn_df = pd.read_csv(previous_txn_path)
    credit_card_txn_df = pd.read_csv(credit_card_txn_path)
    return previous_txn_df, credit_card_txn_df

def process_transactions(previous_txn_df, credit_card_txn_df):
    summary_list = []
    unique_users = previous_txn_df['CustomerID'].unique()
    sampleUser = 10
    for user in unique_users:
        if sampleUser == 0:
            break
        print("Processing user:", user)
        user_txns = previous_txn_df[previous_txn_df['CustomerID'] == user]
        credit_txns = credit_card_txn_df[credit_card_txn_df['User'] == user]
        whatToDo = "Summarize these set of transactions of the user and try to find patterns and important pattern in the data. The aim is to understand his behavior and summarize that AS PARAGRAPHS"
        user_txn_summary = generateDeepSeekChatBotSummarizer(whatToDo, user_txns.to_dict(orient='records'))
        credit_card_summary = generateDeepSeekChatBotSummarizer(whatToDo, credit_txns.to_dict(orient='records'))
        summary_list.append({
            "CustomerID": user,
            "TransactionSummary": user_txn_summary,
            "CreditCardSummary": credit_card_summary
        })
        sampleUser -= 1
    
    summary_df = pd.DataFrame(summary_list)
    print(summary_df.head(3))
    summary_df.to_csv(summary_output_path, index=False)

def periodicSummaryUpdate():
    # Creating csv if it does not exist
    created = False
    os.makedirs(os.path.dirname(summary_output_path), exist_ok=True)
    if not os.path.exists(summary_output_path):
        df = pd.DataFrame(columns=["CustomerID", "TransactionSummary", "CreditCardSummary"])  # Modify columns as needed
        df.to_csv(summary_output_path, index=False)
        print(f"Created empty CSV at {summary_output_path}")
    else:
        print(f"CSV already exists at {summary_output_path}")
    
    previous_txn_df, credit_card_txn_df = load_data()
    process_transactions(previous_txn_df, credit_card_txn_df)
    print("Transaction summaries saved successfully!")

def getRecommendations(CustomerID):
    df = pd.read_csv(summary_output_path)
    user_summary = df[df['CustomerID'] == CustomerID]
    data = f'''
            TRANSACTION SUMMARY FOR THIS USER: {user_summary['TransactionSummary'].values[0]}
            
            CREIDT CARD SUMMARY FOR THIS USER: {user_summary['CreditCardSummary'].values[0]}
    '''
    # Query 1 - Based on data create embeddings and find similar embeddings from the vector db
    model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2") # 768
    embedding = model.encode(data).tolist() 

    with open("../apiKey/pineconeAPI.txt", "r") as file:
        PINECONE_API_KEY = file.read().strip()

    pc = Pinecone(api_key=PINECONE_API_KEY)
    index_name = "banking-services-and-products-recommendations"

    index = pc.Index(index_name)
    # Query Pinecone
    results = index.query(
        vector=embedding,
        top_k=7,
        include_metadata=True
    )
    metadata_list = [match['metadata'] for match in results['matches']]
    
    recommendationPrompt = f'''
    GIVEN: {data}. 
    
    CHOOSE THE TOP 3 financial PRODUCTS THAT ARE HIGHLY RELEVANT TO THE CONVERSATION FROM THE SET OF PRODUCTS: {metadata_list} 

    FOR EACH PRODUCT, TELL WHY YOU CHOSE THAT PRODUCTS FOR THE CURRENT USER (IN JUST 1 LINE FOR EACH PRODUCT).

    IF YOU FEEL THAT IT IS NOT RELEVEANT, JUST SAY 'YOU CAN CHECK OUT ABOUT DIFFERENT PRODUCTS IN OUR WEBSITE'
    '''
    recommendedProductsAnswer = generateDeepSeekChatBotResponse(recommendationPrompt)
    print("Recommendations by DeepSeek Chatbot: ")
    print(recommendedProductsAnswer) # take this answer and display in ui


# periodicSummaryUpdate() # -> call this function to update the summaries
# getRecommendations("C5533885") # -> call this function to get recommendations for a user based on his transaction summaries
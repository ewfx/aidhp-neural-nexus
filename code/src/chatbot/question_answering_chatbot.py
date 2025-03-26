# askQuestion(question) function is used in the chatbot section of the app. Whenever the user enters a query in the input box and clicks on the submit button, the askQuestion function is called. 
# The function takes the user's question as input and performs the following steps:
#   - Chatbot answers the question
#   - The interaction is summarized
#   - Based on the summary, the similar products are queried from the vector database  - Product Recommendations
# Along with answering the question, it also generates a set of product recommendations related to that query

from deepseek_chatbot import generateDeepSeekChatBotResponse
from mistral_chatbot import generateChatBotResponse
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec


def askQuestion(question):
    # Query 1
    answer = generateDeepSeekChatBotResponse(question)
    print("Answer by DeepSeek Chatbot: ")
    print(answer)
    # return answer
    # Query 2
    prompt = f'''
            THE USER ASKED: {question} and THE CHATBOT answered: {answer}. Summarize this into a single paragraph
            '''
    summary = generateChatBotResponse(prompt)
    # Query 3 - Based on summary create embeddings and find similar embeddings from the vector db
    model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2") # 768
    embedding = model.encode(summary).tolist()  # Convert to list

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
    The summary of the conversation between user and chatbot is: {summary}. CHOOSE THE TOP 3 financial PRODUCTS THAT ARE HIGHLY RELEVANT TO THE CONVERSATION FROM THE SET OF PRODUCTS: 
    {metadata_list} 

    IF YOU FEEL THAT IT IS NOT RELEVEANT, JUST SAY 'YOU CAN CHECK OUT ABOUT DIFFERENT PRODUCTS IN OUR WEBSITE
    '''

    recommendedProductsAnswer = generateDeepSeekChatBotResponse(recommendationPrompt)
    print("Recommendations by DeepSeek Chatbot: ")
    print(recommendedProductsAnswer) # take this answer and display in ui
    # return recommendedProductsAnswer
    return answer
    

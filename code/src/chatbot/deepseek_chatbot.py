from huggingface_hub import InferenceClient
import os
from environmentVariableSetup import setEnvironmentVariables

def CollaborativeFilteringUsingDeepSeek(userInfoPrompt):
    # Setting environment variables
    if(os.getenv("HUGGINGFACE_KEY") == None):
        print("HUGGINGFACE_KEY environment variable is None")
        setEnvironmentVariables()
        print("HUGGINGFACE_KEY environment variable is set to the value in the file")

    client = InferenceClient(
        provider="novita",
        api_key=os.getenv("HUGGINGFACE_KEY"),
    )

    template = f""" 
                GIVEN THE SET OF THESE USERS, SUGGEST PRODUCTS 
    **Question:** {question}  
                    **Answer:** 

                    """

    completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
        messages=[
            {
                "role": "system",
                "content": template
            }
        ],
        max_tokens=2000,
    )
    # print(completion.choices[0].message.content.split("</think>", 1)[1])
    return completion.choices[0].message.content.split("</think>", 1)[1]


def generateDeepSeekChatBotResponse(question):
    # Setting environment variables
    if(os.getenv("HUGGINGFACE_KEY") == None):
        print("HUGGINGFACE_KEY environment variable is None")
        setEnvironmentVariables()
        print("HUGGINGFACE_KEY environment variable is set to the value in the file")

    client = InferenceClient(
        provider="novita",
        api_key=os.getenv("HUGGINGFACE_KEY"),
    )

    template = f""" GENERAL GUIDELINES: 
                    You are a professional financial investment advisor chatbot, designed to provide insightful, data-driven, and reliable investment recommendations. Your role is to assist users in making informed financial decisions, considering factors such as risk tolerance, investment horizon, market trends, and available investment options.
                    **Now, answer the following question in a clear and structured manner:**
                    NOTE: If any question is not related to finance domain, YOU MUST NOT ANSWER THAT. Just say "This is not a finance related question. Please ask a finance related question." and end the response
                    **Question:** {question}  
                    **Answer:** 

                    """

    completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
        messages=[
            {
                "role": "system",
                "content": template
            }
        ],
        max_tokens=2000,
    )
    # print(completion.choices[0].message.content.split("</think>", 1)[1])
    return completion.choices[0].message.content.split("</think>", 1)[1]

def generateDeepSeekChatBotGenericResponse(question):
    # Setting environment variables
    if(os.getenv("HUGGINGFACE_KEY") == None):
        print("HUGGINGFACE_KEY environment variable is None")
        setEnvironmentVariables()
        print("HUGGINGFACE_KEY environment variable is set to the value in the file")

    client = InferenceClient(
        provider="novita",
        api_key=os.getenv("HUGGINGFACE_KEY"),
    )

    template = f""" Answer the following question in a clear and structured manner:**
                    **Question:** {question}  
                    **Answer:** 
                    """

    completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
        messages=[
            {
                "role": "system",
                "content": template
            }
        ],
        max_tokens=2000,
    )
    # print(completion.choices[0].message.content.split("</think>", 1)[1])
    return completion.choices[0].message.content.split("</think>", 1)[1]

def generateDeepSeekChatBotSummarizer(whatToDo, data):
    # Setting environment variables
    if(os.getenv("HUGGINGFACE_KEY") == None):
        print("HUGGINGFACE_KEY environment variable is None")
        setEnvironmentVariables()
        print("HUGGINGFACE_KEY environment variable is set to the value in the file")

    client = InferenceClient(
        provider="novita",
        api_key=os.getenv("HUGGINGFACE_KEY"),
    )

    template = f""" {whatToDo}
                     Summarize in a clear and structured manner:**
                    **SET OF TRANSACTIONS MADE BY THE USER:** {data}  
                    **Answer:** 
                    """

    completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
        messages=[
            {
                "role": "system",
                "content": template
            }
        ],
        max_tokens=2000,
    )
    # print(completion.choices[0].message.content.split("</think>", 1)[1])
    return completion.choices[0].message.content.split("</think>", 1)[1]



# generateDeepSeekChatBotResponse("who will win IPL 2025 ? CSK or MI ?")
# print("-------------------------------------------------------------------------------------------------------------------------------------------------------")
# generateDeepSeekChatBotResponse("Is it better to invest in FD or Large Cap funds if I am going to retire after 35 years ?")
# print("-------------------------------------------------------------------------------------------------------------------------------------------------------")

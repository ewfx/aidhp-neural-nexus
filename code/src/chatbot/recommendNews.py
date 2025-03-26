import requests
import os
from deepseek_chatbot import generateDeepSeekChatBotTopicExtractor
import re

def setNewsAPIKey():
    with open("../apiKey/newsAPI.txt", "r") as file:
        secret_key = file.read().strip()  # Strip to remove any newline characters
        os.environ["NEWS_API_KEY"] = secret_key



# Function to analyze user tweet using DeepSeek
def analyze_tweet(tweet):
    query = f'Extract the key financial topic from this tweet and just list those topics and nothing else (no description or explanation). Format to return answer: [topic1, topic2, topic3, ] etc.'
    result = generateDeepSeekChatBotTopicExtractor(query, tweet)    
    lst = result.strip("[]").split(", ")
    print(lst[0])
    return lst

# Function to fetch finance news
def get_finance_news(query):
    setNewsAPIKey()
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={os.getenv("NEWS_API_KEY")}"
    
    response = requests.get(url)
    articles = response.json().get("articles", [])[:5]  # Get top 5 articles
    return [(article["title"], article["url"]) for article in articles]

# Main function to recommend finance news
def suggest_news(tweet):
    topic = analyze_tweet(tweet)
    for sample in topic:
        sample = sample.strip()
        sample = re.sub(r'[^A-Za-z0-9\s]', '', sample)  # Remove special characters
        sample = re.sub(r'\s+', ' ', sample)  # Replace multiple spaces with a single space
        print(f"🔍 Identified Topic: {sample}")
        articles = get_finance_news(sample)
        if articles:
            print("\n📢 Suggested Finance News Articles:")
            for title, url in articles:
                print(f"- {title} ➡ {url}")
        else:
            print("\n⚠ No relevant news found.")

# Example tweet
tweet = "Tech stocks are dropping after Fed's rate hike! Should investors worry?"
suggest_news(tweet)

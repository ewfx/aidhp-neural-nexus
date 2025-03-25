import os

# Setting Enviornment Variables
def setEnvironmentVariables():
    with open("../apiKey/huggingFace.txt", "r") as file:
        secret_key = file.read().strip()  # Strip to remove any newline characters
    os.environ["HUGGINGFACE_KEY"] = secret_key
    huggingface_key = os.getenv("HUGGINGFACE_KEY")
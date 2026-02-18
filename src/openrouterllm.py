import requests
import os
from dotenv import load_dotenv

# IMPORTANT
# I sent the .env file with the api key  in the chat, but I will not be including it in the code repository for security reasons and github gets whiny about it lol
# Just drop that .env file in the same directory as this script and it should work fine
# I have that .env file added to .gitignore so it wont be included in the repo
# thanks guys :3

load_dotenv() # load environment variables from .env file

# set api key and endpoint 
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError("API key not found. Please check your .env file and ensure OPENROUTER_API_KEY is set.")
API_URL = 'https://openrouter.ai/api/v1/chat/completions' # api url, program will send requests and get responses from here

# restricted words/topics, chatbot will not responsd
RESTRICTED_WORDS = ["poop"]

# get llm response functions
def getLLMResponse(messages):
    # set headers and data for the request
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openrouter/free",  # free models router
        "messages": messages # will declare limits at start of chat loop
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status() # check for errors
        responseData = response.json()
        return responseData['choices'][0]['message']['content'] # return the content of the response
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as e:
        return f"Error: {e}"
    
# console chat loop

def chatConsole():
    print("Welcome! this is a test run of using openrouter free. type 'quit' to exit.\n")

    # this is where the chatbot will be constrained.
    messages = [
            { "role": "system", 
                "content": (
                    "You are a helpful, eco-conscious content generation assistant. You will follow these rules:\n"
                    #"Do not invent any ingredients or inputs; only use what the user provides.\n"
                    #"You are strictly constrained to the provided ingredients.\n"
                    #"For any recipe or content generation, only use the ingredients provided by the user. Do not suggest any additional ingredients or substitutions.\n"
                    "This is only for content generation; do not provide decision-making guidelines.\n"
                    "Avoid giving food safety advice, handling instructions, or any information that could be misused.\n"
                    "Respond politely and concisely using only the context provided.\n"
                    "If the user asks for information not included in the provided context, respond with 'I don't have that information.'\n")
            }]
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            print("Goodbye!")
            break
        
        #  check for forbidden words/topics
        if any(word in user_input.lower() for word in RESTRICTED_WORDS):
            print("LLM: Sorry, I can't discuss that topic.\n")
            continue
        
        # append user message to conversation
        messages.append({"role": "user", "content": user_input})
        
        # get ai response
        response = getLLMResponse(messages)
        print(f"LLM: {response}\n")
        
        # append ai response to conversation for context
        messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    chatConsole()    
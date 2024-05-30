
from pip._vendor import requests
import json
# import openai
# import creds as creds
import os
import dotenv
from dotenv import load_dotenv, find_dotenv

APIKEY = ""



dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

APIKEY = os.environ.get("CHAT_KEY")

print(APIKEY)
# Define the endpoint URL
url = "https://api.openai.com/v1/chat/completions"

# Define the request headers
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + APIKEY
}

# Define the request payload
payload = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": f"You are a Music Reccomendation assistant, I will give you a genre name or lead, and then you will reccomend one song based on that. And you will only say the song name, and artist, nothing else\
                    Reccomend me a song that is rock."}],
    "temperature": 0.7
}

# Convert payload to JSON format
payload_json = json.dumps(payload)

# Make the POST request
# response = requests.post(url, headers=headers, data=payload_json)

# Print the response
myDict = {}
# myDict = response.json()
# myDict= myDict['choices']
# myDict = myDict[0]
# myDict = myDict['message']['content']


print(myDict)
from fastapi import FastAPI, Request
import requests
import json

app = FastAPI()

@app.get("/chatbot")
async def chatbot(request: Request):
    # Get the 'question' parameter from URL
    question = request.query_params.get('question', 'Hi')  # Default to 'Hi' if not provided

    # Prepare the payload with the user message
    payload = {
        'messages': [
            {
                'role': 'user',
                'content': question
            }
        ]
    }

    # Convert the payload to JSON format
    json_payload = json.dumps(payload)

    # Define the headers to match the provided request
    headers = {
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'accept': 'application/json',
        'sec-ch-ua-platform': '"Android"',
        'dnt': '1',
        'sec-ch-ua-mobile': '?1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36',
        'content-type': 'application/json',
        'origin': 'https://seoschmiede.at',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'accept-language': 'en-US,en;q=0.9,bn;q=0.8,ru;q=0.7,zh-CN;q=0.6,zh;q=0.5,hi;q=0.4',
        'priority': 'u=1, i'
    }

    # API URL to send the payload
    url = 'https://chatbot-ji1z.onrender.com/chatbot-ji1z'

    try:
        # Send the POST request
        response = requests.post(url, data=json_payload, headers=headers)

        # Print the raw response
        print("Raw Response:", response.text)

        # Return the raw response
        return response.text

    except Exception as e:
        return {"status": "error", "message": str(e)}

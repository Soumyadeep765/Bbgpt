from fastapi import FastAPI, Request
import requests
import json

app = FastAPI()

# Function to fetch content from the given URL
def fetch_role_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.strip()  # Strip to remove any leading/trailing whitespace
    else:
        return "Default system message."  # Handle fetch failure

# API endpoint for handling requests
@app.get("/chatbot")
async def chatbot(request: Request):
    # Get the 'question' parameter from URL
    question = request.query_params.get('question', 'Hi')  # Default to 'Hi' if not provided

    # Fetch the role content from the provided URL
    role_content = fetch_role_content('https://api.teleservices.io/bb.txt')

    # Prepare the payload
    payload = {
        'messages': [
            {
                'role': 'system',
                'content': role_content
            },
            {
                'role': 'user',
                'content': question
            }
        ]
    }

    # Convert the payload to JSON format
    json_payload = json.dumps(payload)

    # Define the headers
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
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-US,en;q=0.9,bn;q=0.8,ru;q=0.7,zh-CN;q=0.6,zh;q=0.5,hi;q=0.4',
        'priority': 'u=1, i'
    }

    # API URL to send the payload
    url = 'https://chatbot-ji1z.onrender.com/chatbot-ji1z'

    try:
        # Send the POST request
        response = requests.post(url, data=json_payload, headers=headers)

        # Debugging: Print response content for analysis
        print("Response content:", response.text)

        # Create a response structure
        if response.status_code == 200:
            # Attempt to parse the response
            try:
                api_response = response.json()
                response_data = {
                    'status': 'success',
                    'message': api_response['choices'][0]['message']['content']
                }
            except json.JSONDecodeError as e:
                response_data = {
                    'status': 'error',
                    'message': f"Failed to decode JSON response: {e}"
                }
        else:
            response_data = {
                'status': 'error',
                'message': f"Failed. Status code: {response.status_code}. Response: {response.text}"
            }

    except Exception as e:
        response_data = {
            'status': 'error',
            'message': f"An error occurred: {str(e)}"
        }

    # Return the JSON response
    return response_data

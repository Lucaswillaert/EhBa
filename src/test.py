import requests
import json

# Zorg ervoor dat je function_app_url correct is ingesteld
function_app_url = "https://your_function_app_url/api/ehb-chatbot"  # Update this with your actual Function App URL

def test_function_app(question):
    payload = {
        "question": question
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(function_app_url, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        print("Response from the AI:")
        print(response.text)
    else:
        print(f"Failed to get a response. Status code: {response.status_code}")

if __name__ == "__main__":
    question = input("Enter your question: ")
    test_function_app(question)

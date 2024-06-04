import logging
import openai
import os
import json
import azure.functions as func
from dotenv import load_dotenv

load_dotenv()
# Set up Azure OpenAI
azure_oai_key = os.getenv("OPENAI_API_KEY_1")
azure_oai_endpoint = os.getenv("OPENAI_ENDPOINT")
azure_oai_deployment = os.getenv("OPENAI_DEPLOYMENT")

logging.info("Azure OpenAI Key: %s", azure_oai_key)
logging.info("Azure OpenAI Endpoint: %s", azure_oai_endpoint)
logging.info("Azure OpenAI Deployment: %s", azure_oai_deployment)

# Initialize the Azure OpenAI client
client = openai.AzureOpenAI(
    azure_endpoint=azure_oai_endpoint,
    api_key=azure_oai_key,
    api_version="2024-02-15-preview"
)

def is_relevant_query(query):
    # Simple keyword-based approach to filter out irrelevant queries
    keywords = ["Erasmushogeschool", "Brussel", "EHB", "Erasmus", "VUB", "universiteit", "hogeschool",
                # Add more keywords as needed
                ]
    for keyword in keywords:
        if keyword.lower() in query.lower():
            return True
    return False

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('HTTP trigger function received a request.')

    system_message = """Je bent een behulpzame assistent die vragen beantwoordt over de Erasmus Hogeschool Brussel (EhB).
    Beantwoord alleen vragen die specifiek betrokken zijn met de erasmus hogeschool Brussel en zijn opleidingen.
    Als de vraag niet relevant is aan de erasmus hogeschool Brussel en zijn opleidingen, geef dan aan dat de vraag niet relevant is."""

    try:
        request_data = req.get_json()
        previous_messages = request_data.get('previousMessages', [])
        current_message = request_data.get('currentMessage')

        if not current_message or not current_message.get('message'):
            return func.HttpResponse(json.dumps({"status": "error", "message": "Please pass a question in the request"}), status_code=400)

        question = current_message.get('message')

        # Check if the question is relevant
        if not is_relevant_query(question):
            return func.HttpResponse(json.dumps({"status": "error", "message": "This chatbot only answers questions about Erasmushogeschool Brussel."}), status_code=400)

        # Prepare messages for the API
        messages = [{"role": "system", "content": system_message}]
        for msg in previous_messages:
            role = "assistant" if msg['sender'] == "bot" else "user"
            messages.append({"role": role, "content": msg['message']})
        messages.append({"role": "user", "content": question})

        # Send the prompt to the OpenAI deployment
        response = client.chat.completions.create(
            model=azure_oai_deployment,
            temperature=0.3,
            max_tokens=800,
            messages=messages
        )

        generated_text = response.choices[0].message.content
        return func.HttpResponse(json.dumps({"status": "success", "message": generated_text}), mimetype="application/json", status_code=200, headers={
            'Access-Control-Allow-Origin': '*'
        })

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse(json.dumps({"status": "error", "message": "Error processing request"}), status_code=500)
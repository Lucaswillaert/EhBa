import logging
import openai
import os
import json
import azure.functions as func

# Set up Azure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
openai_endpoint = os.getenv("OPENAI_ENDPOINT")

def is_relevant_query(query):
    # Simple keyword-based approach to filter out irrelevant queries
    keywords = ["Erasmushogeschool", "Brussel", "EHB", "programs", "admissions", "tuition", "campus", "student life"]
    for keyword in keywords:
        if keyword.lower() in query.lower():
            return True
    return False

def build_prompt(question, chat_history):
    # Construct the prompt with the chat history
    prompt = "You are a knowledgeable assistant specialized in providing information about Erasmushogeschool Brussel. Maintain context and respond accurately based on the conversation history. Here is the conversation history:\n"
    for entry in chat_history:
        role = entry['role']
        content = entry['content']
        prompt += f"{role}: {content}\n"
    prompt += f"user: {question}\nassistant:"
    return prompt

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('HTTP trigger function received a request.')

    try:
        # Extract the question and chat history from the request
        request_data = req.get_json()
        question = request_data.get('question')
        chat_history = request_data.get('chat_history', [])

        if not question:
            return func.HttpResponse("Please pass a question in the request", status_code=400)

        # Check if the question is relevant
        if not is_relevant_query(question):
            return func.HttpResponse("This chatbot only answers questions about Erasmushogeschool Brussel.", status_code=400)

        # Perform prompt engineering by building the prompt with chat history
        prompt = build_prompt(question, chat_history)

        # Send the prompt to the OpenAI deployment
        response = openai.Completion.create(
            engine=openai_endpoint,
            prompt=prompt,
            max_tokens=150
        )

        # Prepare the response
        result = {
            "openai_response": response.choices[0].text.strip()
        }

        return func.HttpResponse(json.dumps(result), mimetype="application/json")

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse("Error processing request", status_code=500)

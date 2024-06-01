import os
import azure.functions as func
import openai
import logging
from azure.storage.blob import BlobServiceClient

# Initialize OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Blob Storage
blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))
container_name = os.getenv("AZURE_CONTAINER_NAME")

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="ehb-chatbot", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def ehbchatfunction(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try: 
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    # Get the question from the request
    question = req_body.get('question')

    if not question: 
        return func.HttpResponse("Please provide a question.", status_code=400)

    # Retrieve the context data from Blob Storage
    context = get_all_blob_data()

    # Generate a response using OpenAI
    response_text = generate_response(question, context)

    return func.HttpResponse(response_text, mimetype="text/plain")


def get_all_blob_data():
    container_client = blob_service_client.get_container_client(container_name)
    blob_data = ""

    for blob in container_client.list_blobs():
        blob_client = container_client.get_blob_client(blob)
        blob_content = blob_client.download_blob().readall().decode('utf-8')
        blob_data += blob_content + "\n"

    return blob_data

#deze functie nog niet geimplementeerd! 
def generate_response(question, context):
    # Prepare the prompt for OpenAI
    prompt = (
        f"{context}\n"
        f"Vraag: {question}\n"
        "Antwoord:"
    )

    response = openai.Completion.create(
        engine="text-davinci-002",  # GPT-3 model
        prompt=prompt,
        max_tokens=150
    )
    answer = response.choices[0].text.strip()

    return answer

context = (
        "Je bent een behulpzame assistent die vragen beantwoordt over de Erasmus Hogeschool Brussel (EhB)."
        "Beantwoord alleen vragen die specifiek betrokken zijn met de erasmus hogeschool Brussel en zijn opleidingen."
        "Als de vraag niet relevant is aan de erasmus hogeschool Brussel en zijn opleidingen, geef dan aan dat de vraag niet relevant is"
        f"Vraag: {question}/nAntwoord: "
    )
import os
import azure.functions as func
import openai
import logging
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient


openai.api_key = os.getenv("AZURE_FUNCTION_API_KEY")
search_key = os.getenv("AZURE_SEARCH_KEY")
index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")
search_endpoint= os.getenv("AZURE_SEARCH_ENDPOINT")

search_client = SearchClient(endpoint=search_endpoint,
                             index_name=index_name,
                             credential=AzureKeyCredential(search_key))

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="ehb-chatbot", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def ehbchatfunction(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try: 
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("invalid JSON", status_code=400)
    
    question = req_body.get('question')

    if not question: 
        return func.HttpResponse("Please provide a question." , status_code=400)
    
    results = search_client.search(search_text=question)

    answers = [doc['content'] for doc in results]


    if answers:
        response = "\n".join(answers)
    else:
        response= "No relevant information found."
    #genereer een reactie obv de ontvangen vraag

    #return de reactie als HTTP-respons
    return func.HttpResponse(response, mimetype="text/plain")


#deze functie nog niet geimplementeerd! 
def generate_response(question):

    #stel de context in:
    context = (
        "Je bent een behulpzame assistent die vragen beantwoordt over de Erasmus Hogeschool Brussel (EhB)."
        "Beantwoord alleen vragen die specifiek betrokken zijn met de erasmus hogeschool Brussel en zijn opleidingen."
        "Als de vraag niet relevant is aan de erasmus hogeschool Brussel en zijn opleidingen, geef dan aan dat de vraag niet relevant is"
        f"Vraag: {question}/nAntwoord: "
    )

    #gebruik GPT-3 om een reactie te genereren op basis van de context
    response = openai.Completion.create(
        engine="text-davinci-002", #GPT3 model
        prompt = context,
        max_tokens = 50
    )
    #extraheren van het antwoord uit de respons van GPT3
    answer = response.choices[0].text.strip()

    return answer
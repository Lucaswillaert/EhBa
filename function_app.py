import logging
import openai
import os
import json
import azure.functions as func

# Set up Azure OpenAI
openai.api_key = "b2d18fd406c84ee88cdcf1b954cd882f"
openai_endpoint = "https://ehbot.openai.azure.com/"


def is_relevant_query(query):
    # Simple keyword-based approach to filter out irrelevant queries
    keywords = [
        "Erasmushogeschool", "Brussel", "EHB", "Erasmus", "VUB", "universiteit", "hogeschool",
        "lessen", "buitenland", "stage", "richting", "examens", "inschrijving", "studenten",
        "docenten", "opleiding", "vakken", "studiepunten", "studie", "campus", "bibliotheek",
        "studentenvereniging", "studentenraad", "studentenbegeleiding", "studiebegeleiding",
        "studieadvies", "studiekeuze", "studiebeurs", "studietoelage", "studievoorschot",
        "studiecontract", "studiegeld", "studieprogramma", "studievoortgang", "verplichte vakken",
        "keuzevakken", "studiebegeleider", "studiebegeleiders", "studieadviseur", "beurs",
        "toelage", "voorschot", "contract", "geld", "programma", "voortgang", "puntentabel",
        "puntensysteem", "puntentotaal", "puntentekort", "puntentekorten", "keuze", "begeleider",
        "begeleiders", "adviseur", "bib", "vereniging", "raad", "begeleiding", "advies",
        "collegegeld", "studievertraging", "studieduur", "studieschuld", "inschrijfprocedure",
        "college", "colleges", "docent", "professor", "opleidingstraject", "curriculum", "ECTS",
        "studieresultaten", "tentamen", "examenperiode", "studielening", "financiële steun",
        "studiefinanciering", "studentenwoning", "studentenkamer", "kot", "huisvesting",
        "studentenhuisvesting", "campusleven", "studiegenoot", "mentor", "studiecoach", "onderwijs",
        "lesmateriaal", "scriptie", "proefschrift", "promotieonderzoek", "promotor", "studentenkaart",
        "studentenpas", "introductiedag", "introductieweek", "studievereniging", "studieclub",
        "werkcollege", "hoorcollege", "seminarie", "project", "stageplaats", "stagemogelijkheden",
        "studieplanning", "zelfstudie", "studiegids", "studiehandleiding", "onderwijsmodule",
        "onderwijsvorm", "curriculumonderdeel", "werkstuk", "studieprestatie", "studieopdracht",
        "opdracht", "tentamenweek", "herkansing", "academisch", "academische kalender", "studiepuntenregistratie",
        "onderzoeksproject", "onderzoeksvoorstel", "studieomgeving", "studieruimte", "collegezaal",
        "studiebeursaanvraag", "beurzen", "studielast", "studiebelasting", "academische graad",
        "bachelor", "master", "promotie", "promovendus", "wetenschappelijke publicatie", "scriptiebegeleider",
        "scriptieonderwerp", "studievorm", "studierichting", "afstudeerrichting", "keuzevak",
        "vak", "studievereisten", "studieplanning", "rooster", "collegejaar", "studietijd",
        "zelfstudietijd", "onderwijsperiode", "studiehouding", "studielandschap", "studiestructuur",
        "examenreglement", "examencommissie", "studieaanpak", "studiebegeleidingsplan", "onderwijsvisie",
        "onderwijsfilosofie", "studentenzorg", "studietraject", "studiemethode", "onderwijsmethode",
        "studentenleven", "studentenwelzijn", "studentenactiviteiten", "studentensport", "studielasturen",
        "studiepuntensysteem", "studiejaar", "academische jaarindeling", "studie-uren", "zelfstudie-uren",
        "academische gemeenschap", "academische integriteit", "academische ondersteuning", "afstudeerproject",
        "anonieme cijfers", "begeleidingsgesprek", "bijles", "brochures", "campusfaciliteiten", "cijferlijst",
        "collegerooster", "communicatievaardigheden", "contacturen", "courseware", "curriculummodules",
        "curriculumvernieuwing", "didactiek", "digitale leeromgeving", "docententeam", "dyslexiebegeleiding",
        "e-learning", "educatieve programma's", "elektronische leeromgeving", "erasmusprogramma", "ethiek",
        "evaluatie", "evaluatierapport", "feedback", "formatief assessment", "gastcollege", "goede studiehouding",
        "groepsopdracht", "groepsproject", "herinschrijving", "huiswerkbegeleiding", "informatieavond",
        "inschrijfdeadline", "inschrijfgeld", "interactief onderwijs", "introweek", "kansengelijkheid",
        "kennistoets", "klas", "klasgenoten", "klaslokaal", "klassenmentor", "klasrooster", "leerdoelen",
        "leerstof", "lesmethodes", "lestijden", "mediatheek", "mobiele leeromgeving", "nieuwsbrief",
        "onderwijsbeleid", "onderwijsevaluatie", "onderwijskundige", "onderwijsmanagement", "onderwijsontwikkeling",
        "onderwijsondersteuning", "onderwijspersoneel", "onderwijsprestaties", "onderwijsprogramma",
        "onderwijssystemen",
        "onderwijstaken", "onderwijsuitvoering", "onderwijsvisie", "onderzoeksbegeleiding", "onderzoekscompetenties",
        "onderzoeksvaardigheden", "online onderwijs", "opfriscursus", "opleidingscommissie", "opleidingsprofiel",
        "praktijkonderwijs", "praktijkopdracht", "praktijkervaring", "projectbegeleiding", "projectonderwijs",
        "projectvaardigheden", "reflectieverslag", "resultaatgericht", "scriptietraject", "studieachterstand",
        "studiebegeleidingstraject", "studieboeken", "studiedag", "studiehouding", "studie-intensiteit",
        "studieplanning", "studiepuntentabel", "studievereniging", "studievoorlichting", "tentamencijfers",
        "tentamenresultaten", "theorie-examen", "toelatingsvoorwaarden", "toetsing", "verdiepingsmodule",
        "verplichte literatuur", "videolectures", "werkcolleges", "werkplekleren", "zelfstudieopdrachten"
    ]

    for keyword in keywords:
        if keyword.lower() in query.lower():
            return True
    return False


def build_prompt(question):
    # Construct the prompt with the chat history
    prompt = (
        "Je bent een behulpzame assistent die vragen beantwoordt over de Erasmus Hogeschool Brussel (EhB)."
        "Beantwoord alleen vragen die specifiek betrokken zijn met de erasmus hogeschool Brussel en zijn opleidingen."
        "Als de vraag niet relevant is aan de erasmus hogeschool Brussel en zijn opleidingen, geef dan aan dat de vraag niet relevant is"
        f"Vraag: {question}\nAntwoord: "
    )


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('HTTP trigger function received a request.')

    try:
        # Extract the question and chat history from the request
        request_data = req.get_json()
        question = request_data.get('question')

        if not question:
            return func.HttpResponse("Please pass a question in the request", status_code=400)

        # Check if the question is relevant
        if not is_relevant_query(question):
            return func.HttpResponse("This chatbot only answers questions about Erasmushogeschool Brussel.",
                                     status_code=400)

        # Perform prompt engineering by building the prompt with chat history
        prompt = build_prompt(question)

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

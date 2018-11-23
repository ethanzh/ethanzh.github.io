from api_key import API_KEY
import requests
from build import slice_text_to_array

# Grabs key from different file for privacy
key_add_on = "?key=" + API_KEY

SYNTAX_ENDPOINT = "https://language.googleapis.com/v1beta2/documents:analyzeSyntax" + key_add_on

ENTITIES_ENDPOINT = "https://language.googleapis.com/v1beta2/documents:analyzeEntities" + key_add_on

SENTIMENT_ENDPOINT = "https://language.googleapis.com/v1/documents:analyzeSentiment" + key_add_on

CLASSIFY_ENDPOINT = "https://language.googleapis.com/v1/documents:classifyText" + key_add_on

TRANSLATION_ENDPOINT = "https://translation.googleapis.com/language/translate/v2" + key_add_on

TRANSLATION_ENDPOINT += "&target=zh-CN&source=en&q="
NEW_TRANSLATION_ENDPOINT = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=zh-CN&dt=t&q="

json_data_template = {
    "document":
        {"type": "PLAIN_TEXT",
         "content":
             "null"}
}
def make_classify_request(body_text):
    current_json = json_data_template
    current_json["document"]["content"] = body_text

    classify_request = requests.post(url=CLASSIFY_ENDPOINT, json=current_json)
    classify_data = classify_request.json()

    categories_list = []

    try:
        for i in classify_data["categories"]:
            categories_list.append(i["name"])
    except KeyError:
        print("Error at", current_json["document"])

    return categories_list

def translate(text):
    # Works up to 4000, gets iffy above that. The higher, the better because it means fewer API calls
    char_limit = 4000

    # Simplest scenario, simply pass in the full text if it's under the char limit.
    if len(text) <= char_limit:

        # Puts text into 1 item array
        return make_translation_request([text])

    elif len(text) > char_limit:

        # Takes long text, turns it into an array of (roughly) evenly sizes slices
        text_array = slice_text_to_array(text, char_limit)

        # Calls Google API, returns text
        return make_translation_request(text_array)

def make_translation_request(text_list):
    # This accumulates all of the translated text
    total = ""

    for text in text_list:

        # Add text to endpoint, make request.
        # current_endpoint = TRANSLATION_ENDPOINT + text
        current_endpoint = NEW_TRANSLATION_ENDPOINT + text
        returned = requests.get(current_endpoint)

        try:
            returned_array = returned.json()[0]

            current_total = ""

            for i in range(len(returned_array)):
                current_total += returned_array[i][0]

        except ValueError:
            print('failed')

        status = returned.status_code

        if status != 200:
            print("Error code", status)

        # Extract just the text out of the JSON object
        total += current_total

    total = total.replace("\r", "")
    total = total.replace("\n", "")

    return total
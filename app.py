from flask import Flask, request, jsonify
from flask.helpers import send_from_directory
from flask_cors import CORS, cross_origin
import requests
import uuid
# from scraper import scrape_webpage
from test_scraper import scrape_website
from text_summarizer import summarizer

app = Flask(__name__, static_folder='Frontend-main/build', static_url_path='')
CORS(app)


@app.route('/')
@cross_origin()
def home():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/scrape', methods=['GET'])
@cross_origin()
def scrape():
    url = request.args.get('url')
    content = scrape_website(url)
    if content:
        return jsonify(content)
    else:
        return jsonify({"error": "Failed to scrape the webpage."}), 500


@app.route('/translator', methods=['POST'])
@cross_origin()
def translate():
    data = request.json  # Get JSON data from the request body
    original_text = data.get('text')  # Get the 'text' field from the JSON data
    # Get the 'language' field from the JSON data
    target_language = data.get('language')

    print(f"Received request with text: {original_text}")
    print(f"Received request with language: {target_language}")

    # API request
    key = 'ca8b4df91a0f45cba47974735d4452e9'
    endpoint = 'https://api.cognitive.microsofttranslator.com/'
    location = 'southeastasia'

    # Indicate that we want to translate and the API version (3.0) and the target language
    path = '/translate?api-version=3.0'
    # Add the target language parameter
    target_language_parameter = '&to=' + target_language
    # Create the full URL
    constructed_url = endpoint + path + target_language_parameter

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Create the body of the request with the text to be translated
    body = [{'text': original_text}]

    # Make the call using post
    translator_request = requests.post(
        constructed_url, headers=headers, json=body)
    # Retrieve the JSON response
    translator_response = translator_request.json()
    # Retrieve the translation
    translated_text = translator_response[0]['translations'][0]['text']

    return jsonify({
        "translated_text": translated_text,
        "original_text": original_text,
        "target_language": target_language
    })


@app.route('/summarize', methods=['POST'])
@cross_origin()
def summarize():
    data = request.json  # Get JSON data from the request body
    rawtext = data.get('text')  # Get the 'text' field from the JSON data

    if request.method == 'POST':
        summary, original_text, len_original_text, len_summary = summarizer(
            rawtext)

        return jsonify({
            "summarized_text": summary,
            "original_text": rawtext,
            "len_original_text": len_original_text,
            "len_summary": len_summary
        })

    return jsonify({"summarized_text": rawtext})


if __name__ == '__main__':
    app.run(debug=True)

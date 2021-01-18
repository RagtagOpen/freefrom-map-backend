from dotenv import load_dotenv
import json
import os
import requests

load_dotenv()


def post_google(data):
    headers = {'Content-Type': 'application/json'}
    google_id = os.environ['GOOGLE_DEPLOYMENT_ID']
    if not google_id:
        raise Exception
    response = requests.post(
        f'https://script.google.com/macros/s/{google_id}/exec',
        json=data,
        headers=headers,
    )
    json_response = json.loads(response.text)
    return json_response

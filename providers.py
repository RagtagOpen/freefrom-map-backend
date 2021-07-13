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


def get_categories_from_cms():
    response = requests.get('http://freefrom-cms.nitro/categories.json?cache=false')
    json_response = json.loads(response.text)
    return json_response['data']


def get_states_from_cms():
    response = requests.get('http://freefrom-cms.nitro/states.json?cache=false')
    json_response = json.loads(response.text)
    return json_response['data']

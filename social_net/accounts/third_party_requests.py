import requests

import clearbit

from django.conf import settings


def verify_email(email):
    payload = {
        'api_key': settings.HUNTER_SECRET_KEY,
        'email': email,
    }
    res = requests.get('https://api.hunter.io/v2/email-verifier', params=payload)
    res = res.json()['data']
    if res['result'].lower() != 'undeliverable':
        return True
    return False


def fetch_data_on_email(email):
    clearbit.key = settings.CLEARBIT_SECRET_KEY
    res = clearbit.Enrichment.find(email=email, stream=True)
    person = res['person']
    data = {
        'first_name': person['name']['givenName'],
        'last_name': person['name']['familyName'],
    }
    return data

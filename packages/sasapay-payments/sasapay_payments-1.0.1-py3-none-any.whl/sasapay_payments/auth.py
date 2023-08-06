import requests
from requests.auth import HTTPBasicAuth


def generate_token(client_id, client_secret, environment='SANDBOX'):
    try:
        if environment == 'SANDBOX':
            token_endpoint = 'https://sandbox.sasapay.app/api/v1/auth/token/?grant_type=client_credentials'
        elif environment == 'PRODUCTION':
            token_endpoint = 'https://api.sasapay.app/api/v1/auth/token/?grant_type=client_credentials'
        else:
            return {'status': False, 'detail': 'Provide valid environment to generate token'}
        params = {'grant_type': 'client_credentials'}
        response = requests.get(token_endpoint,
                                auth=HTTPBasicAuth(client_id, client_secret), params=params, verify=False)
        return response.text
    except Exception as error:
        # print('TOKEN ERROR:', str(error))
        return {'status': False, 'detail': 'Error generating access token'}

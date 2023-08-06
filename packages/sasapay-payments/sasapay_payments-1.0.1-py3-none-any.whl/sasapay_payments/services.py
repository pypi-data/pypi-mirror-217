import requests

def make_get_api_request(url,payload,access_token):

    headers ={
        'Authorization':f'Bearer {access_token}',
        'Content-Type':'application/json'
    }
    response = requests.get(url, json=payload, headers=headers)
    return response.text

def make_post_api_request(url,payload,access_token):
    headers ={
        'Authorization':f'Bearer {access_token}',
        'Content-Type':'application/json'
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.text


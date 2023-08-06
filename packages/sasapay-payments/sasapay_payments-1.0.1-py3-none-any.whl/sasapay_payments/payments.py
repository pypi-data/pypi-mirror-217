
from services import make_post_api_request


sasapay_base_url = 'https://api.sasapay.app/api/v1'


def customer_to_business(payload, access_token):
    url = f'{sasapay_base_url}/payments/request-payment/'
    response = make_post_api_request(
        url=url, payload=payload, access_token=access_token)
    return response


def process_payment(payload, access_token):
    url = f'{sasapay_base_url}/payments/process-payment/'
    response = make_post_api_request(
        url=url, payload=payload, access_token=access_token)
    return response


def business_to_customer(payload, access_token):
    url = f'{sasapay_base_url}/payments/b2c/'
    response = make_post_api_request(
        url=url, payload=payload, access_token=access_token)
    return response


def business_to_business(payload, access_token):
    url = f'{sasapay_base_url}/payments/b2b/'
    response = make_post_api_request(
        url=url, payload=payload, access_token=access_token)
    return response


def transaction_status(payload, access_token):
    url = f'{sasapay_base_url}/transactions/status/'
    response = make_post_api_request(
        url=url, payload=payload, access_token=access_token)
    return response


def account_validation(payload, access_token):
    url = f'{sasapay_base_url}/accounts/account-validation/'
    response = make_post_api_request(
        url=url, payload=payload, access_token=access_token)
    return response

import requests

def send_to_erp(data, api_url, token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    try:
        response = requests.post(api_url, json=data, headers=headers)
        return response.status_code, response.text
    except Exception as e:
        return 500, str(e)

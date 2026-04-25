import requests

BASE_URL = "http://127.0.0.1/api/hospital"


def api_get(module, params=None):
    url = f"{BASE_URL}/{module}/get.php"
    response = requests.get(url, params=params)

    try:
        return response.json()
    except:
        print("GET API ERROR:")
        print(response.text)
        return {}


def api_insert(module, data):
    url = f"{BASE_URL}/{module}/insert.php"
    response = requests.post(url, json=data)

    try:
        return response.json()
    except:
        print("INSERT API ERROR:")
        print(response.text)
        return {}


def api_delete(module, data):
    url = f"{BASE_URL}/{module}/delete.php"
    response = requests.post(url, json=data)

    try:
        return response.json()
    except:
        print("DELETE API ERROR:")
        print(response.text)
        return {}


def api_update_full(module, data):
    url = f"{BASE_URL}/{module}/updatefull.php"
    response = requests.post(url, json=data)

    try:
        return response.json()
    except:
        print("UPDATE FULL API ERROR:")
        print(response.text)
        return {}


def api_update_partial(module, data):
    url = f"{BASE_URL}/{module}/updatepartial.php"
    response = requests.post(url, json=data)

    try:
        return response.json()
    except:
        print("UPDATE PARTIAL API ERROR:")
        print(response.text)
        return {}
"""Basic API checks. Start app.py first, then run: python test_api.py"""

import requests

BASE_URL = "http://127.0.0.1:5000"

endpoints = [
    "/",
    "/campaigns",
    "/campaigns/failed",
    "/reports/summary",
    "/reports/channel",
    "/campaigns/102",
    "/campaigns/999",
    "/campaigns/0",
]

for endpoint in endpoints:
    try:
        response = requests.get(BASE_URL + endpoint, timeout=5)
        print(f"{endpoint:24} -> HTTP {response.status_code}")
    except requests.RequestException as error:
        print(f"{endpoint:24} -> Request failed: {error}")

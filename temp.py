import requests

endpoint = "http://127.0.0.1:1234/attendance"

response = requests.get(endpoint, params={"department": "BCA", "year": "Fy"})

print(response.text)

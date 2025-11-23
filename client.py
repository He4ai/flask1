import requests

response = requests.get(
    "http://127.0.0.1:5000/api/v1/announcements")

print(response.status_code)
print(response.text)

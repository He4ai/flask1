import requests

response = requests.get(
    "http://127.0.0.1:5000/api/v1/announcements/1",
)

print(response.status_code)
print(response.text)

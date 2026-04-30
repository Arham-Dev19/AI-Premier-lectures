import requests

url = "https://mizaajrestaurant.com/"
response = requests.get(url)

print(response.status_code)
print(response.text)
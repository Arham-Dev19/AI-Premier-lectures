import requests

url = "https://jsonplaceholder.typicode.com/users"
response = requests.get(url)

print(response.status_code)
print(type(response.json()))

data = response.json()

print(data[0]["name"])
print(data[0]["email"])
print(data[0]["phone"])
print(data[0]["address"])
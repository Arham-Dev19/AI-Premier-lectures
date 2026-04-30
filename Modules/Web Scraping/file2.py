from bs4 import BeautifulSoup
import requests

url = "https://mizaajrestaurant.com/"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

# heading = soup.find('h1')
# print(heading.text)

# para = soup.find_all("p")
# for p in para:
#     print(p.text)

# data = soup.find("div", class_="elementor-widget-container")
# print(data)  


# links = soup.find_all("a")
# for link in links:
#     print(link.get("href"))
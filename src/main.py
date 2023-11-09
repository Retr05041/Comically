import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup

main_url = "https://viewcomics.org/"

response = requests.get(main_url)
soup = BeautifulSoup(response.text, 'html.parser')

for link in soup.find_all('a'):
    print(link.get('href'))
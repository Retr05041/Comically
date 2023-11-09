import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup

class Site:
    def __init__(self, url):
        self.url = url

    def searchForComic(self, comicName):
        potentialComics = []
        print("Searching for comic: " + comicName)
        print(self.url + "/comic-list?c=" + comicName[0])
        getPage = requests.get(self.url + "/comic-list?c=" + comicName[0])
        soupPage = BeautifulSoup(getPage.text, 'html.parser')

        for comic in soupPage.find_all('a', class_='big-link'):
            if comicName.lower() in comic.text.lower():
                potentialComics.append([comic.text, comic['href']])
            elif comicName.lower().replace(" ", "-") in comic['href'].lower():
                potentialComics.append([comic.text, comic['href']])
            else:
                pass
        
        if len(potentialComics) > 1:
            print("Found multiple comics with that name, please select one:")
            for i in range(1, len(potentialComics)):
                print(str(i) + ". " + potentialComics[i][0])
            comicSelection = input("Comic Selection: ")
            print(potentialComics[int(comicSelection)][1])
        elif len(potentialComics) == 1:
            print("Found one comic with that name: " + potentialComics[0][0] + " - " + potentialComics[0][1])
        else:
            print("No comics found with that name")
            return None

    
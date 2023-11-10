import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup

class Site:
    def __init__(self, url, comicListURL=None, idTag=None, cssClass=None, pagingURL=None):
        self.url = url
        self.comicListURL = comicListURL
        self.idTag = idTag
        self.cssClass = cssClass
        self.pagingURL = pagingURL

        self.fullURL = self.url + self.comicListURL

    def searchForComic(self, comicName):
        """
        Searches for a comic with the given name on the website.
        
        Args:
        - comicName (str): The name of the comic to search for.
        
        Returns:
        - None if no comics are found, otherwise:
        - A list containing the name and URL of the comic if only one is found.
        - The URL of the selected comic if multiple comics are found.
        """
        potentialComics = []

        # Check if the site has a paging system
        if self.pagingURL != None:
            print("Searching for comic: " + comicName)
            print(self.fullURL + comicName[0] + self.pagingURL + "1")
            getPage = requests.get(self.fullURL + comicName[0] + self.pagingURL + "1")
            soupPage = BeautifulSoup(getPage.text, 'html.parser')
        else:
            print("Searching for comic: " + comicName)
            print(self.url + self.comicListURL + comicName[0])
            getPage = requests.get(self.url + self.comicListURL + comicName[0])
            soupPage = BeautifulSoup(getPage.text, 'html.parser')

        # Find final page number
        finalPage = 1
        currentPage = 1
        if self.pagingURL != None:
            while True:
                for pageLink in soupPage.find_all('a'):
                    if "next" in pageLink.text.lower():
                        finalPage = int(pageLink['href'].split("=")[1])
                        getPage = requests.get(self.fullURL + comicName[0] + self.pagingURL + str(finalPage))
                        soupPage = BeautifulSoup(getPage.text, 'html.parser')
                currentPage += 1
                if currentPage == finalPage:
                    continue
                break
        
        print("There are " + str(finalPage) + " pages")

        # Loop through pages
        for page in range(1, finalPage + 1):
            if self.pagingURL != None:
                print("Searching page: " + str(page))
                getPage = requests.get(self.fullURL + comicName[0] + self.pagingURL + str(page))
                soupPage = BeautifulSoup(getPage.text, 'html.parser')
            else:
                getPage = requests.get(self.url + self.comicListURL + comicName[0])
                soupPage = BeautifulSoup(getPage.text, 'html.parser')

            # Find comics on page
            for comic in soupPage.find_all(self.idTag, class_=self.cssClass):
                # print(comic.text)
                if (comicName.lower() in comic.text.lower()) or (comicName.lower().replace(" ", "-") in comic.text.lower()):
                    potentialComics.append([comic.text, comic['href']])
                else:
                    pass

        print(potentialComics)
        
        # Display comics / select comic
        if len(potentialComics) > 1:
            print("Found multiple comics with that name, please select one:")
            for i in range(1, len(potentialComics)):
                print(str(i) + ". " + potentialComics[i][0])
            comicSelection = input("Comic Selection: ")
            if self.url in potentialComics[int(comicSelection)][1]:
                print(potentialComics[int(comicSelection)][1])
            else:
                print(self.url + potentialComics[int(comicSelection)][1])
        elif len(potentialComics) == 1:
            if self.url in potentialComics[0][1]:
                print("Found one comic with that name: " + potentialComics[0][0] + " - " + potentialComics[0][1])
            else:
                print("Found one comic with that name: " + potentialComics[0][0] + " - " + self.url + potentialComics[0][1])
        else:
            print("No comics found with that name")
            return None

    
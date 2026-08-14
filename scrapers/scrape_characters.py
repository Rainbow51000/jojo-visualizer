import requests, time, re
from bs4 import BeautifulSoup
from pathlib import Path
from models import Character
from serialization import dataclasses_to_csv

BASE_URL = "https://jojowiki.com"
URL_P1 = "https://jojowiki.com/Category:Part_1_Characters"
DATA_PATH = Path(__file__).parent / '..' / 'data'
DATA_FILENAME = 'characters.csv'

def getCharacters() -> list[Character]:
    characters: list[Character] = []
    response = requests.get(URL_P1)

    if response.status_code != 200:
        print(f"Erreur lors de la requête initiale : {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    # characters table
    soup = soup.find("div", class_="cbox")
    # list of characters
    soup = soup.find_all("div", class_="charbox diamond resizeImg")

    # every links of characters
    for character in soup:
        # request for each characters, fetching their entity
        subpath = character.find("a")["href"]
        char = getCharacter(subpath)
        characters.append(char)

        time.sleep(0.5)

    return characters

def getCharacter(subpath: str) -> Character:
    responseCharacter = requests.get(BASE_URL + subpath)
    if responseCharacter.status_code != 200:
        print(f"Erreur lors de la requête de personnage : {response.status_code}")
    
    soup = BeautifulSoup(responseCharacter.text, "html.parser")
    
    # extracting data
    name = soup.find("h2", class_="pi-item pi-item-spacing pi-title").text
    chapters = []
    chaptersRaw = soup.find("div", class_="appearanceBox3 textarea")
    chaptersRaw = chaptersRaw.find_all("a")
    for chapter in chaptersRaw:
        txt = chapter["title"]
        # search chapters (only! not anime or ova) appearing and add to list
        try:
            number = re.search("^Chapter\s+(\d+)", txt).group(1)
            chapters.append(number)
        except:
            pass
    
    return Character(name, chapters)

if __name__ == "__main__":
    characters = getCharacters()
    dataclasses_to_csv(characters, DATA_PATH, DATA_FILENAME)
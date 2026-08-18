import requests, time, re, urllib.parse
from bs4 import BeautifulSoup, Tag
from pathlib import Path
from models import Character
from serialization import dataclasses_to_csv

BASE_URL = "https://jojowiki.com"
DATA_PATH = Path(__file__).parent / '..' / 'data'
DATA_FILENAME = 'characters.csv'
URL_PARTS = [
    "https://jojowiki.com/Category:Part_1_Characters",
    "https://jojowiki.com/Category:Part_2_Characters",
    "https://jojowiki.com/Category:Part_3_Characters",
    "https://jojowiki.com/Category:Part_4_Characters",
    "https://jojowiki.com/Category:Part_5_Characters",
    "https://jojowiki.com/Category:Part_6_Characters",
    "https://jojowiki.com/Category:Part_7_Characters",
    "https://jojowiki.com/Category:Part_8_Characters",
    "https://jojowiki.com/Category:Part_9_Characters"
]

def getCharacters(url_parts: list[str]) -> list[Character]:
    subpaths: list[str] = []
    
    for url in url_parts:
        print(f"Getting part {url[35]} characters...")
        subpaths += getCharactersLinks(url)
        print(f"Part {url[35]} completed.")
        time.sleep(0.5)
    
    # Dio_brando and DIO link to the same page, it's useless to keep 2 of them as they will duplicate.
    subpaths.remove("/DIO")
    subpaths = list(set(subpaths))
    characters: list[Character] = []

    for subpath in subpaths:
        print(f"Scraping info on {subpath}")
        characters.append(getCharacter(subpath))
        time.sleep(0.5)
    
    return characters

def getCharactersLinks(url: str) -> list[str]:
    subpaths: list[str] = []
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error during initial request : {response.status_code}")

    charactersLinkSoup = BeautifulSoup(response.text, "html.parser").find("div", class_="cbox").find_all("div", class_="charbox diamond resizeImg")

    for character in charactersLinkSoup:
        subpath = character.find("a")["href"]
        subpaths.append(subpath)
        time.sleep(0.5)

    return subpaths

def getCharacter(subpath: str) -> Character:
    responseCharacter = requests.get(BASE_URL + subpath)
    if responseCharacter.status_code != 200:
        print(f"Error during the request of the specific character at {subpath} : {response.status_code}")
    
    soup = BeautifulSoup(responseCharacter.text, "html.parser")

    name = getCharacterName(subpath)
    chapters = getCharacterChapters(soup)
    
    return Character(name, chapters)

def getCharacterName(subpath: str) -> str:
    return urllib.parse.unquote(subpath.replace("/", "").replace("_", " ").replace("%27", "'").replace("%22", "\""))

def getCharacterChapters(soup: BeautifulSoup) -> list[str]:
    chapters = []

    try:
        chaptersRaw = soup.find("div", class_="appearanceBox3 textarea").find_all("a")
    except:
        return []

    for chapter in chaptersRaw:
        txt = chapter["title"]
        try:
            regex = re.search('^(?:(SO|SBR|JJL|TJL)\s+)?Chapter\s+(\d+)$', txt)
            part = None
            if regex.group(1):
                part = regex.group(1)
            chapter = regex.group(2)
            chapter = getChapterFormatted(part, chapter)
            chapters.append(chapter)
        except:
            pass
    
    return chapters

def getChapterFormatted(part:str|None, chapter: str):
    """
    Format chapter from part 1-5 according to this format :
    "X-YYY" where X is the part number and YYY the chapter number.
    For example, chapter "374" is part 4, chapter 109.
    According to the format, it translates to "4-109".

    This is used because Jojo's Wiki has a different format chapters number from part 1-5 compared to 6-9,
    for example in part 6 it's "Stone Ocean Chapter 4", which could be confused with Part 1 Chapter 4 if
    we took the number literally.
    """
    PART_TRANSLATOR = {
        "SO":6,
        "SBR":7,
        "JJL":8,
        "TJL":9
    }

    if part != None:
        return f"{PART_TRANSLATOR[part]}-{chapter}"

    FIRST_FIVE_PARTS_END_CHAPTERS = [44, 113, 265, 439, 594]

    for part in range(len(FIRST_FIVE_PARTS_END_CHAPTERS)):
        if int(chapter) <= FIRST_FIVE_PARTS_END_CHAPTERS[part]:
            if part == 0:
                return f"{part + 1}-{chapter}"
            else:
                return f"{part + 1}-{int(chapter) - FIRST_FIVE_PARTS_END_CHAPTERS[part-1]}"
    
    print(f"Error during chapter format, it was not recognised, which will be translated to number -1. Number of the chapter that should be formatted : {chapter}")
    return -1

if __name__ == "__main__":
    characters = getCharacters(URL_PARTS)
    dataclasses_to_csv(characters, DATA_PATH, DATA_FILENAME)
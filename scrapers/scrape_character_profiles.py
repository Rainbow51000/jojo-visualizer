import requests, time
from sanitize_filename import sanitize
from bs4 import BeautifulSoup
from pathlib import Path
from utils.character import getCharacterName

BASE_URL = "https://jojowiki.com"
OUTPUT_PATH = Path(__file__).parent / '..' / 'data' / 'character_profiles'
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

def downloadCharactersImage(output_path: Path, url_parts: list[str]) -> None:
    for url in url_parts:
        print(f"Getting profiles from part {url[35]} characters...")
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Error during initial request : {response.status_code}")
        
        characters = BeautifulSoup(response.text, "html.parser").find("div", class_="cbox").find_all("div", class_="charbox diamond resizeImg")
        
        for character in characters:
            filename = sanitize(getCharacterName(character.find("a")["href"]) + ".jpg")
            img_url = character.find_all("img")[-1]["src"]

            img_response = requests.get(img_url)
            img_response.raise_for_status()

            with open(output_path / filename, "wb") as f:
                f.write(img_response.content)
            time.sleep(0.5)
            
        print(f"Profiles of part {url[35]} completed.")
        time.sleep(0.5)

if __name__ == "__main__":
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    for file in OUTPUT_PATH.iterdir():
        if file.is_file:
            file.unlink()
    downloadCharactersImage(OUTPUT_PATH, URL_PARTS)
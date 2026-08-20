import urllib.parse

def getCharacterName(subpath: str) -> str:
    return urllib.parse.unquote(subpath.replace("/", "").replace("_", " "))
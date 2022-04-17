import subprocess
import os
import requests
from bs4 import BeautifulSoup


def func90Title(videoID):
    outputDir = "output"
    fileExt = "mp3"

    urlOfVideo = f"https://www.youtube.com/watch?v={videoID}"
    requestOfYoutubeWebpage = requests.get(urlOfVideo)
    soupOfYoutubeWebpage = BeautifulSoup(requestOfYoutubeWebpage.text, 'html.parser')
    actualWebpageTitle = ""

    for title in soupOfYoutubeWebpage.find_all('title'):
        actualWebpageTitle = title.get_text()
    
    titleOneline = actualWebpageTitle
    

    disallowedCharacters = "._?*><:\"|\\|/"
    for disallowedCharacter in disallowedCharacters:
        titleOneline = titleOneline.replace(disallowedCharacter, "")

    previousFilename = f"{outputDir}\\{videoID}.{fileExt}"
    newFilename = f"{titleOneline}.{fileExt}"


    commandToRename = f"ren \"{previousFilename}\" \"{newFilename}\""

    os.system(commandToRename)
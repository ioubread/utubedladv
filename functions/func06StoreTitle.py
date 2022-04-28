# from youtubelist import allitems

# import os
import requests
from bs4 import BeautifulSoup
import shelve
from pathlib import Path
import os

# allVideos = allitems.split("\n")

def func06StoreTitle(videoID):
    # print(Path.cwd())
    originalDir = Path.cwd()
    outputDir = "output"
    dataDir = "data"
    fileExt = "mp3"
    shelfName = "titleData"

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
    
    if titleOneline.endswith(" - YouTube"):
        titleOneline = titleOneline[:-10]
        # print(titleOneline)

    # titleOneline = titleOneline.rstrip(" - YouTube")

    if len((titleOneline).strip()) == 0:
        titleOneline = videoID


    # previousFilename = f"{outputDir}\\{videoID}.{fileExt}"
    newFilename = f"{titleOneline}.{fileExt}"


    # Hardcoded
    # previousFilename = "dummy.mp3"

    # os.rename(previousFilename, newFilename)
    # os.rename(newFilename, previousFilename)

    os.chdir(dataDir)

    myShelf = shelve.open(shelfName)
    myShelf[videoID] = newFilename
    myShelf.close()

    os.chdir(originalDir)

#     print(titleOneline)


# for videoID in allVideos:
#     func90Title(videoID)
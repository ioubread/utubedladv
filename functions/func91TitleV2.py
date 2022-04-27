import os
import shelve
from pathlib import Path

def func91TitleV2(videoID):

    originalDir = Path.cwd()

    dataDir = "data"
    outputDir = "output"
    fileExt = "mp3"
    shelfName = "titleData"

    os.chdir(dataDir)
    myShelf = shelve.open(shelfName)


    storedTitle = myShelf[videoID]

    previousFilename = f"..\\{outputDir}\\{videoID}.{fileExt}"
    newFilename = f"..\\{outputDir}\\{storedTitle}"

    os.rename(previousFilename, newFilename)

    myShelf.close()
    os.chdir(originalDir)
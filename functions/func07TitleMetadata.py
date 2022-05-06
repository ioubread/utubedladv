import os
import shelve
import eyed3
from pathlib import Path

def func07TitleMetadata(videoID):
    originalDir = Path.cwd()
    fileExtension = "mp3"
    shelfName = "titleData"
    dataDir = "data"
    fileBasename = videoID
    filename = f"{fileBasename}.{fileExtension}"
    outputDir = "output"

    os.chdir(dataDir)

    myShelf = shelve.open(shelfName)

    try:
        storedTitle = myShelf[videoID]
    
    except KeyError:
        return
    
    myShelf.close()
    os.chdir("..")

    musicFileTagged = eyed3.load(f"{outputDir}/{filename}")
    musicFileTagged.tag.title = storedTitle
    musicFileTagged.tag.save()

    
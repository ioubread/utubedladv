import os
import shelve

# Program initialization
print("Please ensure that the playlist is UNLISTED/PUBLIC")
playlistLinkInput = input("Input youtube playlist link: ")

if "playlist?" not in playlistLinkInput:
    playlistID = playlistLinkInput
else:
    playlistID = (playlistLinkInput.partition("playlist?list="))[2]

os.chdir(playlistID)


# Data declaration
dataDir = "data"
outputDir = "output"
fileExt = "mp3"
shelfName = "titleData"
outlineName = "outline.txt"



# Main program starts here
os.chdir(dataDir)


# Digesting outline file
outlineFile = open(outlineName, "r")
outlineContents = outlineFile.read()
outlineFile.close()
outlineSplitted = outlineContents.split("\n")



# Looping through data in outline
for videoID in outlineSplitted:
    duplicateCount = 0

    # Obtaining Title information from func06StoreTitle
    myShelf = shelve.open(shelfName)
    try:
        storedTitle = myShelf[videoID]
    
    except KeyError:
        continue

    # Renaming
    previousFilename = f"..\\{outputDir}\\{videoID}.{fileExt}"
    newFilename = f"..\\{outputDir}\\{storedTitle}"

    try:
        os.rename(previousFilename, newFilename)
    except FileExistsError:

        managedToRename = False

        while managedToRename == False:
            duplicateCount += 1
            newFilename = f"..\\{outputDir}\\{storedTitle[:-4]} ({str(duplicateCount)}).{fileExt}"

            try:
                os.rename(previousFilename, newFilename)
                managedToRename = True
                break
            except FileExistsError:
                continue

        

    # Printing output
    print(f"[{videoID}]: {storedTitle}")

    # Done
    del myShelf[videoID]
    myShelf.close()
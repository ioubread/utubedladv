import os
import sys
from PIL import Image
import shutil
import time

def func03Thumbnail(videoID):

    pathToMP3 = f"output/{videoID}.mp3"
    idealFormat = "png"
    thumbnailDirectory = "temp"

    startOfLink = "https://www.youtube.com/watch?v="

    allItemsInTemp = os.listdir(thumbnailDirectory)

    for item in allItemsInTemp:
        pathToItem = thumbnailDirectory + "/" + item
        os.unlink(pathToItem)

    commandToDownloadThumbnail = f"youtube-dl -q -i -o \"temp/thumbnail.%(ext)s\" {startOfLink + videoID} --skip-download --write-thumbnail"
    os.system(commandToDownloadThumbnail)

    allItemsInTempAfterPurge = os.listdir(thumbnailDirectory)

    if len(allItemsInTempAfterPurge) > 1:
        sys.exit()

    pathToThumbnail = thumbnailDirectory + "/" + allItemsInTempAfterPurge[0]
    pathToIdealThumbnail = thumbnailDirectory + "/" + "thumbnail" + "." + idealFormat
    pathToCroppedThumbnail = thumbnailDirectory + "/" + "thumbnail_cropped" + "." + idealFormat

    original = Image.open(pathToThumbnail)
    original.save(pathToIdealThumbnail, format=idealFormat)
    original.close()

    

    image = Image.open(pathToIdealThumbnail)
    width, height = image.size

    theSmallerDimension = ""
    if width > height:
        theSmallerDimension = "height"
    elif height > width:
        theSmallerDimension = "width"
    elif width == height:
        theSmallerDimension = "equal"
    else:
        pass

    if theSmallerDimension == "equal":
        shutil.copyfile(pathToIdealThumbnail, pathToCroppedThumbnail)
    
    else:
        if theSmallerDimension == "height":
            theDifference = width - height
            theMargin = int(theDifference / 2)

            point1 = (theMargin, 0)
            point2 = (theMargin + height, height)

        elif theSmallerDimension == "width":
            theDifference = height - width
            theMargin = int(theDifference / 2)

            point1 = (0, theMargin)
            point2 = (width, theMargin + width)
        
        value1, value2 = point1
        value3, value4 = point2
        imageCropped = image.crop((value1, value2, value3, value4))

        imageCropped.save(pathToCroppedThumbnail)

    

    ffmpegCommand = f"ffmpeg -nostats -loglevel 0 -i {pathToMP3} -i {pathToCroppedThumbnail} -c:a copy -c:v copy -map 0:0 -map 1:0 -id3v2_version 3 -metadata:s:v title=\"Album cover\" -metadata:s:v comment=\"Cover (front)\" temp/out.mp3"
    # ffmpegCommand = f"ffmpeg -i {pathToMP3} -i {pathToCroppedThumbnail} -c:a copy -c:v copy -map 0:0 -map 1:0 -id3v2_version 3 -metadata:s:v title=\"Album cover\" -metadata:s:v comment=\"Cover (front)\" temp/out.mp3"
    os.system(ffmpegCommand)

    time.sleep(2)

    shutil.move("temp/out.mp3", pathToMP3)

    os.unlink(pathToIdealThumbnail)
    os.unlink(pathToThumbnail)
    os.unlink(pathToCroppedThumbnail)
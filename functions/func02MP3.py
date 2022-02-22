import os
from pydub import AudioSegment
# from pathlib import Path
# import time
import sys

# from classes import *
import functions.classes as classes

# class Error(Exception):
#     pass

# class TargetNotFound(Error):
#     pass



def func02MP3(videoID):

    # print("starting function 2")
    
    targetFileFormat = "mp3"
    getfromDirectory = "output"

    filesInOutput = os.listdir(getfromDirectory)

    targetFilenames = []

    for checkingThisFile in filesInOutput:
        if checkingThisFile.startswith(videoID):
            targetFilenames.append(checkingThisFile)
            # targetFilename = checkingThisFile
            # print(f"WELP it found someone that starts with {videoID}")
    
    if len(targetFilenames) == 0:
        # print("length of targetfilenames is 0")
        # raise TargetNotFound("Target not found, LOL")

        # print("LOL no targets lei")

        raise classes.TargetNotFound

        # sys.exit()
    elif len(targetFilenames) > 1:

        for checkingThisTarget in targetFilenames:
            if checkingThisTarget.endswith(targetFileFormat):
                targetFilenames.remove(checkingThisTarget)
            
        
        if not len(targetFilenames) == 1:
            # print("length of targetfilenames is still not 1")
            # raise "StillNotFound"
            # sys.exit()
            # raise TargetNotFound

            if len(targetFilenames) == 0:
                raise classes.TargetNotFound
            
            else:
                sys.exit()

    targetFilename = targetFilenames[0]
    
    # time.sleep(100)
    
    pathToUnconvertedFile = getfromDirectory + "/" + targetFilename
    idealFilename = videoID + "." + targetFileFormat
    pathToIdealFile = getfromDirectory + "/" + idealFilename

    AudioSegment.from_file(pathToUnconvertedFile).export(pathToIdealFile, format=targetFileFormat)

    os.unlink(pathToUnconvertedFile)
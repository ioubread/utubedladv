from email import message
import os
import importlib
from halo import Halo
import subprocess
from alive_progress import alive_bar
from alive_progress import styles
import copy
import sys
import time
from pathlib import Path

from functions import classes

def constructMessage(videoID, bodyMessage, paddingLength, preBlankPadding, endingMessage):
    messageToReturn = f"{videoID}: {str(bodyMessage)}"
    paddingLengthAccountingEndingMessage = int(paddingLength) - len(str(endingMessage))
    messageToReturn = messageToReturn.ljust(paddingLengthAccountingEndingMessage, ".")
    messageToReturn = messageToReturn + endingMessage
    messageToReturn = f"[{messageToReturn}]"
    messageToReturn = preBlankPadding + messageToReturn

    return messageToReturn




# Creating spinner object
spinner = Halo("Getting playlist items", spinner="dots")


# Declaring directory to functions
directoryToFunctions = "functions"


# Declaring folders in each playlist folder
foldersInPlaylistFolder = ["temp", "data", "output"]
paddingLength = 100
gentleSleepTime = 3



# Getting all the functions
allFunctions = os.listdir(directoryToFunctions)

allFunctions_temp = []




for thisFunction in allFunctions:
    if thisFunction.startswith("func"):
        allFunctions_temp.append(thisFunction)

allFunctions = allFunctions_temp

# print(allFunctions)


allFunctionsWithoutExtensions = []



validLengthOfYoutubeIDs = 11

# Working with the functions to get the list of clean functions
for singleFunction in allFunctions:
    reversedName = singleFunction[::-1]
    reversedNameWithoutExtension = (reversedName.partition("."))[2]
    singleFunctionNameWithoutExtension = reversedNameWithoutExtension[::-1]
    allFunctionsWithoutExtensions.append(singleFunctionNameWithoutExtension)

allFunctionsWithoutExtensionsv2 = []
for singleFunction in allFunctionsWithoutExtensions:
    if not singleFunction == "":
        allFunctionsWithoutExtensionsv2.append(singleFunction)


# Importing the functions
for singleFunction in allFunctionsWithoutExtensionsv2:
    globals()[singleFunction] = importlib.import_module(directoryToFunctions + "." + singleFunction)


# Declaring final variable of the list of functions
listOfFunctions = allFunctionsWithoutExtensionsv2

print("Please ensure that the playlist is UNLISTED/PUBLIC")
playlistLinkInput = input("Input youtube playlist link: ")

if "playlist?" not in playlistLinkInput:
    playlistID = playlistLinkInput
else:
    playlistID = (playlistLinkInput.partition("playlist?list="))[2]


# print("the playlist is")
# print(playlistID)

# Checking whether folder for playlist has been created before
thisDirectory = os.listdir(".")

if playlistID in thisDirectory:
    folderExists = True
else:
    folderExists = False


directoryToOutput = playlistID + "/output"
directoryToData = playlistID + "/data"
pathToOutline = directoryToData + "/outline.txt"
pathToProgress = directoryToData + "/progress.txt"

if folderExists:
    itemsInFolder = os.listdir(directoryToOutput)
    
    # Deleting all PART files
    for item in itemsInFolder:
        extensionOfItem = (item.split("."))[-1]

        if extensionOfItem == "part":
            os.unlink(directoryToOutput + "/" + item)
   

    playlistHasChanged = input("Enter 'y' if the playlist has changed: ")


    if playlistHasChanged == "y":

        # Crafting the command to prompt for video IDs
        commandStimulateID = f"youtube-dl -i --get-id {playlistID}"

        commandShattered = commandStimulateID.split(" ")
        

        # Getting the IDs
        spinner.start()
        # outputStimulateID = subprocess.check_output(commandStimulateID, shell=True, text=True)
        outputStimulateID = subprocess.run(commandShattered, capture_output=True)
        spinner.stop_and_persist()

        outputStimulateID = outputStimulateID.stdout.decode("utf-8")

        outputStimulateIDSplitted = outputStimulateID.split("\n")

        outputStimulateIDValid = []

        for line in outputStimulateIDSplitted:
            if len(line) == validLengthOfYoutubeIDs:
                outputStimulateIDValid.append(line)
        
        listOfIDs = copy.copy(outputStimulateIDValid)
        toWriteToOutline = "\n".join(outputStimulateIDValid)

        # Writing to outline.txt
        # listOfIDs = (outputStimulateID.split("\n"))[:-1]
        # toWriteToOutline = "\n".join(listOfIDs)
        outlineFile = open(pathToOutline, "w")
        outlineFile.write(toWriteToOutline)
        outlineFile.close()

    else:
        pass

    
    numberOfItemsInOutline = len(((open(pathToOutline, "r")).read()).split("\n"))

    itemsInFolderAfterRemovingPART = os.listdir(directoryToOutput)

    videoIDsThatExistInFolderAlready = []

    for item in itemsInFolderAfterRemovingPART:
        videoID = (item.partition("."))[0]
        videoIDsThatExistInFolderAlready.append(videoID)

else:


    os.mkdir(playlistID)
    for folderName in foldersInPlaylistFolder:
        folderToCreate = playlistID + "/" + folderName
        os.mkdir(folderToCreate)
    
    # Crafting the command to prompt for video IDs
    commandStimulateID = f"youtube-dl --get-id {playlistID}"

    # Getting the IDs
    spinner.start()
    outputStimulateID = subprocess.check_output(commandStimulateID, shell=True, text=True)
    spinner.stop_and_persist()

    # Writing to outline.txt
    listOfIDs = (outputStimulateID.split("\n"))[:-1]
    toWriteToOutline = "\n".join(listOfIDs)
    outlineFile = open(pathToOutline, "w")
    outlineFile.write(toWriteToOutline)
    outlineFile.close()



# Get the length of the playlist via outline.txt
outlineFile = open(pathToOutline, "r")
outlineContent = outlineFile.read()
outlineFile.close()
outlineLines = outlineContent.split("\n")
outlineLength = len(outlineLines)


# Prepare to obtain a refined list to run functions through
refinedList = []

# Get userinputindex by reading outline.txt
userinputIndex = copy.copy(outlineLines)

# Constructing userinput by combining userinputIndex and imported functions
userinput = []
for videoID in userinputIndex:
    userinput.append([videoID, listOfFunctions])

# Checking whether progress.txt exists
progressFileExists = os.path.isfile(pathToProgress)

if progressFileExists:
    # Read this and check whether it's actually empty
    progressFile = open(pathToProgress, "r")
    progressContent = progressFile.read()
    progressFile.close()

    if len(progressContent) == 0 or progressContent.startswith("\n"):
        progressFileExists = False
    else:
        pass

# If progress.txt exists, we refine our list with reference to it
if progressFileExists:

    alreadyCompleted = []

    # print("progress file does exist already")

    # Reading contents of progress.txt
    progressFile = open(pathToProgress, "r")
    progressContent = progressFile.read()
    progressFile.close()

    # print(progressContent)

    # Separating the content by break lines
    progressSeparated = (progressContent.split("\n\n"))
    
    if '' in progressSeparated:
        progressSeparated.remove('')

    # print(f"length of separated progress is {len(progressSeparated)}")

    refinedProgressSeparatedList = []
    # uselater = []
    
    for i in range(len(progressSeparated)):
        currentProgressItem = progressSeparated[i]
        videoIDOfCurrentProgressItem = (currentProgressItem.split("\n"))[0]

        # if videoIDOfCurrentProgressItem == "NQn22oDBrg8":
        #     print("THIS IS THE WEIRD PLACE")
        #     print((currentProgressItem).split("\n")[1:])

        if videoIDOfCurrentProgressItem in videoIDsThatExistInFolderAlready:
            # if videoIDOfCurrentProgressItem == "NQn22oDBrg8":
            #     print("synthetically speaking: this video ID already exists in the folder, so i will append this current chunk into progress separated")

            refinedProgressSeparatedList.append(currentProgressItem)
            # uselater.append(currentProgressItem)
        else:
            pass

            # if videoIDOfCurrentProgressItem == "NQn22oDBrg8":
            #     refinedProgressSeparatedList.append(currentProgressItem)

            # print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!HONESTLY, {videoIDOfCurrentProgressItem} doesn't genuinely exist in the folder")



            # will i be genuinely okay if i take the big effort to remove JUST this guy from the progress list? just in this very branch


            # if videoIDOfCurrentProgressItem == "NQn22oDBrg8":
            #     print("well, all that fancy shit didn't mean much")
                
    
    progressSeparated = copy.copy(refinedProgressSeparatedList)

    # print(f"length of separated progress is {len(progressSeparated)}")ZmkzRBeqCYQ

    progressinputIndex = []
    for progressChunk in progressSeparated:
        chunkByLine = progressChunk.split("\n")
        videoID = chunkByLine[0]
        progressinputIndex.append(videoID)

    # print(progressinputIndex)

    # Looping through userinput
    for thisInput in userinput:

        # print(thisInput)

        # Create digestion clone
        digestionClone = copy.copy(thisInput)

        # Define components of digestionClone
        videoID = digestionClone[0]
        wideScopeOfFunctions = digestionClone[1]

        # Try to find existence of this userinput in the progress domain

        indices = []

        for i in range(len(progressinputIndex)):
            if progressinputIndex[i] == videoID:
                indices.append(i)

        if len(indices) > 0:
            indexInProgressExists = True
        else:
            indexInProgressExists = False
            
        # try:
        #     indexInProgress = progressinputIndex.index(videoID)
        #     indexInProgressExists = True
        # except:
        #     indexInProgressExists = False
        
        digestionScopeOfFunctions = copy.copy(wideScopeOfFunctions)

        testScope = []

        # If this userinput exists, then we have some work to do to minus off completed work
        if indexInProgressExists:

            for indexInProgress in indices:
                specificProgress = (progressSeparated[indexInProgress]).split("\n")
                functionsCompleted = specificProgress[1:]
                # print("this specific progress is [for index exists]")
                # print(specificProgress)
                # time.sleep(5)

                for completedFunction in functionsCompleted:
                    testScope.append(completedFunction)

                    while completedFunction in digestionScopeOfFunctions:
                        digestionScopeOfFunctions.remove(completedFunction)
    
        # If it doesn't exist or after we're finished minusing off completed work, we push this into our refined list

        # toprintout = f"[{videoID}, [{digestionScopeOfFunctions}]]"
        # print(toprintout)
        # time.sleep(1)
        refinedList.append([videoID, digestionScopeOfFunctions])

        # if videoID == "NQn22oDBrg8":
        #     print("HEYY!")
        #     print(digestionScopeOfFunctions)
        #     print("FUNCTIONS COMPLETED ARE")
        #     print(testScope)


else:
    refinedList = copy.copy(userinput)


# Getting length of refined list in preparation of Bar
lenRefinedList = len(refinedList)



# progressFile = open(pathToProgress, "w")
# progressFile.close()

# print(progressFileExists)

if progressFileExists:

    progressContentByLine = progressContent.split("\n")

    while True:
        if progressContentByLine[-1] == "":
            progressContentByLine = progressContentByLine[:-1]
        else:
            break



    progressContentByLineJoint = "\n".join(progressContentByLine)

    progressFile = open(pathToProgress, "w")
    progressFile.write(progressContentByLineJoint + "\n\n")
    # progressFile.write("\n\n")
    progressFile.close()


# print("sleeping rn, try checking whether the progress.txt smoothly has an extra fresh line break at the end")
# time.sleep(100)



# Change directory for ease of functions
os.chdir(playlistID)

pathToProgress = Path("data/progress.txt")
# print(Path.cwd())
# print(pathToProgress)



# for i in range(len(refinedList)):
#     scope = refinedList[i][1]
#     name = refinedList[i][0]
#     if len(scope) == 0:
#         print(name)


refinedList_temp = []

# print("before removing empty entries, refinedlist is: ")
# print(len(refinedList))

refinedList_addlater = []

for i in range(lenRefinedList):
    videoID = refinedList[i][0]
    videoScope = refinedList[i][1]

    if len(videoScope) == 0:
        refinedList_temp.append(refinedList[i])
    
    elif len(videoScope) > 0:
        refinedList_addlater.append(refinedList[i])


# for i in range(lenRefinedList):
#     videoID = refinedList[i][0]
#     videoScope = refinedList[i][1]

#     if len(videoScope) > 0:
#         refinedList_temp.append(refinedList[i])



refinedList = refinedList_temp + refinedList_addlater


# for refinedLine in refinedList:
#     print(refinedList)

# print(len(refinedList))


# NOWWW
# is a matter of trying to manipulate the progress bar so that
# the completed ones would show up first
# so i wouldn't be mislead by how there are STILL 539 more to go
# okay, go figure it out later. i need to wash up first

# time.sleep(100)


# print(f"Remaining: [{len(refinedList)}/{outlineLength)}]")

# print(f"[{playlistID}]")

lengthOfPlaylistID = len(str(playlistID))
totalHeadingPadding = (lengthOfPlaylistID + 2) * "-"
messageHeaderOfPlaylistID = totalHeadingPadding + "\n" + "|" + playlistID + "|" + "\n" + totalHeadingPadding

os.system("cls")

print(messageHeaderOfPlaylistID)

print(f"Remaining: [{len(refinedList_addlater)}/{outlineLength}]")

# print("AFTER removing empty entries, refinedlist is: ")
# print(len(refinedList))


# print("sleeping 100seconds before going into refinedlist")
# time.sleep(100)
prePadding = "\b\b\b\b\b\b"

# Main loop of functions happening
for total in [lenRefinedList]:
    with alive_bar(total, title="Downloading...", stats=False, spinner='notes2', length=int(paddingLength/2)) as bar:
        for i in range(lenRefinedList):
            # print(i)
            currentRefinedItem = refinedList[i]

            videoID = currentRefinedItem[0]
            functionsToPerform = currentRefinedItem[1]

            

            # progressMessageToPrint = f"[{videoID}: {functionsToPerform}]"
            progressMessageToPrint = f"{videoID}: {functionsToPerform}"
            progressMessageToPrint = progressMessageToPrint.ljust(paddingLength, ".")
            progressMessageToPrint = f"[{progressMessageToPrint}]"
            progressMessageToPrint = prePadding + progressMessageToPrint

            
            

            # print(len(progressMessageToPrint))

            # time.sleep(100)

            lengthOfI = len(str(i))
            totalPaddingNeededForThisI = "\b" * (lengthOfI - 1)

            progressMessageToPrint = totalPaddingNeededForThisI + progressMessageToPrint

            progressMessageToPrint = constructMessage(videoID, functionsToPerform, paddingLength, prePadding + totalPaddingNeededForThisI, "")
            
            # if i > 9:
            #     progressMessageToPrint = "\b" + progressMessageToPrint
            # elif i > 99:


            # print(f"\b\b\b\b\b\b[{videoID}: {functionsToPerform}]")
            

            if len(functionsToPerform) == 0:

                try:
                    bar()
                    continue
                except KeyboardInterrupt:
                    sys.exit()

                # print("HURRRRR the functions to perform is 0")
                # time.sleep(100)


            # print("HERE")

            print(progressMessageToPrint)


            # print(f"the length of functions to perform is {len(functionsToPerform)}")

            # time.sleep(100)
            # print("HERE")

            # time.sleep(100)

            # time.sleep(5)

            # print(videoID)
            # print(Path.cwd())


            # i found the problem
            # it has something to do with how i'm cancelling it and it goes through the keyboardinterrupt except
            # now, i need to somehow build this so that
            # 

            # time.sleep(100)

            try:
                
                progressFile = open(pathToProgress, "a")
                progressFile.write(f"{videoID}\n")
                
                # print(f"for {videoID}")

                # functionsAlreadyDone = sorted(list(set(listOfFunctions) - set(functionsToPerform)))

                # print(f"functions already done are: {functionsAlreadyDone}")

                # for alreadyDone in functionsAlreadyDone:
                #     progressFile.write(f"{alreadyDone}\n")
                #     # print(f"{alreadyDone} is already done")
                
                progressFile.close()

                # print(f"by right, we've closed the file already. it should be there.")
                # print(f"we're closing the progressfile")

                # print(f"the length of functions to perform is: {len(functionsToPerform)}")

                # print("sleeping 5 seconds")
                # print(time.sleep(5))

                # time.sleep(100)
                # print("sleeping before performing functions")

                time.sleep(1)

                # previouslyPerformedFunction = ""

                for performingFunction in functionsToPerform:
                    # print(f"[{videoID}: {str(performingFunction).rjust(20, ".")}]")
                    # print(f"[{videoID}: {str(performingFunction).rjust(20, ".")}]")
                    # ongoingString = f"[{videoID}: {performingFunction.rjust(20, '.')}]"
                    # print(f"[{videoID}: {(str(performingFunction)).rjust(20, ".")}]")

                    # previousFunction = previouslyPerformedFunction
                    # previouslyPerformedFunction = performingFunction

                    indexOfCurrentFunction = listOfFunctions.index(performingFunction)
                    indexOfPreviousFunction = indexOfCurrentFunction - 1




                    # messageToPrintHere = f"{videoID}: {str(performingFunction)}"
                    # # print("HNG")
                    # messageToPrintHere = messageToPrintHere.ljust(paddingLength-5, ".")
                    # messageToPrintHere = messageToPrintHere + "....."
                    # messageToPrintHere = f"[{messageToPrintHere}]"
                    # messageToPrintHere = totalPaddingNeededForThisI + prePadding + messageToPrintHere

                    messageToPrintHere = constructMessage(videoID, performingFunction, paddingLength, totalPaddingNeededForThisI + prePadding, ".....")

                    print(messageToPrintHere)

                    # time.sleep(100)
                    # messageToPrintHere = f"{totalPaddingNeededForThisI}\b\b\b\b\b\b[{videoID}: {str(performingFunction).ljust(paddingLength, '.')}.....]"



                    # print(f"{totalPaddingNeededForThisI}\b\b\b\b\b\b[{videoID}: {str(performingFunction).ljust(paddingLength, '.')}.....]")
                    try:
                        # print("TRYING this RIGHT NOW")
                        (getattr(globals()[performingFunction], performingFunction))(videoID)
                        # print("it succeeded")
                    except PermissionError:
                        errorMessage = constructMessage(videoID, performingFunction, paddingLength, prePadding + totalPaddingNeededForThisI, "ERROR:PERMISSION")
                        # print("PERMISSION ERROR")
                        print(errorMessage)
                        time.sleep(gentleSleepTime)
                        (getattr(globals()[performingFunction], performingFunction))(videoID)
                    except classes.TargetNotFound:
                        # print("TARGETNOTFOUND ERROR")
                        errorMessage = constructMessage(videoID, performingFunction, paddingLength, prePadding + totalPaddingNeededForThisI, "ERROR:TARGETNOTFOUND")
                        print(errorMessage)

                        time.sleep(gentleSleepTime)

                        if indexOfPreviousFunction < 0:
                            # print("No previous function to fall back on")
                            print(constructMessage(videoID, "No previous function to fall back on", paddingLength, prePadding + totalPaddingNeededForThisI, ""))
                            sys.exit()

                        while True:

                            try:
                                # print("Performing previous function")
                                print(constructMessage(videoID, "Performing previous function", paddingLength, prePadding + totalPaddingNeededForThisI, ""))
                                (getattr(globals()[listOfFunctions[indexOfPreviousFunction]], listOfFunctions[indexOfPreviousFunction]))(videoID)

                                # print("Performing current function")
                                print(constructMessage(videoID, "Performing current function", paddingLength, prePadding + totalPaddingNeededForThisI, ""))
                                (getattr(globals()[performingFunction], performingFunction))(videoID)

                                break

                            except classes.TargetNotFound:
                                continue




                        # print("LOL finally got the hook")

                    
                    # except TargetNotFound:
                    #     print("OH IT FINALLY HOOKED, TARGET NOT FOUND")

                    # messageToPrintHere = f"{videoID}: {str(performingFunction)}"
                    # messageToPrintHere = messageToPrintHere.ljust(paddingLength-5, ".")
                    # messageToPrintHere = messageToPrintHere + " DONE"
                    # messageToPrintHere = f"[{messageToPrintHere}]"
                    # messageToPrintHere = totalPaddingNeededForThisI + prePadding + messageToPrintHere

                    messageToPrintHere = constructMessage(videoID, performingFunction, paddingLength, totalPaddingNeededForThisI + prePadding, f" [{indexOfCurrentFunction + 1}/{len(listOfFunctions)}]")


                    # print(f"\b\b\b\b\b\b[{videoID}: {str(performingFunction).ljust(paddingLength, '.')} DONE]")

                    print(messageToPrintHere)

                    time.sleep(0.5)
                    progressFile = open(pathToProgress, "a")
                    progressFile.write(f"{performingFunction}\n")
                    progressFile.close()

                progressFile = open(pathToProgress, "a")
                progressFile.write("\n")
                progressFile.close()
                bar()

            except:
            # except KeyboardInterrupt:


                # print("got cancelled by keyboarinterrupt")

                itemsHere = os.listdir("output")

                for item in itemsHere:
                    if item.startswith(videoID):
                        if item.endswith("part"):
                            os.unlink(f"output/{item}")
                
                # progressFile.close()
                try:
                    progressFile.close()
                except:
                    pass

                progressFile = open(f"data/progress.txt", "r")
                progressContentExceptContent = progressFile.read()
                progressFile.close()

                splittedExceptProgressContent = progressContentExceptContent.split("\n\n")

                if "" in splittedExceptProgressContent:
                    splittedExceptProgressContent.remove('')

                latestExceptProgressChunk = splittedExceptProgressContent[-1]

                latestExceptProgressChunkSplitted = latestExceptProgressChunk.split("\n")
                # print(latestExceptProgressChunkSplitted)
                if len(latestExceptProgressChunkSplitted) == 2:
                    if latestExceptProgressChunkSplitted[-1] == "":
                        splittedExceptProgressContent = splittedExceptProgressContent[:-1]

                # theIDofLatestExceptProgressChunk = (latestExceptProgressChunk.split("\n"))[0]
                # if theIDofLatestExceptProgressChunk == videoID:
                #     remainingExceptProgress = splittedExceptProgressContent[:-1]

                # this may be the problematic part
                # because of how much i'm writing into the final progress file

                
                

                progressFileFinalWrite = open("data/progress.txt", "w")
                progressFileFinalWrite.write("\n\n".join(splittedExceptProgressContent))
                progressFileFinalWrite.close()

                # print("it got interrupted AND tried its best to salvage the progress, see whether ")
                sys.exit()

input()
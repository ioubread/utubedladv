import os

def func01Download(videoID):

    # print("running function 1")

    savetoDirectory = "/output"
    fullOutputParameter = f'{savetoDirectory}/%(id)s.%(ext)s'

    startOfLink = "https://www.youtube.com/watch?v="

    commandToRun = f"youtube-dl -q -i -o \"{fullOutputParameter}\" -f bestaudio {startOfLink + videoID}"

    # print(f"the command to run is: {commandToRun}")
    os.system(commandToRun)
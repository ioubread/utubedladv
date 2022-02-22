import subprocess

def func04Album(videoID):
    outputDir = "output"
    fileExt = "mp3"
    actualCommand = f"eyed3 {outputDir}/{videoID}.{fileExt} -A \"{videoID}\""
    actualCommandSplitted = actualCommand.split(" ")
    subprocess.call(actualCommandSplitted, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
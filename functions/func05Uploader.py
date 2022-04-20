import subprocess
import json

def func05Uploader(videoID):
    
    youtubeVideoIDIs = videoID

    commandToGetJson = f"youtube-dl {youtubeVideoIDIs} --dump-single-json"
    commandToGetJsonShattered = commandToGetJson.split(" ")
    outputGetJson = subprocess.run(commandToGetJsonShattered, capture_output=True)
    outputGetJsonDecoded = outputGetJson.stdout.decode('utf-8')
    convertToJson = json.loads(outputGetJsonDecoded)
    uploaderName = convertToJson['uploader']

    outputDir = "output"
    fileExt = "mp3"
    actualCommand = f"eyed3 {outputDir}/{videoID}.{fileExt} -a \"{uploaderName}\""
    actualCommandSplitted = actualCommand.split(" ")
    subprocess.call(actualCommandSplitted, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
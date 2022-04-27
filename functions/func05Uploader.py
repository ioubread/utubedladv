import subprocess
import json
import eyed3

def func05Uploader(videoID):

    fileExtension = "mp3"
    fileBasename = videoID
    filename = f"{fileBasename}.{fileExtension}"
    outputDir = "output"

    commandToGetJson = f"youtube-dl https://www.youtube.com/watch?v={videoID} --dump-single-json"
    commandToGetJsonShattered = commandToGetJson.split(" ")

    outputGetJson = subprocess.run(commandToGetJsonShattered, capture_output=True)
    outputGetJsonDecoded = outputGetJson.stdout.decode('utf-8')

    try:
        convertToJson = json.loads(outputGetJsonDecoded)
        convertToJson = json.loads(outputGetJsonDecoded)
        uploaderName = convertToJson['uploader']
    except:
        uploaderName = "Unknown"
        print(f"{videoID}: UNKNOWN")

    musicFileTagged = eyed3.load(f"{outputDir}/{filename}")
    musicFileTagged.tag.artist = uploaderName
    musicFileTagged.tag.save()
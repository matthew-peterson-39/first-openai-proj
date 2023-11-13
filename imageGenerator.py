from openai import OpenAI
from pathlib import Path
import urllib.request

def downloadImage(imageURL, file_path):
    """
    Helper function that downloads image generated and saves it to the specified file_path.
    """
    urllib.request.urlretrieve(imageURL, file_path)

#  replace $YOUR_API_KEY with your unique code from OpenAI API
def myKey():
    return "$YOUR_API_KEY"

def getCurrentCount(filePath='imageCount.txt'):
    with open(filePath, 'r') as file:
        currentValue = int(file.readline().strip())
    return currentValue

def incrementCount(filePath='imageCount.txt'):
    currentValue = getCurrentCount(filePath)
    newValue = currentValue + 1
    with open(filePath, 'w') as file:
        file.write(str(newValue))
    return newValue

def checkDirectoryExists(directory):
    #parents=True -- create any parent directories that are necessary to make the specified path.
    #exist_ok=True -- does not throw error if file exists (ie-> FileExistsError)
    Path(directory).mkdir(parents=True, exist_ok=True)

def genereateImage(imageDescription):
    response = client.images.generate(
        model="dall-e-3",
        prompt=imageDescription,
        #Number of images
        n=1,
        #sizes allowed per model:
        #dall-e-3: 1024x1024, 1792x1024, or 1024x1792 
        size="1024x1024")
    imageURL = response.data[0].url
    checkDirectoryExists('images')
    count = getCurrentCount()
    imageName = f"{imageDescription}-{count}.png"
    imagePath = Path('images') / imageName
    downloadImage(imageURL, imagePath)

# The response from this outputs to the command line and does not save the image.
# The image URL expires after 24 hrs so make sure to save the photo if you like it :D
# toCollab arg (assuming you didnt change filestructure): "images/filename.png"
def collabImage(toCollab):
    response = client.images.create_variation(
        image=open(toCollab, "rb"),
        n=1,
        size="1024x1024")
    return print(response)

if __name__ == '__main__':
    client = OpenAI(api_key=myKey())
    genereateImage('The most random thing you can think of.')
    # collabImage('images/file_name.png')
    incrementCount()
from pathlib import Path
from openai import OpenAI

# replace $YOUR_API_KEY with your unique code from OpenAI API
def myKey():
    return "$YOUR_API_KEY"

def getCurrentCount(filePath='audioCount.txt'):
    with open(filePath, 'r') as file:
        currentValue = int(file.readline().strip())
    return currentValue

def incrementCount(filePath='audioCount.txt'):
    currentValue = getCurrentCount(filePath)
    newValue = currentValue + 1
    with open(filePath, 'w') as file:
        file.write(str(newValue))
    return newValue

def writeJokeToFile(joke):
    count = getCurrentCount()
    filePath = f'joke-{count}.txt'
    with open(filePath, 'a') as file:
        file.write(joke + '\n')

def checkDirectoryExists(directory):
    #parents=True -- create any parent directories that are necessary to make the specified path.
    #exist_ok=True -- does not throw error if file exists (ie-> FileExistsError)
    Path(directory).mkdir(parents=True, exist_ok=True)

def toAudio(prompt, directory):
    checkDirectoryExists(directory)
    count = getCurrentCount()
    filePath = Path(directory) / f"{directory}-{count}.mp3"
    response = client.audio.speech.create(
        model="tts-1-hd",  #tts-1, tts-hd
        voice="onyx",   #nova, onyx, shimmer, fable, alloy
        input=prompt
    )
    response.stream_to_file(filePath)

def createHaikou(haikouContext):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Think of a few different poems yourself before responding."
             "You will be given a single word or a sentance from the USER. The USER is exepecting back a haikou. Before responding,"
             "take some time to compare and analyze your haikou to provide the one that is the most sound and unique."},
            {"role": "user", "content": f'{haikouContext}'}
        ]
    )
    return response.choices[0].message.content

def createJoke(jokeContext):
    """NOTE:
    **Using knowledge of tokens for better prompt design**
    
    Prompts that end with a space
        -Now since we know that tokens can include trailing space characters, it helps to keep in mind that prompts 
            ending with a space character may result in lower-quality output. 
            This is because the API already incorporates trailing spaces in its dictionary of tokens.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Take sometime to famliarize yourself with the type of humor that is popular in the world before responding. You will"
                "be given some context from the USER. The USER is expecting to laugh or smile from your repsonse. Do your best to make that happen using the context of"
                "the USER prompt, but also feel free to be creative if you need to."},
            {"role": "user", "content": f'{jokeContext}'}
        ],
        max_tokens=50
    )
    joke = response.choices[0].message.content
    writeJokeToFile(joke)
    return joke

if __name__ == '__main__':
    client = OpenAI(api_key=myKey())

    ## JOKE AUDIO
    # jokeContext = createJoke("Mondays")
    # toAudio(jokeContext, 'jokes')

    ## HAIKOU ADUIO
    haikou = createHaikou('Fall')
    toAudio(haikou, 'haikous')

    incrementCount()
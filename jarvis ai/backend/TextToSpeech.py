import pygame     # import pygame librry for handling audio playback
import random      # import random for generatioj random choices
import asyncio   #import asyncio for asynchronous funtions
import edge_tts  # import edge tts for tts functionality
import os  # import os for file path handling 
from dotenv import dotenv_values  # import dotenv for reading evn var rom a dotenv file

# load the enviromant variables from a .env file
env_vars = dotenv_values(".env") 
AssistantVoice = env_vars.get("AssistantVoice")

if not AssistantVoice:
    raise ValueError("Missing AssistantVoice in .env file")   # get the assistant voice feom the anviroment variable

# asynchronous function to convert text file into audio file
async def TextToAudioFile(text) -> None:     
    file_path = r"Data\speech.mp3"  # define the path where the speech file will be saved

    if os.path.exists(file_path):   # check if the file already exixts
        os.remove(file_path)   # if it exists, remove it avoid overwriting error.

    # create the communication objesct to generate speech
    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate= '+13%')
    await communicate.save(r'Data\speech.mp3') 

#function to manage tts funtionality
def TTS(Text, func=lambda r=None: True):
    while True:
        try:
            # convet the text to an audio file asynchronously.
            asyncio.run(TextToAudioFile(Text))

            # initialize pygame mixer for audio playback.
            pygame.mixer.init()

            # load the generated speech file into pygame mixer.
            pygame.mixer.music.load(r"Data\speech.mp3")
            pygame.mixer.music.play()    # play the audio.

            # loop until the audio is done playing od the fucntion stops.
            while pygame.mixer.music.get_busy():
                if func() == False:      #check if the internal functions returns false.
                    break
                pygame.time.Clock().tick(10)     # limit the loop for 10 ticks per second.

            return True    # return true if the audio
        

        except Exception as e:   # handle any exceptions during the process
            print(f"Error in TTS: {e}")

        finally:
            try:
                #call the provided function with false to signal the end of tts.
                func(False)
                pygame.mixer.music.stop()    # stop the audio playback
                pygame.mixer.quit()          # quit the pygame mixer

            except Exception as e:   #handle any enception during cleanup.
                print(f"Error in finally block: {e}")

# function to manage tts with additional responses for long text.
def TextToSpeech(Text, func=lambda r=None: True):
    Data = str(Text).split(",")     # split the texts by periods into a list of sentnces.

    # list of predefined responses for cases where the text is too long.
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]

    # if the txt is very long (more than 4 sentences and 250 characters), add a response message.
    if len(Data) > 4 and len(Text) >= 250:
        TTS("".join(Text.split(".")[0:2]) +". " + random.choice(responses), func)

        #otherwise, just play the whole text
    else:
        TTS(Text, func)

# main execution loop
if __name__== "__main__":
    while True:
        #prompt user for input and pass it to the tts function.
        TextToSpeech(input("Enter the text: "))
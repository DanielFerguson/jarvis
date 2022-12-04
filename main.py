# Convert user speech to text

import speech_recognition as sr
import openai
import boto3
import tempfile
from playsound import playsound

# set the API key
openai.api_key = "<your-openai-key-here>"

# create a Polly client
polly = boto3.client("polly", region_name='us-west-1')

# create a Recognizer instance
r = sr.Recognizer()

# define a callback function to be called every time the Recognizer instance detects a complete sentence
def heard(recognizer, audio):
    try:
        # use the Recognizer instance to convert the speech to text
        text = recognizer.recognize_google(audio)

        # print the converted text
        print("User: " + text)

        # call the GPT-3 chat API
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=text,
            max_tokens=1024,
            temperature=0.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # call the synthesize_speech() method of the Polly client, passing in the text and desired voice
        response = polly.synthesize_speech(
            Text=response['choices'][0]['text'],
            VoiceId="Joanna",
            OutputFormat="mp3"
        )

        # extract the audio data from the response
        audio_data = response["AudioStream"].read()

        # create a temporary file to hold the audio data
        with tempfile.NamedTemporaryFile(mode="wb") as temp:
            # write the audio data to the temporary file
            temp.write(audio_data)
            temp.flush()

            # play the audio data from the temporary file
            playsound(temp.name)

        print(response)

    except sr.UnknownValueError:
        pass
    except sr.RequestError:
        pass

# start listening in the background, and call the heard() callback function every time a complete sentence is detected
r.listen_in_background(sr.Microphone(), heard)

# keep the program running until the user presses a key
input("Press any key to stop listening...\n")
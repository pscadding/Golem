# saved as greeting-client.py
import sys
import speech_recognition as sr
import Pyro4
import Pyro4.util
sys.excepthook = Pyro4.util.excepthook

gc = Pyro4.Proxy("PYRONAME:golem.controller@192.168.0.66:9090") # get a Pyro proxy to the Golem object



recognizer = sr.Recognizer()

commandDict = {
    "move forward": gc.move_fowards,
    "move forwards": gc.move_fowards,
    "move backward": gc.move_backwards,
    "move backwards": gc.move_backwards,
}

def run_command(text):
    command = commandDict.get(text.lower())

    if command:
        command()
    else:
        print("command not understood")


def listen():
    print("Begin Listen")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)


    print("now recognise")
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        text = recognizer.recognize_google(audio)
        print("Google Speech Recognition thinks you said ",text)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

while True:
    text = listen()
    if text:
        run_command(text)


import json
import speech_recognition as sr
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


recognizer = sr.Recognizer()
class VoiceControl(object):

    def __init__(self,gc):
        self.commandDict = {
            "forward": gc.move_forwards,
            "forwards": gc.move_forwards,
            "move forward": gc.move_forwards,
            "move forwards": gc.move_forwards,
            "go forwards": gc.move_forwards,
            "go forward": gc.move_forwards,

            "backward": gc.move_backwards,
            "backwards": gc.move_backwards,
            "move backward": gc.move_backwards,
            "move backwards": gc.move_backwards,
            "go backward": gc.move_backwards,
            "go backwards": gc.move_backwards,
        }

    def run(self):
        r = sr.Recognizer()
        m = sr.Microphone()
        with m as source:
            r.adjust_for_ambient_noise(source) # we only need to calibrate once, before we start listening

        r.pause_threshold = 0.3
        r.energy_threshold = 300
        print("Listening")
        recognizer.listen_in_background(sr.Microphone(), self.recognise)

        while True:
            pass

    def run_command(self,text):
        command = self.commandDict.get(text.lower())

        if command:
            command()
        else:
            print("command not understood")

    def recognize_wit(self,audio_data, show_all=False):
        """
        Performs speech recognition on ``audio_data`` (an ``AudioData`` instance), using the Wit.ai API.

        The Wit.ai API key is specified by ``key``. Unfortunately, these are not available without `signing up for an account <https://wit.ai/>`__ and creating an app. You will need to add at least one intent to the app before you can see the API key, though the actual intent settings don't matter.

        To get the API key for a Wit.ai app, go to the app's overview page, go to the section titled "Make an API request", and look for something along the lines of ``Authorization: Bearer XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX``; ``XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`` is the API key. Wit.ai API keys are 32-character uppercase alphanumeric strings.

        The recognition language is configured in the Wit.ai app settings.

        Returns the most likely transcription if ``show_all`` is false (the default). Otherwise, returns the `raw API response <https://wit.ai/docs/http/20141022#get-intent-via-text-link>`__ as a JSON dictionary.

        Raises a ``speech_recognition.UnknownValueError`` exception if the speech is unintelligible. Raises a ``speech_recognition.RequestError`` exception if the speech recognition operation failed, if the key isn't valid, or if there is no internet connection.
        """
        key = "BNO3G7NX6LFBKT2KYMLFVH2ZHEEKUQIL"
        print("get wave data")
        wav_data = audio_data.get_wav_data(
            convert_rate=None if audio_data.sample_rate >= 8000 else 8000,  # audio samples must be at least 8 kHz
            convert_width=2  # audio samples should be 16-bit
        )
        url = "https://api.wit.ai/speech?v=20160526"
        print("get request")
        request = Request(url, data=wav_data,
                          headers={"Authorization": "Bearer {}".format(key), "Content-Type": "audio/wav"})
        try:
            print("Get Response")
            response = urlopen(request, timeout=None)
        except HTTPError as e:
            raise Pyro4.RequestError("recognition request failed: {}".format(e.reason))
        except URLError as e:
            raise Pyro4.RequestError("recognition connection failed: {}".format(e.reason))
        response_text = response.read().decode("utf-8")
        result = json.loads(response_text)

        # return results
        if show_all: return result
        if "_text" not in result or result["_text"] is None: raise Pyro4.UnknownValueError()
        return result["_text"]

    def recognise(self,recognizer,audio):
        print("now recognise")
        # try:
        #     # for testing purposes, we're just using the default API key
        #     # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        #     # instead of `r.recognize_google(audio)`
        #     text = recognizer.recognize_google(audio)
        #     print("Google Speech Recognition thinks you said ",text)
        #     if text:
        #         run_command(text)
        # except sr.UnknownValueError:
        #     print("Google Speech Recognition could not understand audio")
        # except sr.RequestError as e:
        #     print("Could not request results from Google Speech Recognition service; {0}".format(e))
        try:
            print("Wit.ai thinks you said " + self.recognize_wit(audio))
        except sr.UnknownValueError:
            print("Wit.ai could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Wit.ai service; {0}".format(e))

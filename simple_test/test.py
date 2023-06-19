'''
This is a simple test program to make Pepper repeat what the user saying.
The basic idea is, to use a function 'monitor' to record the audio file when the user is speaking.
Then the audio file is sent to Google Recognizer.
Finally, make Pepper speak the results of Google's speech recognition.

For example:
User: Hello!
Pepper: Hello!
'''
from speech_recognition import UnknownValueError

from ControlPepper import ControlPepper
from simple_sound_stream import SpeechRecognitionModule
from WAV2text import WAV2text
import time

'''
This is the method to record the audio file and stop when there is no voice input anymore. 

'''
def monitor(Robot, SpeechRecognition):
    # Subscribe to Naoqi sound detection API.
    Robot.sd.subscribe('Test')
    # Start to listening.
    SpeechRecognition.start()
    recording = False
    last_Signal = Robot.memory.getData("SoundDetected")
    start_time = time.time()
    while True:
        current_time = time.time()
        Signal = Robot.memory.getData("SoundDetected")
        # When there is a new sound, keep on listening. Mark audio signal detected here.
        if Signal != last_Signal:
            if not recording:
                recording = True
            print(Robot.memory.getData("SoundDetected"))
            last_Signal = Signal
            start_time = time.time()
        # When there is no new sound, but also no markers are detected for the audio signal, just hold on.
        elif not recording:
            start_time = current_time
        # When there is no new sound for 1 second, and has already been marked,
        # which means the user has finished speaking.
        elif current_time - start_time > 1:
            SpeechRecognition.save_buffer()
            SpeechRecognition.stop()
            print("stopped")
            break

    Robot.sd.unsubscribe('Test')


if __name__ == "__main__":
    # Initialize PepperControl Model
    IP = "172.18.48.50"
    port = 9559
    Robot = ControlPepper(IP, port)
    # Initialize the recorder
    global SpeechRecognition
    SpeechRecognition = SpeechRecognitionModule("SpeechRecognition", IP, port)
    # Waiting for usring speaking.
    monitor(Robot, SpeechRecognition)
    # Use Google Recognizer and get the result.
    Recognizer = WAV2text('/home/jiangeng/intelligentDialogueManagement/simple_test/simple_out.wav')
    try:
        result = Recognizer.recognize()
        Robot.say(str(result))
    except UnknownValueError:
        Robot.say('Google can not recognize your input.')
    # Make Pepper to repeat the answer from Google.


from pythonScript.ControlPepper import ControlPepper
from pythonScript.simple_sound_stream import SpeechRecognitionModule
import time


def monitor(Robot, SpeechRecognition):
    while True:
        # print('monitor is working.')
        Robot.sd.subscribe('Test')
        SpeechRecognition.start()
        recording = False
        last_Signal = Robot.memory.getData("SoundDetected")
        start_time = time.time()
        while True:
            current_time = time.time()
            Signal = Robot.memory.getData("SoundDetected")
            if Signal != last_Signal:
                if not recording:
                    recording = True
                print(Robot.memory.getData("SoundDetected"))
                last_Signal = Signal
                start_time = time.time()
            elif not recording:
                start_time = current_time

            elif current_time - start_time > 1:
                SpeechRecognition.save_buffer()
                SpeechRecognition.stop()
                print("stopped")
                break

        Robot.sd.unsubscribe('Test')


if __name__ == "__main__":
    IP = "172.18.48.50"
    port = 9559
    Robot = ControlPepper(IP, port)

    global SpeechRecognition
    SpeechRecognition = SpeechRecognitionModule("SpeechRecognition", IP, port)

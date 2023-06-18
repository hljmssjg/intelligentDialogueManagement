from speech_recognition import UnknownValueError
import time
from WAV2text import WAV2text
'''
Implements a module 'Nerve' to connect Rasa and Pepper.
Based on https://github.com/frietz58/WoZ4U.
'''
from simple_sound_stream import SpeechRecognitionModule
from ControlPepper import ControlPepper
from Queue import *
from threading import Event, Thread
from Communicate import Communicate
from Convert import convert_text
from Convert import title
import Tkinter as tk
from Tkinter import Scale
import re
import usrModel
import os
import shutil
from word2number import w2n

# M: Modality (Speech, Screen, None) % None is selected if neither speech
# nor screen will work. RASA should if possible detect this and adapt the
# dialogue (e.g. interrupt).
#
# V: Volume (1,2,3)
#
# F: Font size (1,2,3)
#
# H: Hearing impairment (0,1,2)
#
# S: Seeing impairment (0,1,2)
#
# C: Cognitive impairment (0,1,2)
#
# L: Ambient light (0,1,2)    % 0: not disturbing, 1: a bit disturbing, 2: very disturbing
#
# N: Ambient noise (0,1,2)   % 0: not disturbing, 1: a bit disturbing, 2: very disturbing

'''
Set the global params.
'''
modality = "Screen"
modality_old = modality
hearing = 0
seeing = 0
cognitive = 0

noise = 0
light = 0
attention = 1

cog_sleep_time = 1
wait_time = 6

master_switch = True
Pause = False
isRecognizing = False

Font_size = 40
volume = 0.5

V = 0
F = 0
M = None

'''
Create a GUI to set the dynamic parameters.
Ambient noise N: 0, 1, 2.
Ambient light L: 0, 1, 2.
Attention: 0 or 1.
'''

window = tk.Tk()
window.title("Command Panel")
button_variables = {
    "too noise": tk.IntVar(),
    "too dark": tk.IntVar(),
    "Attention": tk.IntVar(),
}


# The function to create GUI.
def model_GUI():
    global cog_sleep_time, seeing, hearing, Pause
    slider6 = Scale(window, from_=0.0, to=2.0, orient=tk.HORIZONTAL, variable=button_variables["too noise"])
    slider7 = Scale(window, from_=0.0, to=2.0, orient=tk.HORIZONTAL, variable=button_variables["too dark"])
    button9 = tk.Checkbutton(window, text="Attention", variable=button_variables["Attention"])

    button_variables["too noise"].set(0)
    button_variables["too dark"].set(0)
    button_variables["Attention"].set(1)

    label6 = tk.Label(window, text="Noise")
    label7 = tk.Label(window, text="Light")
    label9 = tk.Label(window, text="Attention")

    set_button = tk.Button(window, text="Set", command=print_button_value)

    label6.pack()
    slider6.pack()
    label7.pack()
    slider7.pack()
    label9.pack()
    button9.pack()
    set_button.pack()

    window.mainloop()


# The callback function to set the corresponding global param when 'set' button in GUI is pressed.
def print_button_value():
    global noise, light, attention
    for button_name, button_var in button_variables.items():
        print("var:", button_name)
        print("val:", button_var.get())

        if button_name == "too noise":
            noise = button_var.get()
        if button_name == "too dark":
            light = button_var.get()
        if button_name == "Attention":
            attention = button_var.get()


'''
Calculate V, F, M based on the global params H, N, S, L and set them on Pepper.
'''


# Function to calculate the values for V, F, M:
def getParameters(H, N, S, L):
    V = 1 + H + N
    F = 1 + S + L
    if V <= 3:
        M = "Speech"
    elif F <= 3:
        M = "Screen"
    else:
        M = None
    return V, F, M


# Function to set the values on Pepper:
def setParameters():
    global master_switch, Font_size, cog_sleep_time, wait_time, cognitive, modality, volume, modality_old, V, F, M
    while master_switch:
        cog_sleep_time = 3 + cognitive * 4
        wait_time = cognitive * 2 + 4

        if modality_old == "Screen" and modality == "Speech":
            Robot.hide_img()

        modality_old = modality

        V, F, M = getParameters(hearing, noise, seeing, light)
        # volume = 0.4 + V * 0.2
        brightness = 0.5 + light * 0.2
        Robot.set_brightness(brightness)
        if V <= 3:
            volume = V * 0.5
            Robot.set_volume(volume)
        Font_size = 30 + F * 50
        modality = M
    print("set Parameters module closed.")


'''
Sometimes Google recognizes speech recognition of numbers as English words instead of digital numbers.
This method is used to convert the words in the sentence to digital numbers.
'''


def convert_number_words(sentence):
    words = sentence.split()
    converted_words = []

    for word in words:
        try:
            number = w2n.word_to_num(word)
            converted_words.append(str(number))
        except ValueError:
            converted_words.append(word)

    converted_sentence = " ".join(converted_words)
    return converted_sentence


'''
The output on Pepper is determined according to the modality.
'''


def work(sentence):
    global Pause
    Pause = True
    if modality == "Screen":
        say_evt = Event()
        display_q.put([str(sentence), say_evt])
    elif modality == "Speech":
        Robot.say(str(sentence))
    else:
        Robot.stopDialog()
        say_evt = Event()
        display_q.put(['No modality. A staff is on the way.', say_evt])
        Robot.say('No modality. A staff is on the way.')
        stopAll(recognize_q)
    Pause = False


'''
Stop all threads.
'''


def stopAll(recognize_q):
    global master_switch, Pause
    Pause = True
    master_switch = False
    recognize_q.put(stoprecogize_evt)
    communicateModule.post('/restart')
    time.sleep(2)
    display_q.put(['End the process!', stopdisplay_evt])


'''
Convert a text to img and display it on the tablet.
'''


def display(display_q, robot):
    global Font_size
    while True:
        package = display_q.get()
        text = package[0]
        evt = package[1]
        The_title = title()
        convert_text(text, Font_size, The_title)
        robot.show_img(The_title)

        if evt == stopdisplay_evt:
            time.sleep(3)
            robot.hide_img()
            print('display is end')
            break


'''
When there is an audio file, send it to Google and get the result.
When Google recognizes it successfully, copy the audio file to the audio folder and mark it as audioX.WAV.
When Google cannot recognize the audio file, copy the audio file to the audio folder and mark it as errorX.WAV.
When Rasa asks about the left/right color,
display the memory test picture and adjust the holding time according to the user's cognitive impairment.
'''


def recognize(recognize_q, Robot):
    audio_num = 1
    reco_counts = 2
    # recognize_times = 2
    global isRecognizing, cog_sleep_time, hearing, seeing, Pause, cognitive, attention, noise, volume, modality, Font_size
    while True:
        isRecognizing = False
        evt = recognize_q.get()
        isRecognizing = True
        if evt == stoprecogize_evt:
            break
        Recognizer = WAV2text('/home/jiangeng/intelligentDialogueManagement/pythonScript/simple_out.wav')
        try:
            pre_result = Recognizer.recognize()
            result = convert_number_words(str(pre_result))

            source_file = 'simple_out.wav'
            target_folder = 'audios'
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
            target_file = os.path.join(target_folder, 'audio%d.wav' % audio_num)
            audio_num += 1
            shutil.copy(source_file, target_file)

            # recognize_times = 3
            r = communicateModule.post(result)
            a = communicateModule.receive(r, cognitive, attention, noise)
            print('[*****************GOOGLE SR API***************]: ' + str(pre_result))
            print('[*****************   Convert   ***************]: ' + str(result))
            print('[-----------------   RASA    -----------------]: ' + str(a))
            pattern = r'\*(.*?)\*'
            matches = re.findall(pattern, str(a))
            if matches:
                match_result = ''.join(matches)
                for eachUser in usrModel.usrModel:
                    if eachUser['name'] == match_result:
                        cognitive = eachUser['cognitive']
                        # exercise_Level = eachUser['exercise']

                        hearing = eachUser['hearing']
                        seeing = eachUser['seeing']

                        break

            memoryList = ['What is the color on the left?', 'What is the color on the right?', "Left color?",
                          'What is the left color?',
                          'What is the right color?', "Right color?"]
            if str(a) in memoryList:
                Robot.show_img('resized_memory')
                time.sleep(cog_sleep_time)
                if modality == "Speech":
                    Robot.hide_img()

                work(str(a))
                # recognize_q.clear()

                print('Pause is False')
            else:
                matching_parts = [item for item in memoryList if item in str(a)]
                if matching_parts:
                    matching_string = matching_parts[0]
                    remaining_string = str(a).replace(matching_string, '')

                    if remaining_string:
                        work(remaining_string)

                        print('Pause is False')
                    time.sleep(1.5)
                    Robot.show_img('resized_memory')
                    time.sleep(cog_sleep_time)
                    if modality == "Speech":
                        Robot.hide_img()
                        time.sleep(1)

                    work(matching_string)

                    print('Pause is False')
                else:

                    work(str(a))
                    # recognize_q.clear()

                    print('Pause is False')
            print('#################################################')
            print('H = ', hearing, 'S = ', seeing, 'C = ', cognitive, 'N = ', noise, 'L = ', noise, 'A = ', attention)
            print('M = ', modality, 'V = ', V, 'F = ', F)
            print('Current volume = ', volume, ' Current font size= ', Font_size)
            print('#################################################')
            goodbye_List = ["Ok! Good bye! Have a nice day!", "Goodbye and have a nice day!", "Bye!",
                            "Alright! Take care and have a wonderful day!", "Take care and have a wonderful day!",
                            "Good bye!",
                            "Sure! Goodbye and have a fantastic day!", "Goodbye and have a fantastic day!", "Bye Bye!"
                            ]
            if str(a) in goodbye_List:
                stopAll(recognize_q)

        except UnknownValueError:
            source_file = 'simple_out.wav'
            target_folder = 'audios'
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
            target_file = os.path.join(target_folder, 'error%d.wav' % audio_num)
            audio_num += 1
            shutil.copy(source_file, target_file)
            pass
    print('recognizer is stopped')


'''
Use simple_sound_stream to record the audio file.
Should pause when robot is speaking.
Adjust the waiting time according to the cognitive impairment. 
When the user still does not focus after the waiting time, remind the user according to the current modality.
'''


def monitor(Robot, SpeechRecognition, recognize_q):
    # listen_counts = 2
    global master_switch, Pause, attention, cognitive, wait_time
    original_time = time.time()
    while master_switch:
        if not Pause:
            # print('monitor is working.')
            Robot.sd.subscribe('Test')
            SpeechRecognition.start()
            recording = False
            last_Signal = Robot.memory.getData("SoundDetected")
            start_time = time.time()
            while True:
                if Pause:
                    SpeechRecognition.clear_buffer()
                    SpeechRecognition.stop()
                    break
                current_time = time.time()
                Signal = Robot.memory.getData("SoundDetected")
                if Signal != last_Signal:
                    # if current_time - original_time > 8:
                    #     SpeechRecognition.save_buffer()
                    #     SpeechRecognition.stop()
                    #     evt = Event()
                    #     recognize_q.put(evt)
                    #     break
                    if not recording:
                        recording = True
                    print(Robot.memory.getData("SoundDetected"))
                    last_Signal = Signal
                    start_time = time.time()
                elif not recording:
                    if attention:
                        original_time = time.time()
                    if current_time - original_time > wait_time:
                        if isRecognizing:
                            pass
                        else:
                            if not attention:
                                SpeechRecognition.stop()
                                time.sleep(0.1)
                                SpeechRecognition.clear_buffer()
                                time.sleep(0.1)
                                work('Sorry! I can not hear you!')
                                original_time = time.time()
                                break
                    start_time = current_time

                elif current_time - start_time > 1:
                    SpeechRecognition.save_buffer()
                    SpeechRecognition.stop()
                    print("stopped")
                    evt = Event()
                    recognize_q.put(evt)
                    # listen_counts = 2
                    break

            Robot.sd.unsubscribe('Test')
        else:
            # print('monitor is waiting for speech end.')
            original_time = time.time()
            continue

    print('monitor is stopped.')


'''
Four threads are defined. Global variables and queues are used to communicate between each thread.
'''

if __name__ == "__main__":
    IP = "172.18.48.50"
    port = 9559

    Robot = ControlPepper(IP, port)
    Robot.setSensitivity(0.7)
    Robot.set_volume(2)

    global SpeechRecognition
    SpeechRecognition = SpeechRecognitionModule("SpeechRecognition", IP, port)

    communicateModule = Communicate('http://localhost:5005/webhooks/rest/webhook')

    recognize_q = Queue()
    display_q = Queue()

    stoprecogize_evt = Event()
    stopdisplay_evt = Event()

    thread_monitor = Thread(target=monitor, args=(Robot, SpeechRecognition, recognize_q,))
    thread_recognize = Thread(target=recognize, args=(recognize_q, Robot,))
    thread_display = Thread(target=display, args=(display_q, Robot,))
    thread_set = Thread(target=setParameters)

    thread_monitor.start()
    thread_recognize.start()
    thread_display.start()
    thread_set.start()
    model_GUI()

    thread_set.join()
    thread_monitor.join()
    thread_recognize.join()
    thread_display.join()

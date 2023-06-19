# Intelligent dialogue management system

This code represents an intelligible dialogue manager designed for social robots. It was developed as part of a master's program at Umeå University.

## Environment

Rasa Version      :         3.4.2  
Minimum Compatible Version: 3.0.0  
Rasa SDK Version  :         3.4.0  
Python3 Version    :         3.7.16  

Python2 Version:             Python 2.7.17  

Operating System  :         Linux-5.4.0-126-generic-x86_64-with-Ubuntu-18.04-bionic  


## Instructions

1. Install Naoqi API, and modify '***intelligentDialogueManagement/set_paths.sh***' to build a link to Naoqi. Please refer to the [**Download NAOqi API**](https://github.com/frietz58/WoZ4U) section for specific operations.
2. Open '***intelligentDialogueManagement/pythonScript/ControlPepper.py***',
   Rewrite line 41 of the code as `url = 'http://<Your IP Address>:5000/img/%s.png' % img`
3. Open '***intelligentDialogueManagement/pythonScript/ImgServer.py***',
   Rewrite line 11 of the code as `with open(r'<Your folder path>/intelligentDialogueManagement/pythonScript/img/{}.png'.format(imageId), 'rb') as f:`
   Rewrite line 23 of the code as `app.run(host='<Your IP Address>', port=5000)`
4. Open '***intelligentDialogueManagement/pythonScript/Nerve.py***',
   Rewrite line 269 of the code as `Recognizer = WAV2text('<Your folder path>/intelligentDialogueManagement/pythonScript/simple_out.wav')`
   Rewrite line 445 of the code as `IP = "<Pepper's IP>"`

5. Open '***intelligentDialogueManagement/simple_test/test.py***',
   Rewrite line 56 of the code as `IP = "<Pepper's IP>"`
   Rewrite line 65 of the code as `Recognizer = WAV2text('<Your folder path>/intelligentDialogueManagement/pythonScript/simple_out.wav')`

## Run

Under the folder '***intelligentDialogueManagement***',

1. Open a terminal, run `rasa run`.
2. Open another terminal, run `rasa run actions`.
3. Open the third terminal, 
   run `cd pythonScript` and `python ImgServer.py `.
4. Open the last terminal,
   run `source set_paths.sh `, `cd pythonScript` and `python Nerve.py`.

## Test

If you want to run a simple test program, under the folder '***intelligentDialogueManagement***',

1. Open a terminal.
2. Run `source set_paths.sh `.
3. Run `cd simple_test`.
4. Run `python test.py`

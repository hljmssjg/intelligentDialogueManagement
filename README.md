# Intelligent dialogue management system

This code represents an intelligible dialogue manager designed for social robots. It was developed as part of a master's program at Umeå University.

## Environment

Rasa Version      :         3.4.2  
Minimum Compatible Version: 3.0.0  
Rasa SDK Version  :         3.4.0  
Python3 Version    :         3.7.16  

Python2 Version:             Python 2.7.17  

Operating System  :         Linux-5.4.0-126-generic-x86_64-with-Ubuntu-18.04-bionic  

## Download

You could use git clone command to clone this project:

1. Create a new folder.
2. Open a terminal under that folder.
3. Enter `git clone https://github.com/hljmssjg/intelligentDialogueManagement.git`
4. Input your username and [Token](https://stackoverflow.com/questions/68781928/support-for-password-authentication-was-removed-on-august-13-2021) to log in and download.

Or, you could just simply download ZIP file.

## Set environment

1. Please make sure you have **python 2** and **python 3** in your system, and corresponding versions of pip, such as **pip** for Python 2 and **pip3** for Python 3.

2. Download NAOqi API from [Aldebaran website](https://www.aldebaran.com/en/support/pepper-naoqi-2-9/downloads-softwares). From the download page, select the **Old: Pepper SDK** (not Choregraphe), and download the archive.   Extract the archive to an arbitrary location, and remember that folder path.

3. To use this Intelligent dialogue management, we should set the SDK path. Open '***intelligentDialogueManagement/set_paths.sh***', Edit line 10 in **set_paths.sh** by replacing everything after the colon with the path to the **site-packages** folder inside the extracted NAOqi API folder. For example:  
   `export PYTHONPATH=${PYTHONPATH}:/home/jiangeng/WoZ4U/pynaoqi-python2.7-2.5.7.1-linux64/lib/python2.7/site-packages`.   
   And, edit line 11 in **set_paths.sh** by replacing everything after the colon with the path to the **lib** folder inside the extracted NAOqi folder. For example:   
   `export DYLD_LIBRARY_PATH=${DYLD_LIBRARY_PATH}:/home/jiangeng/WoZ4U/pynaoqi-python2.7-2.5.7.1-linux64/lib`.  
   For more details, please refer to the [WOZ4U](https://github.com/frietz58/WoZ4U)) project.
   
4. Install [rasa dialogue management](https://rasa.com/docs/rasa/installation/installing-rasa-open-source/). In this project, you need to install Rasa open source in your **Python 3** environment, so please use **pip3**:  
   `pip3 install rasa`.  
   And install dependencies for **spaCy**:   
   `pip3 install rasa[spacy]
   python3 -m spacy download en_core_web_md`  

5. Install [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) library in your **Python 2** environment, please use **pip**:   
   `pip install SpeechRecognition`.  
   It should be noted that this library only supports python3.8 +, but we need to use it under python 2. To do this, we need to rewrite its source code.

   1. Open a terminal, use `pip show SpeechRecognition` command to check the location of **SpeechRecognition**.
   2. When you get the install location of S**peechRecognition**, for example, `/home/jiangeng/.local/lib/python2.7/site-packages`, open the `/home/jiangeng/.local/lib/python2.7/site-packages/speech_recognition/__init__.py` file.
   3. Rewrite line 1513 with `endpoint = "https://api.assemblyai.com/v2/transcript/"+{transciption_id}`.

6. Install the remaining library in your **Python 2** environment:  
   `pip install sounddevice`  
   `pip install word2number`  
   `pip install Pillow`             

   `pip install pip install Flask `   
   How many libraries need to be installed depends on your **Python 2** environment. If you meet an error `ModuleNotFoundError: No module named XXXXX`, just use `pip install` command to install that module.

   


## Change path

1. Open '***intelligentDialogueManagement/pythonScript/ControlPepper.py***',  
   Rewrite line 41 of the code as `url = 'http://<Your IP Address>:5000/img/%s.png' % img`
2. Open '***intelligentDialogueManagement/pythonScript/ImgServer.py***',  
   Rewrite line 11 of the code as `with open(r'<Your folder path>/intelligentDialogueManagement/pythonScript/img/{}.png'.format(imageId), 'rb') as f:`  
   Rewrite line 23 of the code as `app.run(host='<Your IP Address>', port=5000)`
3. Open '***intelligentDialogueManagement/pythonScript/Nerve.py***',  
   Rewrite line 269 of the code as `Recognizer = WAV2text('<Your folder path>/intelligentDialogueManagement/pythonScript/simple_out.wav')`  
   Rewrite line 445 of the code as `IP = "<Pepper's IP>"`

4. Open '***intelligentDialogueManagement/simple_test/test.py***',  
   Rewrite line 56 of the code as `IP = "<Pepper's IP>" `   
   Rewrite line 65 of the code as `Recognizer = WAV2text('<Your folder path>/intelligentDialogueManagement/pythonScript/simple_out.wav') ` 

## Static test

You can test the Rasa dialog manager locally without connecting to the Pepper robot. Under the folder '***intelligentDialogueManagement***',

1. Open a terminal, enter `rasa run actions`:  
   ![Rasa run actions](https://github.com/hljmssjg/intelligentDialogueManagement/blob/main/README_IMG/runActions.png)
2. Open another terminal, enter `rasa shell`. Then you could talk to your assistant on the command line.  
   ![Rasa shell](https://github.com/hljmssjg/intelligentDialogueManagement/blob/main/README_IMG/rasaShell.png)

If you meet an error: `rasa_nlu.model.UnsupportedModelError: The model version is to old to be loaded by this Rasa NLU instance. Either retrain the model, or run withan older version...`, Under the folder '***intelligentDialogueManagement***',

1. Open another terminal, enter `rasa train`.
2. Then try `rasa shell` again.

## Run

Under the folder '***intelligentDialogueManagement***',

1. Open a terminal, enter `rasa run`.  
   ![Rasa run](https://github.com/hljmssjg/intelligentDialogueManagement/blob/main/README_IMG/rasaRun.png)
2. Open another terminal, enter `rasa run actions`.  
   ![Rasa run actions](https://github.com/hljmssjg/intelligentDialogueManagement/blob/main/README_IMG/runActions.png)
3. Open the third terminal,  
   enter `cd pythonScript` and `python ImgServer.py `.  
   ![Img Server](https://github.com/hljmssjg/intelligentDialogueManagement/blob/main/README_IMG/ImgServer.png)
4. Open the last terminal,  
   enter `source set_paths.sh `. You will get a response: **Setting environment variables for Bash on Linux/Mac** .    
   
   Then,  enter `cd pythonScript` and `python Nerve.py`.
   
   ![Nerve](https://github.com/hljmssjg/intelligentDialogueManagement/blob/main/README_IMG/Nerve.png)

## Test

If you want to run a simple test program, under the folder '***intelligentDialogueManagement***',

1. Open a terminal.
2. Enter `source set_paths.sh `.
3. Enter `cd simple_test`.
4. Enter `python test.py`


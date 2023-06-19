#!/usr/bin/env python
import speech_recognition as sr
'''
Use Google recognizer service to transform WAV audio file to text.
'''

class WAV2text:
    def __init__(self, fileAddress):
        self.address = fileAddress

    def recognize(self):
        r = sr.Recognizer()
        
        sample = sr.AudioFile(self.address)
        
        with sample as source:
            audio = r.record(source)
        result = r.recognize_google(audio)
        return result







import requests
import re

'''
Implements a module to communicate with Rasa.
'''
class Communicate:
    def __init__(self, url):
        self.url = url

    '''
    Post the sentence to Rasa server.
    '''
    def post(self, sentance):
        message = {
            "sender": 'test_user',
            "message": sentance
        }
        r = requests.post(self.url, json=message)
        return r

    '''
    Receive the sentence from Rasa server. Choose the correct amount of information.
    '''
    def receive(self, r, cognitive, attention, noise):

        # response = r.text.decode("utf-8")
        response = r.text
        print(response)
        if noise > 1:
            pattern = r'\&(.*?)\&'
        else:
            if attention:
                if cognitive < 1:
                    pattern = r'\$(.*?)\$'

                elif cognitive <2:
                    pattern = r'\@(.*?)\@'
                else:
                    pattern = r'\&(.*?)\&'
            else:
                pattern = r'\&(.*?)\&'

        matches = re.findall(pattern, response)
        result = ' '.join(matches)
        return result


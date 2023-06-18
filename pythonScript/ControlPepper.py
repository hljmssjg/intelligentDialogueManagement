from naoqi import ALProxy

'''
Implements a module to control Pepper.
Based on https://github.com/frietz58/WoZ4U.
'''
class ControlPepper:
    def __init__(self, IP, port):
        self.address = IP
        self.port = port
        self.memory = ALProxy("ALMemory", self.address, self.port)
        self.tts = ALProxy("ALTextToSpeech", self.address, self.port)
        self.tablet = ALProxy("ALTabletService", self.address, self.port)
        self.sd = ALProxy("ALSoundDetection", self.address, self.port)
        self.led = ALProxy("ALLeds", self.address, self.port)

    def setSensitivity(self, value):
        self.sd.setParameter("Sensitivity", value)

    def say(self, sentence):
        self.tts.say(sentence)

    def stopDialog(self):
        self.tts.stopAll()

    def set_volume(self, value):
        # 0 - 100
        # self.audio.setOutputVolume(value)
        # Sets the current gain applied to the signal synthesized by the text to speech engine.
        # The default value is 1.0
        self.tts.setVolume(value)

    def set_speed(self, value):
        # 50-400 default 100
        self.tts.setParameter("speed", value)

    def set_brightness(self, value):
        self.tablet.setBrightness(value)

    def show_img(self, img):
        url = 'http://172.23.143.156:5000/img/%s.png' % img
        self.tablet.showWebview(url)

    def hide_img(self):
        self.tablet.hideWebview()

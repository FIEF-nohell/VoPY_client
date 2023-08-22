import socket
import pyaudio
from threading import Thread

class Client:
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.format = pyaudio.paInt16
        self.channels = 2
        self.rate = 44100
        self.chunk = 1024
        self.audio = pyaudio.PyAudio()

    def getAudioDevices(self):
        p = pyaudio.PyAudio()
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device ", i+1, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
        p.terminate()

    def sendAudio(self):
        stream = self.audio.open(format=self.format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunk)
        while True:
            data = stream.read(self.chunk)
            self.client.send(data)

    def receiveAudio(self):
        stream = self.audio.open(format=self.format, channels=self.channels, rate=self.rate, output=True, frames_per_buffer=self.chunk)
        while True:
            data = self.client.recv(self.chunk)
            stream.write(data)

    def run(self):
        send_thread = Thread(target=self.sendAudio)
        receive_thread = Thread(target=self.receiveAudio)
        send_thread.start()
        receive_thread.start()

if __name__ == "__main__":
    client = Client("127.0.0.1", 12345)
    client.getAudioDevices()
    ##client.run()

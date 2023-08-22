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

    def send_audio(self):
        stream = self.audio.open(format=self.format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunk)
        while True:
            data = stream.read(self.chunk)
            self.client.send(data)

    def receive_audio(self):
        stream = self.audio.open(format=self.format, channels=self.channels, rate=self.rate, output=True, frames_per_buffer=self.chunk)
        while True:
            data = self.client.recv(self.chunk)
            stream.write(data)

    def run(self):
        send_thread = Thread(target=self.send_audio)
        receive_thread = Thread(target=self.receive_audio)
        send_thread.start()
        receive_thread.start()

if __name__ == "__main__":
    client = Client("127.0.0.1", 12345)
    client.run()

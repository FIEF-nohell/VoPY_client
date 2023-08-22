from threading import Thread
import pyaudio
import socket

class Client:
    def __init__(self, host, port, username, frequency):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))               #Establish connection
        
        self.client.send(frequency.encode('utf-8'))     #Send frequency
        self.client.send(username.encode('utf-8'))      #Send username

        self.frequency = frequency.encode('utf-8')      #Encode and assign frequency
        self.username = username.encode('utf-8')        #Encode and assign username
        
        self.audio = pyaudio.PyAudio()                  #Initialize the PyAudio object for audio streaming
        self.format = pyaudio.paInt16                   #Set the audio format to 16-bit integer
        self.channels = 1                               #Set the audio channels to mono
        self.rate = 44100                               #Set the sample rate
        self.chunk = 1024                               #Set the chunk size (number of frames to buffer)

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
    ip = input("Enter the target ip: ")
    port = input("Enter the target port (default 12345): ")
    if port == "": port = 12345
    username = input("Enter your username: ")
    frequency = input("Choose a frequency (1-9): ")
    while frequency not in [str(i) for i in range(1, 10)]:
        print("Invalid choice. Please choose a frequency between 1 and 9.")
        frequency = input("Choose a frequency (1-9): ")
    client = Client(str(ip), port, username, frequency)
    client.run()
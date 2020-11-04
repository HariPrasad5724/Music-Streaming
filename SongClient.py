import socket
import pyaudio
import wave
import sys

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.connect(("192.168.43.34", 5544))

p = pyaudio.PyAudio()
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 3
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)
print("********Choose the song which is listed below********")
print("\n")
while True:
    res = client_socket.recv(1024).decode()
    print(res)
    print("\n")
    sys.stdout.flush()
    x = input("Select the song name: ")
    client_socket.send(x.encode())
    ch = int(client_socket.recv(1024).decode())
    if ch == 0:
        print("Choose the available song name!")
        continue
    if ch == 1:
        print("Track ", x, "is Playing !!")
        data = "1"
        while data != "":
            try:
                stream.write(data)
                data = client_socket.recv(1024)
            except KeyboardInterrupt:
                print("Song Paused!")
                stream.stop_stream()
                input_state = input("Enter R to Resume & E to Exit: ")
                if input_state.upper() == "R":
                    print("Song resumes!")
                    stream.start_stream()
                    continue
                if input_state.upper() == "E":
                    print("Streaming cancelled by the user!")
                    stream.close()
                    p.terminate()
                    continue
stream.stop_stream()
stream.close()
p.terminate()

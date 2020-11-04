import socket
import pyaudio
import wave
import os
from _thread import *


def clientthread(conn, address):
    print("<", address, ">  connected ")
    while True:

        resource = os.listdir("./resource")
        ss = "\n\t\t Song Player \n"
        for i in range(len(resource)):
            if i % 2 == 0:
                ss += "\n"
            resource[i] = resource[i][:-4]
            ss = ss+"\t\t\t\t"+resource[i]+"\t\t\t\t"
        conn.send(ss.encode())
        x = conn.recv(1024).decode()
        for i in resource:
            if x.lower() == i.lower():
                print("Lets start to stream!!")
                conn.send("1".encode())
                x = i
                break
        else:
            print("Hurray!  Select the available song!")
            conn.send("0".encode())
            continue
        x = "./resource/"+x+".wav"
        print(x)
        wf = wave.open(x, 'rb')

        p = pyaudio.PyAudio()

        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        frames_per_buffer=CHUNK)

        data = 1
        while data:
            data = wf.readframes(CHUNK)
            conn.send(data)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("192.168.43.34", 5544))

server_socket.listen(10)
while True:
    conn, address = server_socket.accept()
    start_new_thread(clientthread, (conn, address))

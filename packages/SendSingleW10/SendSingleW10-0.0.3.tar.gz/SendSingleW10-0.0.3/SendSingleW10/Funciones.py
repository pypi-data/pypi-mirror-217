from CheckVersionW10 import CheckVersion
from CheckVersionW10 import StrEnd
import socket

def SendSingle (Server, Port, Data):
    if CheckVersion():
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((Server, Port))
        info = Data + StrEnd(Port)
        client.send(info.encode())
        DataFromServer = client.recv(1024)
        client.close()
        return DataFromServer.decode()

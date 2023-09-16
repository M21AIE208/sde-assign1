import socket
import threading
import tqdm
import os
import hashlib

# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

class Node(threading.Thread):

    def __init__(self,host,port):
        super(Node,self).__init__()
        self.terminate_flag = threading.Event()
        self.host = host
        self.port = port
        self.peer_nodes = []
        self.hashfiles = []
        self.file = {}
        
        self.sock = socket.socket()
        self.sock.bind((self.host,self.port))
        # self.sock.listen(1)
        
    def add_file(self,filepath):
        hasher = hashlib.md5()
        try:
            with open(filepath,"rb") as fileObj:
                buf = fileObj.read()
                while len(buf)>0:
                    hasher.update(buf)
                    buf = fileObj.read()
            self.hashfiles.append(hasher.hexdigest())
            self.file[hasher.hexdigest()] = filepath
            print("File added\n")
            print("File hash : ", hasher.hexdigest())
            return hasher.hexdigest()
        except Exception as er:
            print("File Not Found")
                      
        
    def send_file(self,filehash,ip,port):

        if filehash in self.hashfiles:
            filename = self.file[filehash]

        filesize = os.path.getsize(filename)
        print(f"Connecting to {ip}:{port}")
        self.sock.connect((ip,port))
        print("Connected.")
        self.sock.send(f"{filename}{SEPARATOR}{filesize}".encode())
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                # we use sendall to assure transimission in 
                # busy networks
                self.sock.sendall(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))
        self.sock.close()
                
    
    def add_file_dir(self,folderpath):
        self.folderpath = folderpath
        
    def request_file(self):
        file_socket = socket.socket()
        file_socket.bind(("0.0.0.0",6000))
        file_socket.listen(5)
        client_socket, address =  file_socket.accept()
        print(f"Connected to {address}")
        received = client_socket.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        filename =  os.path.basename(filename)
        filesize = int(filesize)
        with open(f"{self.folderpath}{filename}","wb") as fileObj:
            while True:
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                fileObj.write(bytes_read)
                
        file_socket.close()
        print("File Downloaded")
        return client_socket 

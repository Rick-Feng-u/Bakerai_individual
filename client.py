import socket
class ourClient():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connects to a server
    def connect(self, connectInfo):
        self.sock.connect(connectInfo)
    
    # Gets a response in readable form from a server
    def getResponse(self):
        return self.sock.recv(4096).decode("utf-8")

    # Sends string response correctly encoded to the server
    def sendResponse(self, msg):
        self.sock.send(bytes(msg.encode()))
    
    # Closes the connection to the server
    def close(self):
        self.sock.close()
    
    # Opens a client connection with a server until closing
    def runClient(self):
        ip = input ("enter target IP Address: ")
        port = int(input("enter target port: "))
        client.connect((ip, port)) 
        userInput = ""
        while userInput != "quit":
            userInput = input("Send a message: ")
            client.sendResponse(userInput)
            response = client.getResponse()
            print("Server response: " + response)
        client.close()
# If this file is run as main
if __name__ == "__main__":
    client = ourClient()
    client.runClient()
    
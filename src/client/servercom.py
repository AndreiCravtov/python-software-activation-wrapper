import msgpack
import socket
import select

class ServerCommunication:
    def __init__(self):
        self.CONNECTION_TIMEOUT = 5

        self.PORT = 4209
        self.IP = socket.gethostbyname(socket.gethostname())
        self.ADDRESS = (self.IP, self.PORT)

        self.PACKAGE_SIZE = 4096

        # try connecting to the server
        self.connected = self.attempt_connection()

    def attempt_connection(self):
        # create client
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket created")

        # connect to server
        self.client.connect(self.ADDRESS)
        print("Connected to\t"+self.IP+" : "+str(self.PORT))

        # set client to non-blocking
        self.client.setblocking(0)

        # send greeting
        self.send_message({
            "message": "greeting"
        })
        print("Sent greeting package")

        # recieve welcome
        message = self.receive_message()
        if not (message["message"] if "message" in message else {}) == "welcome": # invalid connection
            #close connection
            self.client.close()
            print("Connection closed")

            # return not connected status
            return False

        return True

    def close_connection(self):
        if self.connected:
            self.client.close()
            print("Connection closed")

    def send_message(self, data_object):
        data_binary = msgpack.packb(data_object)
        self.client.send(data_binary)

    def receive_message(self):
        data_object = {}

        if select.select([self.client], [], [], self.CONNECTION_TIMEOUT)[0]:
            data_binary = self.client.recv(self.PACKAGE_SIZE)
            data_object = msgpack.unpackb(data_binary)

        return data_object

if __name__ == "__main__": # check if this is code is being executed from the source file
    raise Exception("This is a module. Import it to use...") # if yes, throw an error
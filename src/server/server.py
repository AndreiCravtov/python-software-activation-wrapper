import database as db
import licence as lc
import instruct as ins
import helper as hlp

import msgpack
import socket
import select
from threading import Thread

class Server:
    def __init__(self):
        # define constants
        self.SERVER_TICK_RATE = 120
        self.PACKAGE_SIZE = 4096

        self.SERVER_IP = socket.gethostbyname(socket.gethostname())
        self.SERVER_PORT = 4209
        self.SERVER_ADDRESS = (self.SERVER_IP, self.SERVER_PORT)

        self.CLIENT_NUMBER = 5
        self.SERVER_TIMEOUT = 5

        # create server socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket created")

        # set server to non-blocking
        self.server.setblocking(0)

        # initiate server socket
        self.server.bind(self.SERVER_ADDRESS)
        self.server.listen(self.CLIENT_NUMBER)
        print("Started listening on\t"+self.SERVER_IP+" : "+str(self.SERVER_PORT))

        # run server mainloop
        ins.Mainloop(self.catch_new_client_connection, self.SERVER_TICK_RATE)

    def catch_new_client_connection(self):
        try:
            # get a new client connection
            client, client_address = self.server.accept()
            print("Got a connection from\t"+client_address[0]+" : "+str(client_address[1]))

            # set client to non-blocking
            client.setblocking(0)

            # begin handling the client in a separate thread
            Thread(
                target=self.handle_client_connection,
                args=[client, client_address]
            ).start()
        except BlockingIOError as _: pass
        except Exception as e:
            print("Unexpected error while waiting for new connections!")
            print(e)

    def handle_client_connection(self, client, client_address):
        # print handling
        pnt = hlp.AtomicPrint()

        pnt.add_print("Handling connection from\t"+client_address[0]+" : "+str(client_address[1]))
        
        try:
            # receive greeting
            message = self.receive_message(client)

            if not (message["message"] if "message" in message else {}) == "greeting":
                self.send_message({
                    "message": "Invalid message received"
                }, client)
                raise Exception("Invalid message received")
            pnt.add_print("\tReceived greeting package")

            # send welcome
            self.send_message({
                "message": "welcome"
            }, client)
            pnt.add_print("\tSent welcome package")

            # receive main data packages
            message = self.receive_message(client)
            pnt.add_print("\tReceived main data package")

            # check for data validity
            try:
                if not lc.SoftwareLicence.validate_incoming_licence_components(message):
                    self.send_message(["Invalid incoming data"], client)
                    raise Exception("Invalid incoming data")
            except:
                self.send_message(["Invalid incoming data"], client)
                raise Exception("Invalid incoming data")                    
            pnt.add_print("\tReceived data is valid")

            # get return data and send it
            self.send_message({
                "message": lc.SoftwareLicence.generate_licence_components(message)
            }, client)
            pnt.add_print("\tReturn data generated")
            pnt.add_print("\tSent response data package")

            # move licence from active_keys to used_keys
            message = lc.SoftwareLicence.decrypt_key(message)
            db.LicenceDatabaseUtils.remove_active_key(message["message"]["key"], message["message"]["checksum"])
            db.LicenceDatabaseUtils.add_used_key(message["message"]["key"], message["message"]["checksum"])
            pnt.add_print("\tSuccessfully altered licence key database")

        except Exception as e:
            pnt.add_print("\tSome error occurred")
            pnt.add_print("\t"+str(e))

        #close connection
        client.close()
        pnt.add_print("\tConnection closed")

        # output to console
        pnt.print_all()

    def send_message(self, data_object, client):
        data_binary = msgpack.packb(data_object)
        client.send(data_binary)

    def receive_message(self, client):
        data_object = {}

        if select.select([client], [], [], self.SERVER_TIMEOUT)[0]:
            data_binary = client.recv(self.PACKAGE_SIZE)
            data_object = msgpack.unpackb(data_binary)

        return data_object
    
if __name__ == "__main__": # check if this is code is being executed from the source file
    raise Exception("This is a module. Import it to use...") # if yes, throw an error
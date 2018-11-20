"""
File: phonebookclienthandler.py
Project 10.5
Client handler for phonebook.
"""

from socket import *
from codecs import decode
from threading import Thread
from phonebook import Phonebook

BUFSIZE = 1024
CODE = "ascii" # You can specify other encoding, such as UTF-8 for non-English characters


class PhonebookClientHandler(Thread):
    """Handles a phonebook requests from a client."""
    
    def __init__(self, client, phonebook):
        """Saves references to the client socket and phonebook."""
        Thread.__init__(self)
        self.client = client
        self.phonebook = phonebook
   
    def run(self):
        self.client.send(bytes("Welcome to the phone book application!"))
        while True:
            message = decode(self.client.recv(BUFSIZE))
            if not message:
                print("Client disconnected")
                self.client.close()
                break
            else:
                request = message.split()
                command = request[0]
                if command == "FIND":
                    number = self.phonebook.get(request[1])
                    if not number:
                        reply = "Number not found."
                    else:
                        reply = "The number is " + number
                else:
                    self.phonebook.add(request[1], request[2])

                    # write it to the file:
                    filename = "Phonebook.txt"
                    phonebook_file = open(filename, "a")  # opens in read only
                    phonebook_file.write(request[1] + " " + request[2] + "\n")
                    phonebook_file.close()

                    reply = "Name and number added to phone book and file."
                self.client.send(bytes(reply))



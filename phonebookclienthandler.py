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

        # This block was moved from server file to try and make it handled here instead
        phonebook = Phonebook()  # called from the phonebook.py
        filename = "Phonebook.txt"
        while True:
            try:
                file = open(filename, "r")  # opens in read only
                print("File found")
                contents = file.readlines()
                for line in contents:
                    information = line.split(" ")  # This splits each line of the text file by spaces
                    person = phonebook.add(information[0], information[1])
                break
            except ReferenceError:
                print("File not found, do better next time.")
                filename = input("Please enter the name of the phonebook to be loaded: ")
        # End of test block

        # create string of phonebook to send to client on connection
        start_book = phonebook.__str__()
        self.client.send(bytes(start_book.encode()))

        self.client.send(bytes("Welcome to the phone book application!", CODE))
        while True:
            message = decode(self.client.recv(BUFSIZE), CODE)
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

                    reply = "Name and number added to phone book and file.\nReconnect to update table below."
                self.client.send(bytes(reply, CODE))



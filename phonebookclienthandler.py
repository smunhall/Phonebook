"""
File: phonebookclienthandler.py
Project 10.5
Client handler for phonebook.
"""

import base64
from codecs import decode
from threading import Thread
from Crypto import Random
from Crypto.Cipher import AES

BLOCK_SIZE = 16
BUFSIZE = 1024
PASSPHRASE = b"1234567890123456"
CODE = "ascii"  # You can specify other encoding, such as UTF-8 for non-English characters


class PhonebookClientHandler(Thread):
    """Handles a phonebook requests from a client."""

    def __init__(self, client, phonebook):
        """Saves references to the client socket and phonebook."""
        Thread.__init__(self)
        self.client = client
        self.phonebook = phonebook

    def encrypt(self, message, passphrase):
        """Used to encrypt data to be sent."""
        iv = Random.new().read(BLOCK_SIZE)
        aes = AES.new(passphrase, AES.MODE_CFB, iv)
        return base64.b64encode(aes.encrypt(message))

    def decrypt(self, encrypted, passphrase):
        """Used to decrypt data received."""
        iv = Random.new().read(BLOCK_SIZE)
        aes = AES.new(passphrase, AES.MODE_CFB, iv)
        return aes.decrypt(base64.b64decode(encrypted))

    def run(self):
        # This block was moved from server file to try and make it handled here instead
        # phonebook = Phonebook()  # called from the phonebook.py
        filename = "Phonebook.txt"
        while True:
            try:
                file = open(filename, "r")  # opens in read only
                print("File found")
                contents = file.readlines()
                for line in contents:
                    information = line.split(" ")  # This splits each line of the text file by spaces
                    self.phonebook.add(information[0], information[1])
                break
            except ReferenceError:
                print("File not found, do better next time.")
                filename = input("Please enter the name of the phonebook to be loaded: ")
        # End of test block

        # create string of phonebook to send to client on connection
        start_book = self.phonebook.__str__()
        start_book_encrypted = self.encrypt(bytes(start_book, "ascii"), PASSPHRASE)  # pass bytes into encode method
        self.client.send(start_book_encrypted)  # DATA SENT NEED ENCRYPTION

        self.client.send(bytes("Welcome to the phone book application!", CODE))  # This doesn't need encryption
        while True:
            message = decode(self.client.recv(BUFSIZE), CODE)  # DATA RECEIVED NEED DECRYPTION
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
                self.client.send(self.encrypt(bytes(reply, CODE), PASSPHRASE))  # doesn't need encryption

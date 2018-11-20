"""
File: phonebookserver.py
Server for providing phonebook access.
Uses client handlers to handle clients' requests.
Creates a single phonebook for all clients.
"""

from phonebook import Phonebook
from socket import *
from phonebookclienthandler import PhonebookClientHandler

# In this example, it is set to local host
HOST = "localhost"
PORT = 5001
ADDRESS = (HOST, PORT)

phonebook = Phonebook() # called from the phonebook.py
server = socket(AF_INET, SOCK_STREAM)
server.bind(ADDRESS)
server.listen(5)

# This is to pre-load the phonebook into the server before any clients connect
# filename = input("Please enter the name of the phonebook to be loaded: ")   # use "Phonebook.txt"
filename = "Phonebook.txt"

# while True:
try:
    file = open(filename, "r")      # opens in read only
    print("File found")
    contents = file.readlines()
    for line in contents:
        information = line.split(" ")  # This splits each line of the text file by spaces
        person = phonebook.add(information[0], information[1])
except ReferenceError:
    print("File not found, do better next time.")
    filename = input("Please enter the name of the phonebook to be loaded: ")

# create string of phonebook to send to client on connection
start_book = phonebook.__str__()

# The server now just waits for connections from clients
# and hands sockets off to client handlers
while True:
    print("Waiting for connection . . .")
    client, address = server.accept()
    print("... connected from: ", address)
    # send the starting book to the
    client.send(bytes(start_book.encode()))
    # The handlers share the phonebook
    # Multiple clients can connect to the phonebook
    handler = PhonebookClientHandler(client, phonebook)
    handler.start()

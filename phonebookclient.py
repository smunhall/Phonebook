"""
File: phonebookclient.py
Project: Phonebook client server program

Client for a phone book application.
Sends the commands ADD <name> <number> or FIND <name> to the server.

"""

from socket import *
from codecs import decode
from breezypythongui import EasyFrame
import re
import os

HOST = "localhost" # in your project, make the HOST IP to be dynamic - get it from the OS
PORT = 5001
BUFSIZE = 1024
ADDRESS = (HOST, PORT)
CODE = "ascii"


class PhonebookClient(EasyFrame):
    """GUI for the client app."""

    COLOR = "#CCCCFF"

    def __init__(self):
        """Initialize the frame and widgets."""
        EasyFrame.__init__(self, title = "Phone Book", background = PhonebookClient.COLOR)
        # Add the labels, fields, and button
        self.statusLabel = self.addLabel(text = "Do you want to connect to the Phonebook?",
                                     row = 0, column = 0,
                                     columnspan = 3,
                                     background = PhonebookClient.COLOR)
        self.findBtn = self.addButton(row = 1, column = 0,
                                      text = "Find",
                                      command = self.find,
                                      state = "disabled")
        self.addBtn = self.addButton(row = 1, column = 1,
                                      text = "Add",
                                      command = self.add,
                                      state = "disabled")
        self.connectBtn = self.addButton(row = 1, column = 2,
                                      text = "Connect",
                                      command = self.connect)
        self.outputArea = self.addTextArea("", row=2, column=0,
                                          columnspan=3,
                                          width=50, height=4)

    def find(self):
        """Looks up a name in the phone book."""
        name = self.prompterBox(promptString = "Enter the name.")
        if name == "": return
        self.server.send(bytes("FIND " + name))
        reply = decode(self.server.recv(BUFSIZE))
        if not reply:
            self.messageBox(message = "Server diconnected")
            self.disconnect()
        else:
            self.statusLabel["text"] = reply
        
    def add(self):
        """Adds a name and number to the phone book."""
        name = self.prompterBox(promptString = "Enter the name.")
        if name == "": return
        number = self.prompterBox(promptString = "Enter the number.")
        if number == "": return
        self.server.send(bytes("ADD " + name + " " + number))
        reply = decode(self.server.recv(BUFSIZE))
        if not reply:
            self.messageBox(message = "Server diconnected")
            self.disconnect()
        else:
            self.statusLabel["text"] = reply
            
    def connect(self):
        """Starts a new session with the doctor."""
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.connect(ADDRESS)
        start_book = self.server.recv(1024).decode()
        self.outputArea.setText(start_book)
        self.statusLabel["text"] = decode(self.server.recv(BUFSIZE))
        self.connectBtn["text"] = "Disconnect"
        self.connectBtn["command"] = self.disconnect
        self.findBtn["state"] = "normal"
        self.addBtn["state"] = "normal"
            
    def disconnect(self):
        """Ends the session with the doctor."""
        self.server.close()
        self.statusLabel["text"] = "Want to connect?"
        self.connectBtn["text"] = "Connect"
        self.connectBtn["command"] = self.connect
        self.findBtn["state"] = "disabled"
        self.addBtn["state"] = "disabled"

def main():
    """Instantiate and pop up the window."""
    PhonebookClient().mainloop()


if __name__ == "__main__":
    main()


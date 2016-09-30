#!/usr/bin/python

import os

# Variables


CMD_HISTORY=(os.path.expanduser("~") + "/.cmdTest/history")
CMD_STACKS=(os.path.expanduser("~") + "/.cmdTest/stacks")

README="/opt/cmdTest/README"

def STACKMANAGER():
    pass
def CREATE_STACK(STACKNAME):
    pass
def CHECKOUT_STACK(STACKNAME):
    pass

def INIT():
    if os.path.isdir(CMD_HISTORY):
        print ("Yes!")

def NEW():
    print ("No stacks detected, let's start by creating one.")
    try:
        raw_input("Press <enter> to begin.")
    except KeyboardInterrupt:
        print ("\nExiting!")
        exit()

    # Create stack
    try:
        STACKNAME = raw_input("Type the stack name: ")
    except KeyboardInterrupt:
        print ("\nExiting!")
        exit()
    CREATE_STACK(STACKNAME)
    CHECKOUT_STACK(STACKNAME)
    print ("\nDone!\n")
    print ("Now that you have a stack, consider populating it with questions so you can take a test!\n")

#NEW()
INIT()

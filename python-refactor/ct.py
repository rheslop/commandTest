#!/usr/bin/python

import os
import time

# Variables

CMD_HISTORY=(os.path.expanduser("~") + "/.CmdTest/history")
CMD_STACKS=(os.path.expanduser("~") + "/.CmdTest/stacks")

README = "/opt/cmdTest/README"

# QUIZE_SIZE is the number of questions as requested
QUIZ_SIZE = 0

# RANDOM_NUMBER between 1 and QUIZ_SIZE
RANDOM_NUMBER = 0

# PREVIOUS_QUESTION is used to ensure given question does not match previous
PREVIOUS_QUESTION = 0

FINAL_SCORE = 0

STARTD=(time.strftime("%Y-%m-%d"))
STARTT=(time.strftime("%H:%M:%S"))

def INIT_DIRS():
    if os.path.isdir(CMD_HISTORY):
        pass
    else:
        os.makedirs(CMD_HISTORY)
    if os.path.isdir(CMD_STACKS):
        pass
    else:
        os.makedirs(CMD_STACKS)

# An empty file, having the same name as the stack,
# but without extension, serves as a marker for the
# currently checked out stack.

def SANITY_CHECK():
    MARKERS = 0
    for i in (os.listdir(CMD_STACKS)):
        if not i.endswith(".db"):
            MARKERS += 1
    return MARKERS

def CHECKED_STACK():
    for i in (os.listdir(CMD_STACKS)):
        if not i.endswith(".db"):
            CURRENT = i
    return CURRENT

def CLEAR_CHECKOUT():
    for i in (os.listdir(CMD_STACKS)):
        if not i.endswith(".db"):
            os.remove(CMD_STACKS + "/" + i)

def STACKMANAGER():
    pass
def CREATE_STACK(STACKNAME):
    pass
def CHECKOUT_STACK(STACKNAME):
    pass


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

if (SANITY_CHECK() > 0):
    if (SANITY_CHECK() > 1):
        print "Correcting stack."
        CLEAR_CHECKOUT()
    else:
        print CHECKED_STACK()
else:
    print ("No stack checked out.")

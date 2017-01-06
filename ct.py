#!/usr/bin/python

import os
import subprocess
import time
import sqlite3

class commandColors:
    DEFAULT = '\33[0m'
    RED = '\033[31m'
    CYAN = '\33[36m'
    WHITE = '\33[37m'


def BANNER():
    print (' ____ _______   _____   __   ___    __   ______')
    print ('|  __|  _  | \_/  |  \_/ |  /   \  |  \ | |    \\')
    print ('| |  | | | |      |      | /  ^  \ |   \| | |\  |')
    print ('| |__| |_| | |\/| | |\/| |/  ___  \| |\   | |/  |')
    print ('|____|_____|_|__|_|_|__|_|__/_ _\__|_|_\__|____/ ')
    print ('             |___    ___|   _ |     |___    ___|')
    print ('                 |  |   |  |_  \  \_|   |  |')
    print ('                 |  |   |   _| _\  \    |  |')
    print ('                 |  |   |  |__|  \  \   |  |')
    print ('                 |__|   |_____|_____|   |__|')

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
    CURRENT = "noneXXXXX"
    for i in (os.listdir(CMD_STACKS)):
        if not i.endswith(".db"):
            CURRENT = i
    return CURRENT

def CLEAR_CHECKOUT():
    for i in (os.listdir(CMD_STACKS)):
        if not i.endswith(".db"):
            os.remove(CMD_STACKS + "/" + i)

def CHECKOUT_STACK(STACK):
    if os.path.isfile(CMD_STACKS + "/" + STACK + ".db"):
        open(CMD_STACKS + "/" + STACK, 'w').close
    else:
        print ("%s is not a valid option." % STACK)

def CREATE_STACK():
    subprocess.call('clear',shell=True)
    STACK = raw_input("Stack Name: ")
    DATABASE = CMD_STACKS + "/" + STACK + ".db"
    if os.path.isfile(DATABASE):
        print ("It appears a stack by that name already exists.")
        return 1
    else:
        connection = sqlite3.connect(DATABASE)
        troll = connection.cursor()
        troll.execute("CREATE TABLE main (id INTEGER PRIMARY KEY, Question TEXT, Answer TEXT)")
        connection.commit()
        connection.close()
        return STACK

def POPULATE(STACK):
    QUESTION = raw_input("Question ~> ")
    ANSWER = raw_input("Answer ~> ")
    DATABASE = CMD_STACKS + "/" + STACK + ".db"
    connection = sqlite3.connect(DATABASE)
    troll = connection.cursor()
    troll.execute("INSERT INTO main VALUES (?, ?, ?)", (1, QUESTION, ANSWER))
    connection.commit()
    connection.close()

def DISPLAY(STACK):
    DATABASE = CMD_STACKS + "/" + STACK + ".db"
    connection = sqlite3.connect(DATABASE)
    troll = connection.cursor()
    troll.execute('SELECT * FROM main')
    print (troll.fetchall())
    connection.commit()
    connection.close()

def NEW():
    print ("No stacks detected, let's start by creating one.")
    CREATE_STACK()
    CHECKOUT_STACK(STACKNAME)
    print ("\nDone!\n")
    print ("Now that you have a stack, consider populating it with questions so you can take a test!\n")

def TEST(stack):
    pass

def MAIN_MENU():
    print \
    commandColors.WHITE + "Welcome to CommandTest - Stack: " + \
    commandColors.RED + CHECKED_STACK() + \
    commandColors.DEFAULT
    print ""
    print('Options:')
    print ""
    print('    test                  create')
    print ""
    print('    display               populate')
    print ""
    print('    history               view')
    print ""
    print('    query                 stack')
    print ""
    print('    help                  exit')
    print ""
    
BANNER()
time.sleep(.5)
subprocess.call('clear',shell=True)
MAIN_MENU()

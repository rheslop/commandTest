#!/usr/bin/python

import os
import subprocess
import time
import sqlite3

class commandColors:
    DEFAULT = '\033[0m'
    RED = '\033[31m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'


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
    CURRENT = "deadMonkey"
    for i in (os.listdir(CMD_STACKS)):
        if not i.endswith(".db"):
            CURRENT = i
    return CURRENT

def CLEAR_CHECKOUT():
    for i in (os.listdir(CMD_STACKS)):
        if not i.endswith(".db"):
            os.remove(CMD_STACKS + "/" + i)

def CHECKOUT_STACK():
    subprocess.call('clear',shell=True)
    print commandColors.WHITE + "Select stack:" + commandColors.DEFAULT
    print('')
    for i in (os.listdir(CMD_STACKS)):
        if i.endswith(".db"):
            print i[:-3] + ('\n')
    SELECTION = raw_input(" ~> ")
    if SELECTION:
        if os.path.isfile(CMD_STACKS + "/" + SELECTION + ".db"):
            CLEAR_CHECKOUT()
            open(CMD_STACKS + "/" + SELECTION, 'w').close
        else:
            print commandColors.RED + \
            ("%s is not a valid option." % SELECTION) + \
            commandColors.DEFAULT
            time.sleep(1)
            CHECKOUT_STACK()
    else:
        MAIN_MENU()
    MAIN_MENU()

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
    subprocess.call('clear',shell=True)
    print('')
    print commandColors.WHITE + 'Question:'
    print commandColors.WHITE + 'Answer:' + commandColors.DEFAULT
    print('')
    QUESTION = raw_input('Question ~> ')
    subprocess.call('clear',shell=True)

    print('')
    print commandColors.WHITE + 'Question: ' + \
    commandColors.CYAN + QUESTION + commandColors.DEFAULT
    print commandColors.WHITE + 'Answer:' + commandColors.DEFAULT
    print('')
    ANSWER = raw_input('Answer ~> ')

    def POPULATE_MENU():
        subprocess.call('clear',shell=True)
        print('')
        print commandColors.WHITE + 'Question: ' + \
        commandColors.CYAN + QUESTION + commandColors.DEFAULT
        print commandColors.WHITE + 'Answer: ' + \
        commandColors.CYAN + ANSWER + commandColors.DEFAULT
        print('')
        print('Options:')
        print ('')
        print ('save    - commit and exit')
        print ('add     - commit and add another')
        print ('clear   - cancel and start over')
        print ('exit    - cancel and and return to main menu')          
        OPTION = raw_input(' ~> ')
        if OPTION == 'save':
            DATABASE = CMD_STACKS + "/" + STACK + ".db"
            connection = sqlite3.connect(DATABASE)
            troll = connection.cursor()
            NEXT_ID = troll.execute("SELECT COUNT(*) FROM main").fetchone()[0] + 1
            troll.execute("INSERT INTO main VALUES (?, ?, ?)", (NEXT_ID, QUESTION, ANSWER))
            connection.commit()
            connection.close()
        elif OPTION == 'add':
            DATABASE = CMD_STACKS + "/" + STACK + ".db"
            connection = sqlite3.connect(DATABASE)
            troll = connection.cursor()
            NEXT_ID = troll.execute("SELECT COUNT(*) FROM main").fetchone()[0] + 1
            troll.execute("INSERT INTO main VALUES (?, ?, ?)", (NEXT_ID, QUESTION, ANSWER))
            connection.commit()
            connection.close()
            POPULATE(STACK)
        elif OPTION == 'clear':
            POPULATE(STACK)
        elif OPTION == 'exit':
            MAIN_MENU()
        else:
            print commandColors.RED + OPTION + ' is not a valid option.' + \
            commandColors.DEFAULT
            time.sleep(1)
    POPULATE_MENU()
            

def DISPLAY(STACK):
    DATABASE = CMD_STACKS + "/" + STACK + ".db"
    connection = sqlite3.connect(DATABASE)
    troll = connection.cursor()
    troll.execute('SELECT * FROM main')
    print (troll.fetchall())
    connection.commit()
    connection.close()
    raw_input("Press Enter to continue...")

def NEW():
    print ("No stacks detected, let's start by creating one.")
    CREATE_STACK()
    CHECKOUT_STACK(STACKNAME)
    print ("\nDone!\n")
    print ("Now that you have a stack, consider populate it with questions so you can take a test :-) \n")

def TEST(stack):
    pass

def MAIN_MENU():
    subprocess.call('clear',shell=True)
    if CHECKED_STACK() == 'deadMonkey':
        STACK = 'NONE'
        STYLE = commandColors.RED
    else:
        STACK = CHECKED_STACK()
        STYLE = commandColors.CYAN

    # Some options require a checkedout stack
    def PRINT_WARN():
        print commandColors.RED + \
        'Stack must be Checked out first.'
        print 'Use' + commandColors.CYAN + ' stack ' \
        + commandColors.RED + 'for checkout.'
        time.sleep(1)
        subprocess.call('clear',shell=True)
        MAIN_MENU()

    print \
    commandColors.WHITE + "Welcome to CommandTest - Stack: " + \
    STYLE + STACK + commandColors.DEFAULT
    print ""
    print('Options:')
    print ""
    print('    test                  create')
    print('    display               populate')
    print('    history               view')
    print('    query                 stack')
    print('    help                  exit')
    print ""
    OPTION = raw_input(" ~> ")

    if OPTION == 'test':
        pass
    elif OPTION == 'display':
        pass
    elif OPTION == 'history':
        pass
    elif OPTION == 'query':
        pass
    elif OPTION == 'help':
        pass
    elif OPTION == 'create':
        CREATE_STACK()
    elif OPTION == 'populate':
        if STACK == 'NONE':
            PRINT_WARN()
        else:
            POPULATE(STACK)
    elif OPTION == 'view':
        if STACK == 'NONE':
            PRINT_WARN()
        else:
            DISPLAY(STACK)

    elif OPTION == 'stack':
        CHECKOUT_STACK()
    elif OPTION == 'exit':
        exit()
    else:
        print commandColors.RED + OPTION + \
        ' is not a valid option.' + commandColors.DEFAULT
        time.sleep(1)

    subprocess.call('clear',shell=True)
    MAIN_MENU()
    
BANNER()
time.sleep(.5)
MAIN_MENU()

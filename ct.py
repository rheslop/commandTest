#!/usr/bin/python

import curses
import os
import subprocess
import time
import sqlite3


def BANNER():
    screen.addstr(0, 10, ' ____ _______   _____   __   ___    __   ______')
    screen.addstr(1, 10, '|  __|  _  | \_/  |  \_/ |  /   \  |  \ | |    \\')
    screen.addstr(2, 10, '| |  | | | |      |      | /  ^  \ |   \| | |\  |')
    screen.addstr(3, 10, '| |__| |_| | |\/| | |\/| |/  ___  \| |\   | |/  |')
    screen.addstr(4, 10, '|____|_____|_|__|_|_|__|_|__/_ _\__|_|_\__|____/ ')
    screen.addstr(5, 10, '             |___    ___|   _ |     |___    ___|')
    screen.addstr(6, 10, '                 |  |   |  |_  \  \_|   |  |')
    screen.addstr(7, 10, '                 |  |   |   _| _\  \    |  |')
    screen.addstr(8, 10, '                 |  |   |  |__|  \  \   |  |')
    screen.addstr(9, 10, '                 |__|   |_____|_____|   |__|')

# Variables
screen = curses.initscr()
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

def MAIN_MENU(screen):
    curses.curs_set(0)
    BANNER()
    screen.refresh()
    time.sleep(.5)
    screen.clear()
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)
    curses.init_pair(2, curses.COLOR_CYAN, -1)
    curses.init_pair(3, curses.COLOR_RED, -1)
    screen.addstr(0, 0, 'Welcome to CommandTest - Stack: ', curses.color_pair(1))
    if CHECKED_STACK() == 'noneXXXXX':
        screen.addstr(0, 32, 'NONE', curses.color_pair(3))
    else:
        screen.addstr(0, 32, CHECKED_STACK(), curses.color_pair(2))
    screen.addstr(3, 0, 'Options:')
    screen.addstr(5, 3, 'B', curses.A_UNDERLINE)
    screen.addstr(5, 7, 'Begin Test')
    screen.addstr(5, 30, 'C', curses.A_UNDERLINE)
    screen.addstr(5, 34, 'Create a new stack')
    screen.addstr(7, 3, 'D', curses.A_UNDERLINE)
    screen.addstr(7, 7, 'Display Information')
    screen.addstr(7, 30, 'P', curses.A_UNDERLINE)
    screen.addstr(7, 34, 'Populate stack with questions')
    screen.addstr(9, 3, 'R', curses.A_UNDERLINE)
    screen.addstr(9, 7, 'View README')
    screen.addstr(9, 30, 'V', curses.A_UNDERLINE)
    screen.addstr(9, 34, 'View stack')
    screen.addstr(11, 3, 'H', curses.A_UNDERLINE)
    screen.addstr(11, 7, 'Review History')
    screen.addstr(11, 30, 'Q', curses.A_UNDERLINE)
    screen.addstr(11, 34, 'Query stack')
    screen.addstr(13, 3, 'ESC', curses.A_UNDERLINE)
    screen.addstr(13, 7, 'Exit')
    screen.addstr(13, 30, 'S', curses.A_UNDERLINE)
    screen.addstr(13, 34, 'Switch stack')
#    key_press = screen.getch()
#    while key_press != 27:
#        if key_press == ord('b'):
#            pass
#        elif key_press == ord('c'):
#            curses.endwin()
#            NEW_STACK = CREATE_STACK()
#            subprocess.call('clear',shell=True)
#            POPULATE(NEW_STACK)
#            DISPLAY(NEW_STACK)
#            key_press = 27
#        key_press = 27
    screen.getch()
    curses.endwin()

# 0: black
# 1: red
# 2: green
# 3: yellow
# 4: blue
# 5: magenta
# 6: cyan
# 7: white

curses.wrapper(MAIN_MENU)

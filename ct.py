#!/usr/bin/python

import os
import subprocess
import time
import sqlite3
from random import randint

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
CMD_HISTORY=(os.path.expanduser('~') + '/.CmdTest/history')
CMD_STACKS=(os.path.expanduser('~') + '/.CmdTest/stacks')
SETTINGS_DATABASE=(os.path.expanduser('~') + '/.CmdTest/settings.db')
README = '/opt/cmdTest/README'

def INIT():
    if not os.path.isdir(CMD_HISTORY):
        os.makedirs(CMD_HISTORY)
    if not os.path.isdir(CMD_STACKS):
        os.makedirs(CMD_STACKS)
    if not os.path.isfile(SETTINGS_DATABASE):
        connection = sqlite3.connect(SETTINGS_DATABASE)
        troll = connection.cursor()
        troll.execute('CREATE TABLE main (menu TEXT, option TEXT)')
        troll.execute('INSERT INTO main VALUES (?, ?)', ('test_type', 1))
        troll.execute('INSERT INTO main VALUES (?, ?)', ('visibility', 1))
        troll.execute('INSERT INTO main VALUES (?, ?)', ('case_sensitivity', 1))
        connection.commit()
        connection.close()
    
def SETTINGS():
    connection = sqlite3.connect(SETTINGS_DATABASE)
    troll = connection.cursor()
    troll.execute("SELECT option FROM main WHERE menu='test_type'")
    test_type = troll.fetchone()[0]
    troll.execute("SELECT option FROM main WHERE menu='visibility'")
    visibility = troll.fetchone()[0]
    troll.execute("SELECT option FROM main WHERE menu='case_sensitivity'")
    case = troll.fetchone()[0]
    connection.commit()
    connection.close()
    subprocess.call('clear',shell=True)
    print('')
    print(' Test Flow')
    print('')
    if test_type == '1':
        print(' 1. Randomized - Variable [*]')
        print(' 2. Randomized - Full     [ ]')
        print(' 3. Ordered               [ ]')
    elif test_type == '2':
        print(' 1. Randomized - Variable [ ]')
        print(' 2. Randomized - Full     [*]')
        print(' 3. Ordered               [ ]')
    elif test_type == '3':
        print(' 1. Randomized - Variable [ ]')
        print(' 2. Randomized - Full     [ ]')
        print(' 3. Ordered               [*]')
    print('')
    print('')
    print(' Behavior when wong answer provided:')
    print('')
    if visibility == '0':
        print(' 4. Show correct answer [ ]')
        print(' 5. Hide correct answer [*]')
    elif visibility == '1':
        print(' 4. Show correct answer [*]')
        print(' 5. Hide correct answer [ ]')
    print('')
    print('')
    print(' Case sensitivity:')
    print('')
    if case == '0':
        print(' 6. On  [ ]')
        print(' 7. Off [*]')
    elif case == '1':
        print(' 6. On  [*]')
        print(' 7. Off [ ]')
    print('')
    print('')
    USER_SELECTION = raw_input(' SELECTION ~> ')

    if USER_SELECTION == 'exit' or USER_SELECTION == 'quit':
        MAIN_MENU(0)
    else:
        try:
            test_int = int(USER_SELECTION)
        except ValueError:
            print commandColors.RED + USER_SELECTION + ' is not a number.  Please select menu option. (1 - 7)'
            print commandColors.DEFAULT
            time.sleep(1)
            SETTINGS()
        if not 0 < int(USER_SELECTION) < 8:
            print commandColors.RED + USER_SELECTION + ' is out of bounds.  Please select menu option between 1 and 7.'
            print commandColors.DEFAULT
            time.sleep(1)
            SETTINGS()
        else:
            connection = sqlite3.connect(SETTINGS_DATABASE)
            troll = connection.cursor()
            if USER_SELECTION == '1':
                troll.execute('UPDATE main SET option=? WHERE menu=?', ('1', 'test_type'))
            elif USER_SELECTION == '2':
                troll.execute('UPDATE main SET option=? WHERE menu=?', ('2', 'test_type'))
            elif USER_SELECTION == '3':
                troll.execute('UPDATE main SET option=? WHERE menu=?', ('3', 'test_type'))
            elif USER_SELECTION == '4':
                troll.execute('UPDATE main SET option=? WHERE menu=?', ('1', 'visibility'))
            elif USER_SELECTION == '5':
                troll.execute('UPDATE main SET option=? WHERE menu=?', ('0', 'visibility'))
            elif USER_SELECTION == '6':
                troll.execute('UPDATE main SET option=? WHERE menu=?', ('1', 'case_sensitivity'))
            elif USER_SELECTION == '7':
                troll.execute('UPDATE main SET option=? WHERE menu=?', ('0', 'case_sensitivity'))
            connection.commit()
            connection.close()
            SETTINGS()

def NEW():
    print ('No stacks detected, let\'s start by creating one.')
    CREATE_STACK()
    CHECKOUT_STACK(STACKNAME)
    print ('\nDone!\n')
    print ('Now that you have a stack, consider populate it with questions so you can take a test :-) \n')

def CHECKED_STACK():
    CURRENT = 'deadMonkey'
    for i in (os.listdir(CMD_STACKS)):
        if not i.endswith('.db'):
            CURRENT = i
    return CURRENT

def HISTORY(STACK):
    DATES = []
    TIMES = []
    SCORES = []
    TEST_HISTORY =(CMD_HISTORY + '/' + STACK + '.db')
    if not os.path.isfile(TEST_HISTORY):
        print commandColors.RED + 'There isn\'t history for this test yet.'
    else:
        connection = sqlite3.connect(TEST_HISTORY)
        troll = connection.cursor()
        troll.execute('SELECT DATE FROM main')
        for row in troll.fetchall():
            DATES.append(row[0])
        troll.execute('SELECT TIME FROM main')
        for row in troll.fetchall():
            TIMES.append(row[0])
        troll.execute('SELECT SCORE FROM main')
        for row in troll.fetchall():
            SCORES.append(row[0])
        for H_INDEX in range(0, len(DATES)):
            print commandColors.WHITE + DATES[H_INDEX] + ' ' + \
            TIMES[H_INDEX] + commandColors.CYAN + ' ' + \
            SCORES[H_INDEX] + commandColors.DEFAULT

    raw_input('Press Enter to continue...')

def CLEAR_CHECKOUT():
    for i in (os.listdir(CMD_STACKS)):
        if not i.endswith('.db'):
            os.remove(CMD_STACKS + '/' + i)

def CHECKOUT_STACK():
    subprocess.call('clear',shell=True)
    print commandColors.WHITE + 'Select stack:' + commandColors.DEFAULT
    print('')
    for i in (os.listdir(CMD_STACKS)):
        if i.endswith('.db'):
            print('     ') + i[:-3]
    print('')
    SELECTION = raw_input(' ~> ')
    if SELECTION:
        if SELECTION == 'exit':
            MAIN_MENU(0)
        elif os.path.isfile(CMD_STACKS + '/' + SELECTION + '.db'):
            CLEAR_CHECKOUT()
            open(CMD_STACKS + '/' + SELECTION, 'w').close
        else:
            print commandColors.RED + \
            ('%s is not a valid option.' % SELECTION) + \
            commandColors.DEFAULT
            time.sleep(1)
            CHECKOUT_STACK()
    else:
        MAIN_MENU(0)
    MAIN_MENU(0)

def CREATE_STACK():
    subprocess.call('clear',shell=True)
    STACK = raw_input('Stack Name: ')
    DATABASE = CMD_STACKS + '/' + STACK + '.db'
    if os.path.isfile(DATABASE):
        print ('It appears a stack by that name already exists.')
    else:
        connection = sqlite3.connect(DATABASE)
        troll = connection.cursor()
        troll.execute('CREATE TABLE main (Question TEXT, Answer TEXT)')
        connection.commit()
        connection.close()
        return STACK

def PRUNE(STACK):
    subprocess.call('clear',shell=True)
    print('')
    Qlist = []
    Alist = []
    ID_list = []

    DATABASE = CMD_STACKS + '/' + STACK + '.db'
    connection = sqlite3.connect(DATABASE)
    troll = connection.cursor()
    troll.execute('SELECT Question FROM main')
    for row in troll.fetchall():
        Qlist.append(row[0])
    troll.execute('SELECT Answer FROM main')
    for row in troll.fetchall():
        Alist.append(row[0])
    troll.execute('SELECT rowid FROM main')
    for row in troll.fetchall():
        ID_list.append(row[0])
        
    connection.close()

    for Q_INDEX in range(0, len(Qlist)):
        NUM = str(Q_INDEX + 1)
        print commandColors.RED + NUM + '. ' + \
        commandColors.WHITE + 'Q: ' + commandColors.DEFAULT + \
        Qlist[Q_INDEX] + ' ' + commandColors.WHITE + 'A: ' + \
        commandColors.DEFAULT + Alist[Q_INDEX]
    print('')
    print('Choose the Q/A pair to delete by number.\nThis will DELETE the Q/A pair from the stack.')
    print('\nType \'exit\' or \'quit\' to return to main menu.\n')
    DELETE_ME = raw_input(' ~> ')
    if DELETE_ME == 'exit' or DELETE_ME == 'quit':
        MAIN_MENU(0)
    else:
        try:
            Q_INDEX = int(DELETE_ME) - 1
        except ValueError:
            print commandColors.RED + 'ValueError: I don\'t recognize that as a number.' + commandColors.DEFAULT
            time.sleep(1)
            PRUNE(STACK)
    if int(DELETE_ME) <= 0:
        print commandColors.RED + 'IndexError: I\'m not seeing number %s' % DELETE_ME
        time.sleep(1)
        PRUNE(STACK)
    try:
        TARGET = ID_list[Q_INDEX]
    except IndexError:
        print commandColors.RED + 'IndexError: I\'m not seeing number %s' % DELETE_ME
        time.sleep(1)
        PRUNE(STACK)
    DATABASE = CMD_STACKS + '/' + STACK + '.db'
    connection = sqlite3.connect(DATABASE)
    troll = connection.cursor()
    troll.execute('DELETE FROM main WHERE rowid = ?', (TARGET,))
    connection.commit()
    connection.close()
    PRUNE(STACK)
    
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
            DATABASE = CMD_STACKS + '/' + STACK + '.db'
            connection = sqlite3.connect(DATABASE)
            troll = connection.cursor()
            troll.execute('INSERT INTO main VALUES (?, ?)', (QUESTION, ANSWER))
            connection.commit()
            connection.close()
        elif OPTION == 'add':
            DATABASE = CMD_STACKS + '/' + STACK + '.db'
            connection = sqlite3.connect(DATABASE)
            troll = connection.cursor()
            troll.execute('INSERT INTO main VALUES (?, ?)', (QUESTION, ANSWER))
            connection.commit()
            connection.close()
            POPULATE(STACK)
        elif OPTION == 'clear':
            POPULATE(STACK)
        elif OPTION == 'exit':
            MAIN_MENU(0)
        else:
            print commandColors.RED + OPTION + ' is not a valid option.' + \
            commandColors.DEFAULT
            time.sleep(1)
            POPULATE_MENU()
    POPULATE_MENU()
            
def DISPLAY(STACK):
    Qlist = []
    Alist = []

    DATABASE = CMD_STACKS + '/' + STACK + '.db'
    connection = sqlite3.connect(DATABASE)
    troll = connection.cursor()
    troll.execute('SELECT Question FROM main')
    for row in troll.fetchall():
        Qlist.append(row[0])
    troll.execute('SELECT Answer FROM main')
    for row in troll.fetchall():
        Alist.append(row[0])

    for Q_INDEX in range(0, len(Qlist)):
         print commandColors.WHITE + 'Question: ' + \
         commandColors.DEFAULT + Qlist[Q_INDEX]
         print commandColors.WHITE + 'Answer: ' + \
         commandColors.DEFAULT + Alist[Q_INDEX]
         print('')
    connection.close()

    raw_input('Press Enter to continue...')

def QUERY(STACK):
    Qlist = []
    Alist = []
    matches = 0

    DATABASE = CMD_STACKS + '/' + STACK + '.db'
    connection = sqlite3.connect(DATABASE)
    troll = connection.cursor()
    troll.execute('SELECT Question FROM main')
    for row in troll.fetchall():
        Qlist.append(row[0])
    troll.execute('SELECT Answer FROM main')
    for row in troll.fetchall():
        Alist.append(row[0])
    connection.close()
    print('')
    ARG = raw_input('QUERY: ')    
    for Q_INDEX in range(0, len(Qlist)):
        if Qlist[Q_INDEX].find(ARG) != -1:
            matches += 1
            print commandColors.WHITE + 'Question: ' + \
            commandColors.DEFAULT + Qlist[Q_INDEX]
            print commandColors.WHITE + 'Answer: ' + \
            commandColors.DEFAULT + Alist[Q_INDEX]
            print('')
        elif Alist[Q_INDEX].find(ARG) != -1:
            matches += 1
            print commandColors.WHITE + 'Question: ' + \
            commandColors.DEFAULT + Qlist[Q_INDEX]
            print commandColors.WHITE + 'Answer: ' + \
            commandColors.DEFAULT + Alist[Q_INDEX]
            print('')
    if matches == 0:
        print('No matches found.')
    raw_input('Press Enter to continue...')


def TEST1(STACK):
    # EXCLUSION_WINDOW is used to ensure questions are not repeated too often
    EXCLUSION_WINDOW = []

    Qlist = []
    Alist = []

    STARTD=(time.strftime("%Y-%m-%d"))
    STARTT=(time.strftime("%H:%M:%S"))

    # QUIZ_SIZE is the number of questions as requested

    CORRECT = 0
    INCORRECT = 0
    SCORE = 0.0

    # Populate Qlist and Alist with questions and answers

    DATABASE = CMD_STACKS + '/' + STACK + '.db'
    connection = sqlite3.connect(DATABASE)
    troll = connection.cursor()
    troll.execute('SELECT Question FROM main')
    for row in troll.fetchall():
        Qlist.append(row[0])
    troll.execute('SELECT Answer FROM main')
    for row in troll.fetchall():
        Alist.append(row[0])

    if len(Qlist) == 0:
        print('You must populate this stack with questions prior to testing.')
        time.sleep(1)
        MAIN_MENU(0)
    elif len(Qlist) == 1:
        QUIZ_SIZE = 1
    else:
        print('How many questions would you like to take?\n')
        try:
            QUIZ_SIZE = int(raw_input(' ~> '))
        except ValueError:
            print commandColors.RED + 'Error!'
            time.sleep(1)
            MAIN_MENU(0)

    if len(Qlist) > 20:
        EXCLUSION_WINDOW_SIZE = 7
    elif len(Qlist) > 10:
        EXCLUSION_WINDOW_SIZE = 4
    else:
        EXCLUSION_WINDOW_SIZE = 1

    for i in range(0, QUIZ_SIZE):

        Q_INDEX = randint(0, (len(Qlist) - 1))
        while Q_INDEX in EXCLUSION_WINDOW:
            Q_INDEX = randint(0, (len(Qlist) - 1))
        if len(EXCLUSION_WINDOW) < EXCLUSION_WINDOW_SIZE:
            EXCLUSION_WINDOW.append(Q_INDEX)
        else:
            del EXCLUSION_WINDOW[0]
            EXCLUSION_WINDOW.append(Q_INDEX)

        subprocess.call('clear',shell=True)
        # Header
        if i == 0:
            print commandColors.WHITE + \
            ('Total %d | Correct %d | Answered %d' % (QUIZ_SIZE,CORRECT,i)) \
            + commandColors.DEFAULT
        else:
            Score = float(CORRECT) / float(i)
            print commandColors.WHITE + \
            ('Total %d | Correct %d | Answered %d | Score ' % (QUIZ_SIZE,CORRECT,i)) \
            + commandColors.CYAN + '%.2f' % (Score) + commandColors.DEFAULT
        print('')

        print Qlist[Q_INDEX]
        user_response = raw_input(' ~> ')
        if user_response == Alist[Q_INDEX]:
            print('')
            print(':-)')
            CORRECT += 1
            time.sleep(.5)
        else:
            print('')
            print(commandColors.RED + 'Incorrect' + commandColors.DEFAULT)
            print(commandColors.WHITE + 'Correct Answer: ' \
            + commandColors.DEFAULT + Alist[Q_INDEX])
            INCORRECT += 1
            print('')
            raw_input('Press Enter to continue...')

    subprocess.call('clear',shell=True)
    print('')
    i += 1
    Score = float(CORRECT) / float(i)
    DISPLAY_SCORE = ('%.2f' % (Score))
    print('Final Score = ' + commandColors.CYAN + DISPLAY_SCORE)
    print commandColors.DEFAULT
    connection.close()

    COMMIT_HISTORY(STACK, STARTD, STARTT, DISPLAY_SCORE)
    raw_input('Press Enter to continue...')

def TEST2(STACK):

    Qlist = []
    Alist = []

    STARTD=(time.strftime("%Y-%m-%d"))
    STARTT=(time.strftime("%H:%M:%S"))

    CORRECT = 0
    INCORRECT = 0
    SCORE = 0.0

    # Populate Qlist and Alist with questions and answers

    DATABASE = CMD_STACKS + '/' + STACK + '.db'
    connection = sqlite3.connect(DATABASE)
    troll = connection.cursor()
    troll.execute('SELECT Question FROM main')
    for row in troll.fetchall():
        Qlist.append(row[0])
    troll.execute('SELECT Answer FROM main')
    for row in troll.fetchall():
        Alist.append(row[0])

    if len(Qlist) == 0:
        print('You must populate this stack with questions prior to testing.')
        time.sleep(1)
        MAIN_MENU(0)

    QUIZ_SIZE = len(Qlist)

    for i in range(0, len(Qlist)):

        Q_INDEX = randint(0, (len(Qlist) - 1))
        subprocess.call('clear',shell=True)
        # Header
        if i == 0:
            print commandColors.WHITE + \
            ('Total %d | Correct %d | Answered %d' % (QUIZ_SIZE,CORRECT,i)) \
            + commandColors.DEFAULT
        else:
            Score = float(CORRECT) / float(i)
            print commandColors.WHITE + \
            ('Total %d | Correct %d | Answered %d | Score ' % (QUIZ_SIZE,CORRECT,i)) \
            + commandColors.CYAN + '%.2f' % (Score) + commandColors.DEFAULT
        print('')

        print Qlist[Q_INDEX]
        user_response = raw_input(' ~> ')
        if user_response == Alist[Q_INDEX]:
            print('')
            print(':-)')
            CORRECT += 1
            time.sleep(.5)
            del Qlist[Q_INDEX]
            del Alist[Q_INDEX]
        else:
            print('')
            print(commandColors.RED + 'Incorrect' + commandColors.DEFAULT)
            print(commandColors.WHITE + 'Correct Answer: ' \
            + commandColors.DEFAULT + Alist[Q_INDEX])
            INCORRECT += 1
            print('')
            del Qlist[Q_INDEX]
            del Alist[Q_INDEX]
            raw_input('Press Enter to continue...')

    subprocess.call('clear',shell=True)
    print('')
    i += 1
    Score = float(CORRECT) / float(i)
    DISPLAY_SCORE = ('%.2f' % (Score))
    print('Final Score = ' + commandColors.CYAN + DISPLAY_SCORE)
    print commandColors.DEFAULT
    connection.close()
    COMMIT_HISTORY(STACK, STARTD, STARTT, DISPLAY_SCORE)
    raw_input('Press Enter to continue...')

def TEST3(STACK):

    Qlist = []
    Alist = []

    STARTD=(time.strftime("%Y-%m-%d"))
    STARTT=(time.strftime("%H:%M:%S"))

    CORRECT = 0
    INCORRECT = 0
    SCORE = 0.0

    # Populate Qlist and Alist with questions and answers

    DATABASE = CMD_STACKS + '/' + STACK + '.db'
    connection = sqlite3.connect(DATABASE)
    troll = connection.cursor()
    troll.execute('SELECT Question FROM main')
    for row in troll.fetchall():
        Qlist.append(row[0])
    troll.execute('SELECT Answer FROM main')
    for row in troll.fetchall():
        Alist.append(row[0])

    if len(Qlist) == 0:
        print('You must populate this stack with questions prior to testing.')
        time.sleep(1)
        MAIN_MENU(0)

    QUIZ_SIZE = len(Qlist)

    for i in range(0, len(Qlist)):

        Q_INDEX = i
        subprocess.call('clear',shell=True)
        # Header
        if i == 0:
            print commandColors.WHITE + \
            ('Total %d | Correct %d | Answered %d' % (QUIZ_SIZE,CORRECT,i)) \
            + commandColors.DEFAULT
        else:
            Score = float(CORRECT) / float(i)
            print commandColors.WHITE + \
            ('Total %d | Correct %d | Answered %d | Score ' % (QUIZ_SIZE,CORRECT,i)) \
            + commandColors.CYAN + '%.2f' % (Score) + commandColors.DEFAULT
        print('')

        print Qlist[Q_INDEX]
        user_response = raw_input(' ~> ')
        if user_response == Alist[Q_INDEX]:
            print('')
            print(':-)')
            CORRECT += 1
            time.sleep(.5)
        else:
            print('')
            print(commandColors.RED + 'Incorrect' + commandColors.DEFAULT)
            print(commandColors.WHITE + 'Correct Answer: ' \
            + commandColors.DEFAULT + Alist[Q_INDEX])
            INCORRECT += 1
            print('')
            raw_input('Press Enter to continue...')

    subprocess.call('clear',shell=True)
    print('')
    i += 1
    Score = float(CORRECT) / float(i)
    DISPLAY_SCORE = ('%.2f' % (Score))
    print('Final Score = ' + commandColors.CYAN + DISPLAY_SCORE)
    print commandColors.DEFAULT
    connection.close()
    COMMIT_HISTORY(STACK, STARTD, STARTT, DISPLAY_SCORE)
    raw_input('Press Enter to continue...')



def COMMIT_HISTORY(STACK, STARTD, STARTT, DISPLAY_SCORE):
    TEST_HISTORY = (CMD_HISTORY + '/' + STACK + '.db')
    if not os.path.isfile(TEST_HISTORY):
        connection = sqlite3.connect(TEST_HISTORY)
        troll = connection.cursor()
        troll.execute('CREATE TABLE main (DATE TEXT, TIME TEXT, SCORE TEXT)')
        connection.commit()
        connection.close()

    connection = sqlite3.connect(TEST_HISTORY)
    troll = connection.cursor()
    troll.execute('INSERT INTO main VALUES (?, ?, ?)', (STARTD, STARTT, str(DISPLAY_SCORE)))
    connection.commit()
    connection.close()

def DELETE(STACK):
    TARGET_STACK = CMD_STACKS + '/' + STACK + '.db'
    CHECK_MARKER = CMD_STACKS + '/' + STACK

    subprocess.call('clear',shell=True)
    print('')
    print commandColors.RED + 'Are you sure you want to PERMANENTLY delete stack ' + STACK + '?'
    print('Type \'YES\' to remove, \'exit\' to abort.')
    print commandColors.DEFAULT + ('')
    ACTION = raw_input(' ~> ')
    if ACTION == 'YES':

        print commandColors.RED + 'DELETING',
        time.sleep(.25)
        print'.',
        time.sleep(.25)
        print'.',
        time.sleep(.25)
        print'.' + commandColors.DEFAULT

        if os.path.isfile(TARGET_STACK):
            os.remove(TARGET_STACK)
        if os.path.isfile(CHECK_MARKER):
            os.remove(CHECK_MARKER)
    elif ACTION == 'exit':
        MAIN_MENU(0)
    else:
        print commandColors.RED + ACTION + ' is not a recognized response.'
        time.sleep(1)
        DELETE(STACK)
    
def MAIN_MENU(EXPANDED):
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
        'A stack must be checked out first.'
        print 'Use' + commandColors.CYAN + ' select ' \
        + commandColors.RED + 'for checkout.'
        time.sleep(1.5)
        subprocess.call('clear',shell=True)
        MAIN_MENU(0)


    def MENU_SIMPLE():
        print \
        commandColors.WHITE + 'Welcome to CommandTest - Stack: ' + \
        STYLE + STACK + commandColors.DEFAULT
        print('')
        print('Options:')
        print('')
        print('    test                             select')
        print('    history                          create')
        print('    view                             populate')
        print('    search                           prune')
        print('    settings                         delete')
        print('    help                             exit')
        print ('')

    def MENU_LONG():
        print \
        commandColors.WHITE + 'Welcome to CommandTest - Stack: ' + \
        STYLE + STACK + commandColors.DEFAULT
        print('')
        print('Options:')
        print('')
        print('    test     | Start test            select   | Switch stacks')
        print('    history  | View test history     create   | Create new stack')
        print('    view     | View stack contents   populate | Add questions to stack')
        print('    search   | Query stack           prune    | Remove questions from stack')
        print('    settings | Change settings       delete   | Delete this stack')
        print('    help                             exit')
        print ('')

    if EXPANDED == 0:
        MENU_SIMPLE()
    if EXPANDED == 1:
        MENU_LONG()

    OPTION = raw_input(' ~> ')

    if OPTION == 'test':
        if STACK == 'NONE':
            PRINT_WARN()
        else:
            TEST3(STACK)
    elif OPTION == 'history':
        if STACK == 'NONE':
            PRINT_WARN()
        else:
            HISTORY(STACK)
    elif OPTION == 'view':
        if STACK == 'NONE':
            PRINT_WARN()
        else:
            DISPLAY(STACK)
    elif OPTION == 'search':
        if STACK == 'NONE':
            PRINT_WARN()
        else:
            QUERY(STACK)
    elif OPTION == 'settings':
        SETTINGS()
    elif OPTION == 'help':
        MAIN_MENU(1)
    elif OPTION == 'select':
        CHECKOUT_STACK()
    elif OPTION == 'create':
        STACK = CREATE_STACK()
        CLEAR_CHECKOUT()
        open(CMD_STACKS + '/' + STACK, 'w').close
    elif OPTION == 'populate':
        if STACK == 'NONE':
            PRINT_WARN()
        else:
            POPULATE(STACK)
    elif OPTION == 'prune':
        if STACK == 'NONE':
            PRINT_WARN()
        else:
            PRUNE(STACK)
    elif OPTION == 'delete':
        if STACK == 'NONE':
            PRINT_WARN()
        else:
            DELETE(STACK)
    elif OPTION == 'exit':
        exit()
    elif OPTION == 'clear':
        MAIN_MENU(0)
    else:
        print commandColors.RED + OPTION + \
        ' is not a valid option.' + commandColors.DEFAULT
        time.sleep(1)

    subprocess.call('clear',shell=True)
    if EXPANDED == 0:
        MAIN_MENU(0)
    else:
        MAIN_MENU(1)

INIT()
BANNER()
time.sleep(.5)
MAIN_MENU(0)

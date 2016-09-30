#!/usr/bin/python

def CREATE_STACK(STACKNAME):
    pass
def CHECKOUT_STACK(STACKNAME):
    pass

def NEW():
    print ("No stacks detected, let's start by creating one.")
    raw_input("Press <enter> to begin.")

    # Create stack
    STACKNAME = raw_input("Type the stack name: ")
    # This currently does not work
    CREATE_STACK(STACKNAME)
    CHECKOUT_STACK(STACKNAME)
    print ("\nDone!\n")
    print ("Now that you have a stack, consider populating it with questions so you can take a test!\n")



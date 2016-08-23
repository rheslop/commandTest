#!/bin/bash
. /opt/cmdTest/cmdtest.conf

function NEW {
echo "No stacks detected, Let's start by creating one."
echo "Press <enter> to begin."
read

# Create stack
############
echo "Type the stack name:"
echo ""
read -p "CREATESTACK > " STACKNAME
CREATE_STACK $STACKNAME
CHECKOUT_STACK $STACKNAME
echo ""
echo "Done!"
echo ""
###########

echo "Now that you have a stack, consider populating it with questions so you can take a test!"
echo ""

$STACKMANAGER
/opt/cmdTest/cmdtest.sh
}


function mainWrapper {

clear
echo -n -e "\e[37;40mWelcome to cmdTest - "
case $STACKERR in
0)
echo -e "Stack: \E[0;36;40m$CHECKED_STACK\E[0m"
;;
1)
echo -e "Stack: \E[0;31;40mNone\E[0m"
;;
esac
echo ""
echo "Options:"
echo ""
echo -e "1.\tStart test"
echo -e "2.\tReview History"
echo -e "3.\tDisplay information"
echo -e "4.\tManage Stacks"
echo -e "5.\tView readme"
echo -e "6.\tQuit"
echo ""

read -p "Main ~> " COMMAND
case $COMMAND in
1|test)
	TEST
	mainWrapper
;;
2)
	GET_HISTORY
	mainWrapper
;;
3|getinfo)
	GETINFO
	mainWrapper
;;
4|stackManager)
	$STACKMANAGER
	mainWrapper
;;
5|readme)
	less $README
	clear
	mainWrapper
;;
6|exit|quit)
	echo ""
	exit
;;
*)
	echo -e "\E[31;m\"$COMMAND\" is not a valid option.\E[0;m"
	sleep 1
	mainWrapper
;;
esac

}

[ "$(ls -A $CMD_STACKS)" ] && mainWrapper || NEW


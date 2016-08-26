#!/bin/bash

if [[ $UID -ne 0 ]]; then
	echo "This script must be run as root."
	exit
fi


INSTALL_DIR=/opt/cmdTest

if [ "$1" == "" ]; then
	echo "For this installation to be successfull, ensure the following:"
	echo
	echo "-----------------------------------------------------------------"
	echo " * bc is installed"
	echo " * sqlite is installed"
	echo -e " * There is \E[0;36mnot\E[0m another package named \E[0;36mcmdtest\E[0m currently installed,"
	echo "   as this may cause conflicts."
	echo "-----------------------------------------------------------------"
	echo
	read -p "Continue installation? [y|n] " RESPONSE

	case $RESPONSE in
		y|Y)
			mkdir -p $INSTALL_DIR
			cp ./cmdtest.conf $INSTALL_DIR && chmod 744 $INSTALL_DIR/cmdtest.conf
			cp ./cmdtest.sh $INSTALL_DIR && chmod 755 $INSTALL_DIR/cmdtest.sh
			cp ./stackManager $INSTALL_DIR && chmod 755 $INSTALL_DIR/stackManager
			cp ./README $INSTALL_DIR && chmod 744 $INSTALL_DIR/README
			cp ./LICENSE $INSTALL_DIR && chmod 744 $INSTALL_DIR/LICENSE
			ln -sf $INSTALL_DIR/cmdtest.sh /usr/bin/cmdtest
		
		;;
		n|N)
			echo "Exiting."
			exit
		;;
		*)
			echo "$RESPONSE is not a valid response. Exiting."
		;;
	esac
else
	if [ $1 == uninstall ]; then
		rm -rf $INSTALL_DIR
		rm -rf /usr/bin/cmdtest
	else
		echo "$1 is not a recognized option."
	fi
fi


#!/bin/bash

if [[ $UID -ne 0 ]]; then
	echo "This script must be run as root."
	exit
fi

INSTALL_DIR=/opt/commandTest

if [ "$1" == "" ]; then

	mkdir -p $INSTALL_DIR
	cp ./ct.py $INSTALL_DIR && chmod 755 $INSTALL_DIR/ct.py
	cp ./README $INSTALL_DIR && chmod 744 $INSTALL_DIR/README
	cp ./LICENSE $INSTALL_DIR && chmod 744 $INSTALL_DIR/LICENSE
	ln -sf $INSTALL_DIR/ct.py /usr/bin/ct
		
else
	if [ $1 == uninstall ]; then
		rm -rf $INSTALL_DIR
		rm -rf /usr/bin/ct
	else
		echo "$1 is not a recognized option."
	fi
fi


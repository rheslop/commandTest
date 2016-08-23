#!/bin/bash

if [[ $UID -ne 0 ]]; then
	echo "This script must be run as root."
	exit
fi

INSTALL_DIR=/opt/cmdTest

if [ "$1" == "" ]; then
	yum -y install bc
	mkdir -p $INSTALL_DIR
	cp ./cmdtest.conf $INSTALL_DIR && chmod 744 $INSTALL_DIR/cmdtest.conf
	cp ./cmdtest.sh $INSTALL_DIR && chmod 755 $INSTALL_DIR/cmdtest.sh
	cp ./stackManager $INSTALL_DIR && chmod 755 $INSTALL_DIR/stackManager
	cp ./README $INSTALL_DIR && chmod 744 $INSTALL_DIR/README
	cp ./LICENSE $INSTALL_DIR && chmod 744 $INSTALL_DIR/LICENSE
	ln -sf $INSTALL_DIR/cmdtest.sh /usr/bin/cmdtest
else
	if [ $1 == uninstall ]; then
		rm -rf $INSTALL_DIR
		rm -rf /usr/bin/cmdtest
	else
		echo "$1 is not a recognized option."
	fi
fi


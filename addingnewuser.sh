#!/bin/bash
# Script to add a user to Linux system
if [ $(id -u) -eq 0 ]; then
    read -p "Enter username : " username
    read -s -p "Enter password : " password
    egrep "^$username" /etc/passwd >/dev/null
    if [ $? -eq 0 ]; then
        echo "$username exists!"
        exit 1
    else
        pass=$(perl -e 'print crypt($ARGV[0], "password")' $password)
        useradd -m -p $pass $username
        [ $? -eq 0 ] && echo "User has been added to system!" || echo "Failed to add a user!"
    fi
else
    echo "Only root may add a user to the system"
    exit 2
fi



#####################################################################################################

#!/bin/bash


#Author: Raj
#Version: 1.1

if [ $(id -u) -eq 0]                 # id -u returns the userid # of the user. 0 is for root

then

echo "Enter the username to add to the system"
read username					

echo "Checking the system if username exits ......"

sleep 2

egrep "^$username" /etc/passwd > /dev/null

if [ $? -eq 0 ]					# the exit code of the last command "egrep"

then

        echo "$username already exists!"

        exit 1					# your own exit code. will print the message with exit code of 1.

else

        echo "Adding $username as a new user"

fi


echo "Would you like to set up a password for $username right now? Enter either yes or no"

read answer

input=${answer,,}

if [ "$input" = "yes" ]

then

useradd -m  $username

passwd $username


[ $? -eq 0 ] && echo " User $username has been added to the system." || echo "Failed to add user $username to the system."

else

useradd $username

[ $? -eq 0 ] && echo " User $username has been added to the system." || echo "Failed to add user $username to the system."

fi

else 

echo "Only root can add user to the system"

fi
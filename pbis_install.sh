#!/bin/bash

if [[ $EUID -ne 0 ]]
then
    echo "This script must be run as root" 2>&1
    exit 1
else

    PBISDIR="/opt/pbis"
    PBISVERSION=`/opt/pbis/bin/pbis-status | grep -i "Compiled daemon version" | awk '{print($4)}'`
    OS=`lsb_release -a | grep -i description`

    if [ -d "$PBISDIR" ]
    then
        echo "PBIS is installed. Checking PBIS version...."
        sleep 2
        echo "The installed version is $PBISVERSION"
        echo "Update PBIS to lastest version? (Y/N)."
        read input
        if [ $input == "y" ] || [ $input == "Y" ]
        then
            if [[ $OS == *"Ubuntu"* ]]
            then
                echo "Ubuntu OS System Found"
				sleep 2
                `wget -O - http://repo.pbis.beyondtrust.com/yum/RPM-GPG-KEY-pbis|sudo apt-key add -`
                sudo wget -O /etc/apt/sources.list.d/pbiso.list http://repo.pbis.beyondtrust.com/apt/pbiso.list
                LATEST_VERSION=`apt-cache madison pbis-open | awk '{print($3)}'`
                if [ $LATEST_VERSION == $PBISVERSION ]
                then
                    echo "You already have the latest version of PBIS installed"
                    sleep 2
                else
                    sudo apt-get update
                    sudo apt-get --assume-yes install pbis-open
                fi

            else
                echo "Redhat OS System Found"
				sleep 2
                `wget -O /etc/yum.repos.d/pbiso.repo http://repo.pbis.beyondtrust.com/yum/pbiso.repo`
                LATEST_VERSION=`yum --showduplicates list pbis-open | grep -i -A 1 "Available Packages" | awk 'FNR==2{print($2)}'`
                if [ $LATEST_VERSION == $PBISVERSION ]
                then
                    echo "You already have the latest version of PBIS installed"
                    sleep 2
                else
                    yum clean all
                    yum install -y pbis-open
                fi
            fi

        elif [ $input == "n" ] || [ $input == "N" ]
        then
            echo "Good Bye.."
        else
            echo "You didn't enter either Y or N"
        fi

    else
        echo "PBIS is not installed"
        echo "Install PBIS? (Y/N)"
        read input
		if [ $input == "y" ] || [ $input == "Y" ]
        then
            if [[ $OS == *"Ubuntu"* ]]
            then
                echo "Ubuntu OS System Found"
                `wget -O - http://repo.pbis.beyondtrust.com/yum/RPM-GPG-KEY-pbis|sudo apt-key add -`
                sudo wget -O /etc/apt/sources.list.d/pbiso.list http://repo.pbis.beyondtrust.com/apt/pbiso.list
                sudo apt-get update
                sudo apt-get --assume-yes install pbis-open
            else
                echo "Redhat OS System Found"
                `wget -O /etc/yum.repos.d/pbiso.repo http://repo.pbis.beyondtrust.com/yum/pbiso.repo`
                yum clean all
                yum install -y pbis-open
            fi
        elif [ $input == "n" ] || [ $input == "N" ]
        then
            echo "Good Bye.."
        else
            echo "You didn't enter either Y or N"
        fi
    fi
fi


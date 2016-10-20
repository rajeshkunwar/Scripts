#!/usr/bin/env python

import sys
import os # good for running shell commands
import time
import subprocess # better for storing shell output to a variable instead of using os.system

#Method to check pbis dir

def pbisDir():
        dir = "/opt/pbis"
        return os.path.isdir(dir)       # Returns True/False value

# Method to check the pbis version

def pbisVersion():
        pbisVersion = "/opt/pbis/bin/pbis-status | grep -i 'Compiled daemon version' | awk '{print($4)}'"
        pbisVersion = subprocess.Popen(pbisVersion, stdout=subprocess.PIPE,shell=True)
        output, err = pbisVersion.communicate()
        print "The installed PBIS version is:", output

#Method for redhat install

def redhatInstall():
        repo = "wget -O /etc/yum.repos.d/pbiso.repo http://repo.pbis.beyondtrust.com/yum/pbiso.repo"
        repo = subprocess.Popen(repo, stdout=subprocess.PIPE,shell=True)
        repo, err = repo.communicate()
        os.system("yum clean all")
        os.system("yum install -y pbis-open")

#Method for ubuntu install

def ubuntuInstall():
        os.system("wget -O - http://repo.pbis.beyondtrust.com/yum/RPM-GPG-KEY-pbis|sudo apt-key add -")
        os.system("sudo wget -O /etc/apt/sources.list.d/pbiso.list http://repo.pbis.beyondtrust.com/apt/pbiso.list")
        os.system("sudo apt get update && sudo apt-get --assume-yes install pbis-open")

if not os.geteuid() == 0:
        sys.exit('Script must be run as root')

else:
        osType = "lsb_release -a | grep -i 'description'"
        osType = subprocess.Popen(osType, stdout=subprocess.PIPE,shell=True)
        output, err = osType.communicate()

        if "Red Hat" in output:        
                print "Redhat system found"
                time.sleep(2)

                if pbisDir() == True:
                        print "PBIS is installed. Checking PBIS version......"
                        time.sleep(2)
                        pbisVersion()
                        answer = raw_input("Update PBIS to latest version? (Y/N)").lower()  

                        if answer == "y" or answer == "yes":
                                redhatInstall()   # Calling the redhatInstall method

                else:
                        answer = raw_input("PBIS is not installed. Would you like to install it? (Y/N)").lower()

                        if answer == "y" or answer == "yes":
                                redhatInstall()

        elif "Ubuntu" in output:
                print "Ubuntu system found"
                time.sleep(2)

                if pbisDir() == True:
                        print "PBIS is installed. Checking PBIS version......."
                        time.sleep(2)
                        pbisVersion()
                        answer = raw_input("Update PBIS to latest version? (Y/N)").lower()

                        if answer == "y" or answer == "yes":
                                ubuntuInstall()

                else:
                        answer = raw_input("PBIS is not installed. Would you like to install it? (Y/N)").lower()

                        if answer == "y" or answer == "yes":
                                ubuntuInstall()

        else:
                print "OS not supported"

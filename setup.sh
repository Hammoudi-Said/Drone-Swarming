
# Python3 Installation
if [ `command -v command` ]; then
    echo "Python3 already installed"
else
  echo "python installation"
    sudo apt-get install software-properties-common
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get -y install python3.8
fi

# Pip3 Installation
if [ `command -v pip3` ]; then
  echo "pip3 already installed"
else
  sudo apt install -y python3-pip
fi

# Install python modules

# djitellopy
#python3 -c "import djitellopy"
#if [ $? == 0 ]; then
#  echo "djitellopy already exist"
#else
#  pip3 install -y djitellopy
#fi

# platform
python3 -c "import platform"
if [ $? == 0 ]; then
  echo "platform already exist"
else
  pip3 install -y lib-platform
fi

# regex
python3 -c "import re"
if [ $? == 0 ]; then
  echo "regex already exist"
else
  pip3 install -y regex
fi

# logging
python3 -c "import logging"
if [ $? == 0 ]; then
  echo "logging already exist"
else
  pip3 install -y logging
fi

#time
python3 -c "import time"
if [ $? == 0 ]; then
  echo "time already exist"
else
  pip3 install -y python3-time
fi

# nmap
python3 -c "import nmap"
if [ $? == 0 ]; then
  echo "nmap already exist"
else
  pip3 install -y python3-nmap
fi

# socket
python3 -c "import socket"
if [ $? == 0 ]; then
  echo "socket already exist"
else
  pip3 install -y socket.py
fi

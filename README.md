# Drone-Swarming
This project aims at creating an experimental setup for Multi-Agent Systems (MAS), namely a swarm of Tello Edu Drones.

* First task was to work on automation of the configuration of drones by script: connect tello drone to pc, be sure that the drone works,
then send command to connect tello drone to the router and finally get all tello ip address. With `conf.py` you are able to configure as many tello drones as you want.

![configuration prototype](./img/swarm.png)
# Installation
The instructions below work on Linux and similar operating systems.

#### Clone this repository
```bash
git clone https://github.com/hammoudipro/Drone-Swarming.git
```

#### Change directory
```bash
cd Drone-Swarming
```

#### Install python3 and all needed modules
The file `setup.sh` is responsible for the python setup.
- First we need to give execute permissions to `setup.sh`
```bash
chmod +x setup.sh
```
- Then execute script bash
```bash
./setup.sh
```

## Usage

#### Tello drone configuration
Before we execute the configuration script, be sure that all tello drones that you want to configure 
are switch on, and Tello's Wi-Fi are detected (e.g. Tello-AB89C4) by your laptop. 

- We need the **name**, **ssid**, **password** and **netmask** (by default netmask is set to 24) of the router 

```python3
from conf import *
from djitellopy import TelloSwarm

def swarm_example():
    # create, initialize a configuration and save it in a variable for later
    # change the parameter with your router's parameter
    conf = Configuration('router_name', 'router_ssid', 'router_password', router_netmask)
    # run tello configuration script
    conf.run()
    if conf.get_tello_ip_swarm() is None:
        logging.error("There is no available Tello drone")
        return
    # create swarm  drone with available tello ip that we recover from conf variable
    swarm = TelloSwarm.fromIps(conf.get_tello_ip_swarm())
    swarm.connect()
    swarm.takeoff()
    swarm.move_forward(20)
    swarm.land()
    swarm.end()
```

- Execute script drone swarm example
```bash
python3 main.py
```
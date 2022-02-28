# This is a sample Python script.

from conf import *
from djitellopy import TelloSwarm

def swarm_example():
    # create, initialize a configuration and save it in a variable for later
    # change the parameter with your router's parameter
    conf = Configuration('redme007', 'redme007', 'motdepasse', 24)
    # run tello configuration script
    ip = conf.run()

    # create swarm  drone with available tello ip that we recover from conf variable
    swarm = TelloSwarm.fromIps(ip)
    swarm.connect()
    swarm.takeoff()

    swarm.move_forward(30)
    swarm.move_down(30)
    swarm.sequential(lambda i, tello: tello.move_up(i * 10 + 20))
    swarm.sequential(lambda i, tello: tello.move_down(i * 10 + 20))
    swarm.rotate_clockwise(180)
    swarm.move_forward(30)
    swarm.move_up(40)
    swarm.move_down(40)

    swarm.land()
    swarm.end()

if __name__ == '__main__':
    swarm_example()

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from conf import *
from djitellopy import TelloSwarm


def swarm_example():
    # create and initialize a configuration
    conf = Configuration('redme007', 'redme007', 'motdepasse', 24)
    conf.run()
    if conf.get_tello_ip_swarm() is None:
        logging.error("There is no available Tello drone")
        return
    swarm = TelloSwarm.fromIps(conf.get_tello_ip_swarm())
    swarm.connect()
    swarm.takeoff()
    swarm.move_forward(20)
    swarm.land()
    swarm.end()


if __name__ == '__main__':
    swarm_example()

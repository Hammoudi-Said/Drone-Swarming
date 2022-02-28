import pickle
import threading
import time

from djitellopy import Tello, TelloSwarm

from conf import Configuration


#ip = ['192.168.33.147', '192.168.33.200', '192.168.33.213', '192.168.33.251', '192.168.33.38', '192.168.33.6', '192.168.33.75']

def get_satate_background(swarm, path):
    """Start a process in background to get current state of each tello
    :swarm: a swarm of tello
    :path: path where to save data
    """
    for tello in swarm:
        thread = threading.Thread(name='background_state', target=tello.get_current_state_always, args=(path,))
        thread.daemon = True
        thread.start()





def swarm_example():
    conf = Configuration('redme007', 'redme007', 'motdepasse', 24)
    ip = conf.getTelloIp()
    swarm = TelloSwarm.fromIps(ip)
    swarm.connect()
    print("enable mission pad ...")
    swarm.enable_mission_pads()
    swarm.set_mission_pad_detection_direction(0)
    # for tello in swarm:
    #     tello.enable_mission_pads()
    #     tello.set_mission_pad_detection_direction(0)

    swarm.takeoff()
    get_satate_background(swarm, "/home/hammoudi/Documents/M2/PFE/Drone-Swarming")
    swarm.move_down(30)
    swarm.sequential(lambda i, tello: tello.move_up(i * 10 + 20))

    swarm.sequential(lambda i, tello: tello.move_down(i * 10 + 20))
    swarm.move_up(40)
    swarm.move_down(40)

    print("disable mission pad ...")
    swarm.disable_mission_pads()
    swarm.land()
    swarm.end()



if __name__ == '__main__':
    swarm_example()




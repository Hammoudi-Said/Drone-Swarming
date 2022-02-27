import os
import platform
import re
import logging
import sys
import nmap
import socket, struct

from djitellopy import Tello


class Configuration(object):
    """
    Tello network configuration and automation
    """
    def __init__(self, router_name, SSID_router, password, netmask=24):
        """

        :param SSID_router: the name of router that all drones will connect
        :param password: of the router
        :param netmask: int , the netmask of the router. To find the netmask you should connect to the router then in terminal tap 'ip a'
        """
        self.ssid = SSID_router
        self.name = router_name
        self.password = password
        self.netmask = netmask
        self.dronePrefixName = 'TELLO'
        self.tello_ip_swarm = None
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

    def get_tello_ip_swarm(self):
        """
        :return: list drone ip
        """
        return self.tello_ip_swarm

    def displayAvailableNetworks(self):
        """
        display available networks
        :return: list of available networks
        """
        if platform.system() == "Windows":
            command = "netsh wlan show networks interface=Wi-Fi"
        elif platform.system() == "Linux":
            command = "nmcli dev wifi list"
        list_of_networks = os.popen(command).read()
        logging.info('Available networks : \n %s \n' % list_of_networks)
        return list_of_networks

    def find_tello_network(self):
        """
        this function display available network and search all network that their ssid begin with dronePrefixName
        :return: list of tello networks name
        """
        logging.info(f'Searching for tello network which network name prefix begin with: {self.dronePrefixName}')
        netwoks = str(self.displayAvailableNetworks())
        tellos = re.findall(self.dronePrefixName + "-\w+", netwoks)
        logging.info('Available tello network name  : \n %s \n' % tellos)
        return tellos

    def createNewConnection(self,name, SSID, key):
        """
        this function create initialize a new connection
        :param name: network name
        :param SSID: netork ssid
        :param key: password
        :return: None
        """
        config = """<?xml version=\"1.0\"?>
    <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
        <name>""" + name + """</name>
        <SSIDConfig>
            <SSID>
                <name>""" + SSID + """</name>
            </SSID>
        </SSIDConfig>
        <connectionType>ESS</connectionType>
        <connectionMode>auto</connectionMode>
        <MSM>
            <security>
                <authEncryption>
                    <authentication>WPA2PSK</authentication>
                    <encryption>AES</encryption>
                    <useOneX>false</useOneX>
                </authEncryption>
                <sharedKey>
                    <keyType>passPhrase</keyType>
                    <protected>false</protected>
                    <keyMaterial>""" + key + """</keyMaterial>
                </sharedKey>
            </security>
        </MSM>
    </WLANProfile>"""
        if platform.system() == "Windows":
            command = "netsh wlan add profile filename=\"" + name + ".xml\"" + " interface=Wi-Fi"
            with open(name + ".xml", 'w') as file:
                file.write(config)
        elif platform.system() == "Linux":
            command = "nmcli dev wifi connect '" + SSID + "' password '" + key + "'"
        logging.info(f'Inialize a new conection with nam : {name} and ssid: {SSID}.\n')
        os.system(command)
        if platform.system() == "Windows":
            os.remove(name + ".xml")

    def connect_to_network(self ,name, SSID):
        """
        function that allow connection to network with the name and ssid given in parameter
        :param name: network name
        :param SSID: network ssid
        :return: None
        """
        logging.info(f'connect to network with name: {name} and ssid: {SSID} \n')
        if platform.system() == "Windows":
            command = "netsh wlan connect name=\"" + name + "\" ssid=\"" + SSID + "\" interface=Wi-Fi"
        elif platform.system() == "Linux":
            command = "nmcli con up " + SSID
        os.system(command)

    def check_wifi_connection(self, wifiSSID):
        """
        Verify if the local machine is connected to wifiName.
        It returns true it's connected, false otherwise
        :param wifiName: name of the wifi where we want to connect the local machine
        :return: boolean
        """
        logging.info(f'check if local machine is connected to {wifiSSID} ...\n')
        if platform.system() == "Windows":
            raise Exception("The command is not supported by windows system, only linux system\n")
        elif platform.system() == "Linux":
            command = "nmcli device wifi show | grep SSID"
        logging.info(f'command: {command} \n')
        SSID = os.popen(command).read()
        logging.info(f'Actual wifi : {SSID} \n')
        SSID_name = SSID.split(':')[1]
        if wifiSSID.strip().lower() == SSID_name.strip().lower():
            return True
        return False

    def get_local_ip_address(self):
        """
        return the ip address
        :return: string ip addr
        """
        logging.info(f'Searching for local ip address ... \n')
        hostnames = os.popen('hostname -I').read()
        ip = hostnames.split(' ')[0]
        logging.info(f'Local ip address : {ip} ... \n')
        return ip

    def networkScanner(self, ip):
        """
        Scan the ip address and return list ip devices which are connected to the router
        :param ip: the ip address
        :return: list of subnet
        """
        logging.info(f'Scanning the network with ip: {ip} \n')
        logging.info(f'Scanning please wait ...\n')
        print("Scanning please wait ...")
        nm = nmap.PortScanner()
        nm.scan(hosts=ip, arguments='-sn')
        hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
        networks = []
        for host, status in hosts_list:
            networks.append(host)
            logging.info("Host\t{} {}".format(host, status))
        return networks

    def getTelloIp(self):
        """
        Scan all devices connected to the router and return tello drone's ip
        :return: list ip of all tello drone connected to the router
        """
        logging.info("Scanning Tello ip address that are connected to the router")
        host = self.get_local_ip_address()
        # scanning devices connected to the router
        tello_ip = self.networkScanner(f'{host}/{str(self.netmask)}')
        logging.info(f'All devices ip: {tello_ip}')
        # remove host ip
        logging.info(f"Remove host ip ({host}) from all devices ")
        tello_ip.remove(host)
        # remove default gateway
        if platform.system() == 'Linux':
            default_gateway = self.get_default_gateway_linux()
            if default_gateway in tello_ip:
                tello_ip.remove(default_gateway)
                logging.info(f"Remove default gateway ({default_gateway}) from all devices ")

        logging.info(f'Tello ip : {tello_ip}')
        return tello_ip

    def find_available_network(self, num):
        """

        """
        print(f'[Start_Searching]Searching for {num} available Tello...\n')
        tello_network_name = self.find_tello_network()
        if not tello_network_name:
            print(f'There is {len(tello_network_name)} available Tello network detected')
            print(f'Do you want to rescan ? Y/N ...')
            resp = input()
            if resp.strip().lower() == 'y' or resp.strip().lower() == 'yes':
                return self.find_available_network(num)
            else:
                sys.exit()
        elif len(tello_network_name) < num:
            print(f'There is {len(tello_network_name)} available Tello network detected')
            print(f'Do you want to continue ? Y/N ...')
            resp = input()
            if resp.strip().lower() == 'y' or resp.strip().lower() == 'yes':
                return tello_network_name
            else:
                sys.exit()
        elif len(tello_network_name) > num:
            print(f'There is {len(tello_network_name)} available Tello network detected')
            print(f'Do you want to continue with {len(tello_network_name)} drones ? Y/N ... ')
            resp = input()
            if resp.strip().lower() == 'y' or resp.strip().lower() == 'yes':
                return tello_network_name
            else:
                tello_network_name = tello_network_name[:num]
                return tello_network_name

        elif num == len(tello_network_name):
            return tello_network_name

    # https://stackoverflow.com/questions/2761829/python-get-default-gateway-for-a-local-interface-ip-address-in-linux/6556951
    def get_default_gateway_linux(self):
        """Read the default gateway directly from /proc."""
        with open("/proc/net/route") as fh:
            for line in fh:
                fields = line.strip().split()
                if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                    # If not default route or not RTF_GATEWAY, skip it
                    continue

                return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))



    def run(self):
        """
        this function run the script configuration
        """
        # choose number of drone to configure
        while True:
            try:
                num = int(input('Please, put the number of drone that you want to configure ?'))
                break
            except:
                print("That's not a number!")
        BATTERY_MIN = 20
        logging.info("Running configuration script ...")
        tello_network_name = self.find_available_network(num)
        # if tello_network_name == []:
        #     logging.warning("There is no available tello drone detected, Please reboot the tello drone ..")
        #     return
        print(f'Available tello network name : {tello_network_name}')
        drone_up = []
        drone_down = []
        tello = Tello()
        for net in tello_network_name:
            logging.info(f'Try to connect tello drone with network name {net} to local machine')
            self.createNewConnection(str(net), str(net), "")
            self.connect_to_network(str(net), str(net))
            if self.check_wifi_connection(str(net)):
                tello.connect()
                battery = tello.get_battery()
                logging.info(f'{net} battery : {battery}')
                if battery > BATTERY_MIN:
                    drone_up.append(tello.query_serial_number())
                    tello.connect_to_wifi(self.ssid, self.password)
                else:
                    print(f'Getting serial number of defected drone {net}.')
                    drone_down.append(tello.query_serial_number())
                    logging.warning(f'The batery of {net} is lower then {BATTERY_MIN}, please change the battery')
        print(f'There is {len(drone_up)} drones working : {drone_up}')
        print(f'There is {len(drone_down)} drones not working with serial number: {drone_down}')
        res = input("Do you want to continue ? Y/N ... ")
        if res.strip().lower() == 'n' or res.strip().lower() == 'No':
            sys.exit()
        logging.info("connecting to router ...\n")

        while not self.check_wifi_connection(self.ssid):
            try:
                self.createNewConnection(self.name, self.ssid, self.password)
                self.connect_to_network(self.name, self.ssid)
            except Exception as err:
                continue

        # if not self.check_wifi_connection(self.ssid):
        #     logging.error(f'Unable to connect to wifi with ssid: {self.ssid} ')
        #     return

        print("searching for tello drone ip")
        tello_ip = self.getTelloIp()
        while len(tello_ip) != len(drone_up):
            print(f'There is {len(tello_ip)} drone connected to the router. It must be {len(drone_up)}')
            res = input("Do you want to rescan ? Y/N ...")
            if res.strip().lower() == 'y' or res.strip().lower() == 'yes':
                tello_ip = self.getTelloIp()
            else:
                break
        self.tello_ip_swarm = tello_ip
        print(f'Connected tello ip : {tello_ip} \n')
        return tello_ip

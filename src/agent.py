#!/usr/bin/python3

import socket
import struct
import sys
import os
import json
import time
import random
import subprocess
import re
import config
import psutil


class UDPAgent:

    def __init__(self, multicast_group, server_ipport):
        self.multicast_group = multicast_group
        self.server_port = ("", server_ipport)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    @staticmethod
    def get_info():
        output = subprocess.check_output("lscpu", shell=True)
        output = str(output, "utf-8")

        maxHz = re.findall(r"CPU\smax\sMHz:\s+([0-9]+)", output)
        maxHz = eval(maxHz[0])

        minHz = re.findall(r"CPU\smin\sMHz:\s+([0-9]+)", output)
        minHz = eval(minHz[0])

        usage = os.getloadavg()[0]

        output = subprocess.check_output("cat /proc/meminfo", shell=True).decode()

        memtotal = re.findall(r"MemTotal:\s+([0-9]+)", output)
        memtotal = int(eval(memtotal[0])/1024)

        freemem = re.findall(r"MemFree:\s+([0-9]+)", output)
        freemem = int(eval(freemem[0])/1024)

        avaimem = re.findall(r"MemAvailable:\s+([0-9]+)", output)
        avaimem = int(eval(avaimem[0])/1024)

        return {
                "type": "probe response",
                "maxHz": maxHz,
                "minHz": minHz,
                "usage": usage,
                "totalMem": memtotal,
                "freeMem": freemem,
                "availableMem": avaimem
                }

    @staticmethod
    def get_info_mac():

        (_,minHz,maxHz) = psutil.cpu_freq()
        (memtotal,avaimem,_,_,freemem,_,_,_) = psutil.virtual_memory()
        usage = os.getloadavg()[0]

        return {
                "type": "probe response",
                "maxHz": maxHz,
                "minHz": minHz,
                "usage": usage,
                "totalMem": memtotal,
                "freeMem": freemem,
                "availableMem": avaimem
                }

    def receive(self):
        # Bind to the server address
        self.socket.bind(self.server_port)

        # Tell the operating system to add the socket to the multicast group
        # on all interfaces.
        group = socket.inet_aton(self.multicast_group)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        # Receive/respond loop
        while True:
            print('\nWaiting to receive message')
            data, address = self.socket.recvfrom(1024)

            try:
                msg_info = json.loads(data.decode())

                print('Received', msg_info, 'from', address[0])
                info = {}
                if ('type' in msg_info) and (msg_info['type'] == 'probe request'):
                    if 'time' in msg_info:
                        if sys.platform == "linux" or sys.platform == "linux2":
                            info = self.get_info()
                        elif sys.platform == "darwin":
                            info = self.get_info_mac()
                            print("Sou um mac")
                        info["sentTime"] = msg_info["time"]

                        print('Information: ', info)
                        # don't send them all at once, each sleeps for a litle
                        ms = random.randint(0, 10)
                        time.sleep(ms/1000.0)
                        self.socket.sendto(bytes(json.dumps(info), "utf-8"), address)
                    else:
                        print("Erro, msg não contem elemento time")
                else:
                    print("Erro, msg não type não encontrado/incorreto")
            except json.decoder.JSONDecodeError:
                print("Erro, mensagem não vem em JSON")


def main():
    ip = config.udp_ip
    port = config.udp_port

    # create monitor instance
    agente = UDPAgent(ip, port)

    # start monitor
    agente.receive()


if __name__ == "__main__":
    main()

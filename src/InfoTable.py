#!/usr/bin/python3

import socket
import struct
import sys
import json
import pprint

class InfoTable():

    def __init__(self):
        self.dic = {}

    def updateInfo(self,server, info):
        info.update({"port":server[1]})
        self.dic[server[0]] = info

    def printInfo(self):
        pprint.pprint(self.dic)

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
		self.dic[server] = info

	def printInfo(self):
		pprint.pprint(self.dic)
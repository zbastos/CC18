#!/usr/bin/python3

import time
import socket
import sys
import struct
import json
from threading import Thread
import config
import infotable


class UDPMonitor:

	def __init__(self):
		self.multicast_Time = config.refresh
		self.stateTable = infotable.InfoTable()
		self.multicast_group = (config.udp_ip, config.udp_port)
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.timeout = config.timeout

	"""
	Multicast function, will keep running as long as UDPMonitor is up
	"""
	def multicast(self):

		self.socket.settimeout(self.timeout)
		message = {"type": "probe request"}

		try:
			while True:

				# depende das infos da tabela, ir buscar o maior (?) verificar se é necessário
				# ttl = struct.pack('b',1)
				# self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

				try:
					print("Sending broadcast request...")
					message["time"] = time.time()
					print(message)
					self.socket.sendto(bytes(json.dumps(message), "utf-8"), self.multicast_group)

					while True:
						if self.receive_msg() != 0:
							break
				finally:
					print("All connections received, sleeping soon\n")

				time.sleep(self.multicast_Time)

		except InterruptedError:
			print(self.stateTable.print_info())
			self.socket.close()
			print("Closed socket")

	"""
	Receive msg from random multicast server
	"""
	def receive_msg(self):
		print('Waiting to receive')

		try:
			data_b, server = self.socket.recvfrom(1024)  # (?)
			# convert json object to python object
			data_str = str(data_b, "utf-8")
			data = json.loads(data_str)
			# update info from client server
			self.stateTable.update_info(server, data)
		except socket.timeout:
			print("Timed out, no response")
			print('==================')
			return -1
		else:
			print('Received message', data, 'from', server[0])
			print('==================')
			return 0

	def request_server(self):
		return self.stateTable.request_server()

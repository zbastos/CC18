#!/usr/bin/python3

import time
import socket
import sys
import struct
import json
from InfoTable import InfoTable


class UDPMonitor:

	def __init__(self, table, ip, port, m_time, timeout=1):
		self.multicast_Time = m_time
		self.stateTable = table
		self.multicast_group = (ip, port)
		print("Creating socket")
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.timeout = timeout

	"""
			Multicast function, will keep running as long as UDPMonitor is up
	"""
	def multicast(self):

		self.socket.settimeout(self.timeout)
		message = "Update infos"
		try:
			while True:
				# depende das infos da tabela, ir buscar o maior (?) verificar se é necessário
#				ttl = struct.pack('b',1)

#				self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

				try:
					print("Sending broadcast request...")
					sent = self.socket.sendto(bytes(message,"utf-8"), self.multicast_group)

					while True:
						if self.receive_msg() != 0:
							break
				finally:
					print("All connections received, sleeping soon\n")

				time.sleep(self.multicast_Time)

		except KeyboardInterrupt:
			print(self.stateTable.printInfo())
			self.socket.close()
			print("Closed socket")

	"""
	Receive msg from random multicast server
	"""
	def receive_msg(self):
		print('Waiting to receive')

		try:
			dataB, server = self.socket.recvfrom(1024)  # (?)
			# convert json object to python object
			datastr = str(dataB,"utf-8")
			data = json.loads(datastr)
			# update infos from client serer
			self.stateTable.updateInfo(server, data)
		except socket.timeout:
			print("Timed out, no response")
			print('==================')
			return -1
		else:
			print('Received message', data, 'from', server[0])
			print('==================')
			return 0


def main():
	#create info table to store server's info
	ip = "239.8.8.8"

	port = 8888

	time = 10

	print("\nSetting up information table...")

	table = InfoTable()

	print("\nSetting up UDP Monitor...")
	#create monitor instance
	monitor = UDPMonitor(table,ip,port,time)

	print("Starting...")
	#start monitor
	monitor.multicast()


if __name__ == "__main__":
	main()

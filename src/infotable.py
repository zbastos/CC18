#!/usr/bin/python3

import pprint
import time
from statistics import median


class TableEntry:
	def __init__(self, port, info):
		self.port = port
		self.rtt = self.calculate_rtt(info['sentTime'])
		self.rtt_array = [self.rtt]
		self.median_free = info['freeMem']
		self.free_array = [self.median_free]
		self.median_available = info['availableMem']
		self.available_array = [self.median_available]
		self.total_mem = info['totalMem']
		self.median_cpu = info['usage']
		self.median_mem_load = max(self.median_available, self.median_free) / self.total_mem
		self.cpu_array = [self.median_cpu]

	def __eq__(self, other):
		return self.rtt == other.rtt and \
			self.median_mem_load == other.median_mem_load and \
			self.total_mem == other.total_mem

	def __lt__(self, other):
		if self.median_cpu < 1 or other.media_cpu < 1:
			return self.median_cpu < other.media_cpu

		if self.median_mem_load < 0.5 or other.median_mem_load < 0.5:
			return self.median_mem_load < other.median_mem_load

		return self.rtt < other.rtt

	def print(self):
		message = "Port: " + str(self.port) + "\n Rtt (seconds): " + "{0:.5f}".format(self.rtt) + \
			"\n Median Free Mem: " + str(self.median_free) + "\n Median Available Mem: " + \
			str(self.median_available) + "\n Total Mem: " + str(self.total_mem) + "\n Median Cpu: " + \
			"{0:.5f}".format(self.median_cpu)
		return message

	@staticmethod
	def calculate_rtt(t1):
		t2 = time.time()
		return t2-t1

	def update_infos(self, info):
		rtt = self.calculate_rtt(info['sentTime'])
		self.rtt_array.append(rtt)
		self.rtt = median(self.rtt_array)

		self.free_array.append(info['freeMem'])
		self.median_free = median(self.free_array)

		self.available_array.append(info['availableMem'])
		self.median_available = median(self.available_array)

		self.cpu_array.append(info['usage'])
		self.median_cpu = median(self.cpu_array)

		self.median_mem_load = max(self.median_available,self.median_free) / self.total_mem


class InfoTable:

	def __init__(self):
		self.dic = {}

	def update_info(self, server, info):
		# verificar se é a primeira vez que aparece o server
		server_ip = server[0]
		server_port = server[1]

		# update informations
		if server_ip in self.dic:
			self.dic[server_ip].update_infos(info)
		# add new server
		else:
			self.dic[server_ip] = TableEntry(server_port,info)

	def print_info(self):
		for (key, val) in self.dic.items():
			print(key + " -> " + val.print())

	def request_server(self):
		return min(self.dic.items())

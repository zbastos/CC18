#!/usr/bin/python3
from threading import Thread

import config
import monitor
import socket

#TODO finish
def listen_from_client(data, client_socket):
	while True:
		data = client_socket.recv(config.data_size)


def handle_thread(backend_socket, client_socket):
	data = b""
	client_listener = Thread(target=listen_from_client, args=[data, client_socket])
	client_listener.start()
	while True:
		if not data:
			backend_socket.close()
			break
		backend_socket.send(data)
		data = client_socket.recv(config.data_size)


def main():
	udp_monitor = monitor.UDPMonitor()
	monitor_thread = Thread(target=monitor.UDPMonitor.multicast, args=[udp_monitor])
	monitor_thread.start()
	tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	tcp_infos = (config.tcp_ip, config.tcp_port)
	tcp_server.bind(tcp_infos)
	servers = []

	while True:
		tcp_server.listen(config.max)
		print("Waiting for tcp connection")
		(client_socket, (c_ip, c_port)) = tcp_server.accept()
		agent_ip = udp_monitor.request_server()
		print("I chose " + agent_ip[0] + "||" + agent_ip[1].print() + " for a request from " + c_ip)
		backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		backend_socket.connect((agent_ip, config.tcp_port))
		handler = Thread(target=handle_thread, args=[backend_socket, client_socket])
		handler.start()
		servers.append(handler)


if __name__ == '__main__':
	main()

#!/usr/bin/python
import client_send_msg

def send(title, message):
	 print client_send_msg.send_msg(title, message)
	 return client_send_msg.send_msg(title, message)
	 

if __name__ == '__main__':
	send("zwt","zwt")

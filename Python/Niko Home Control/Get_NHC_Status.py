#!/usr/bin/python

"""
**********************************************
Get NHC Status
**********************************************
Author: Steve Gilissen - github.com/sgilissen - gilissen.me
**********************************************
Usage : Get_NHC_Status.py [IP_dest]
IP_dest = IP address of the Niko Home control IP module 

Permissions needed: sudo chmod +x Set_NHC.py

This script should be used in a cron-job in Domoticz to set the status of the switches
""" 

# lib for TCP connection
import socket

# lib to use arguments
import sys

# lib to use time
import time

End='\r\n' #end marker
def recv_end(the_socket):
    total_data=[];data=''
    while True:
            data=the_socket.recv(8192)
            if End in data:
                total_data.append(data[:data.find(End)])
                break
            total_data.append(data)
            if len(total_data)>1:
                #check if end_of_data was split
                last_pair=total_data[-2]+total_data[-1]
                if End in last_pair:
                    total_data[-2]=last_pair[:last_pair.find(End)]
                    total_data.pop()
                    break
    return ''.join(total_data)
    

TCP_PORT = 8000
BUFFER_SIZE = 1024

# Read arguments used to launch this command
#Output_ID = sys.argv[1]
#Output_Value = sys.argv[2]
IP_dest = sys.argv[1]

# Made the message to send to NHC IP controller (JSON format)
TCP_Message = '{"cmd":"listactions"}\r\n'

# print only used for debugging
print ('Connected to NHC Controller: '+ IP_dest)
print ('Message sent: ' + TCP_Message)


# connect to IP and send message
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP_dest, TCP_PORT))
s.send(TCP_Message.encode('utf-8'))
# receive reply from NHC
data = recv_end(s)
s.close()


# Message from NHC (no test of the message in this first version 
print ('Reply from NHC Controller: ' + data.decode('utf-8'))

# NHC must reply error 0 : {"cmd":"executeactions", "data":{"error":0}}

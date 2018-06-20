#!/usr/bin/python

"""
03/18/2016 Set_NHC V1.0
Niko Home Control (NHC) Set actions from Python3 
Control Actions by sending TCP command

Use : Set_NHC.py [Outpu_ID] [Output_Value] [IP_dest]
example : python3 Set_NHC.py "35" "0" "192.168.0.26"
Output_ID = 6 : The ID of action to control
Output_Value = 100 (Value from 0 to 100 %)
IP_dest = IP of the Niko Home control IP module (use your router to fix the IP with MAC Adress)

Take care of permissions on this file to execute as script from Domoticz use this command before use !
sudo chmod +x Set_NHC.py
""" 

# lib for TCP connection
import socket

# lib to use arguments
import sys

TCP_PORT = 8000
BUFFER_SIZE = 1024

# Read arguments used to launch this command
Output_ID = sys.argv[1]
Output_Value = sys.argv[2]
IP_dest = sys.argv[3]

# Made the message to send to NHC IP controller (JSON format)
TCP_Message = '{"cmd":"executeactions","value1":' + str(Output_Value) + ',"id":' + str(Output_ID) + '}\r\n'
#TCP_Message = '{"cmd":"startevents",0}'

# print only used for debugging
print ('Connect to NHC IP : '+ IP_dest)
print ('Message send : ' + TCP_Message)

# connect to IP and send message
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP_dest, TCP_PORT))
s.send(TCP_Message.encode('utf-8'))

# receive reply from NHC
data = s.recv(BUFFER_SIZE)
s.close()

# Message from NHC (no test of the message in this first version 
print ('Reply from NHC IP : ' + data.decode('utf-8'))

# NHC must reply error 0 : {"cmd":"executeactions", "data":{"error":0}}

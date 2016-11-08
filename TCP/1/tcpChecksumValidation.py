# Author     : Pallavi
# Created on : 13-10-2016

import socket
import sys

segment = str(sys.argv[1])
srcIP = str(sys.argv[2])
destIP = str(sys.argv[3])

MOD = 1 << 16

def ones_comp_add(num1,num2):
    result = num1 + num2
    return result if result < MOD else (result+1) % MOD

def length_of_msg(msg):
	hexMsgLen = len(msg)

	if hexMsgLen == 0:
		return 0
	elif hexMsgLen%2 == 0:
		return (hexMsgLen/2)
	else:
		return (hexMsgLen/2)+ 1

srcIPHex = socket.inet_aton(srcIP).encode('hex')
destIPHex = socket.inet_aton(destIP).encode('hex')

# replacing checksum
segChecksum = segment[32:36]
noChecksumSeg = segment[0:32]+'0000'+segment[36:]

reservedNum = "{:02x}".format(0)
protocolNum = "{:02x}".format(6)
reservAndProtocol = "".join([reservedNum,protocolNum])

# tcp segment length, (offset*4)+ lengthOfData, lengthOfData and offset part is variable.

dataOffset = int((segment[24:25]),16)
dataBytes = segment[64:]
lengthOfMsg = length_of_msg(dataBytes)
totalMsgLength = ((dataOffset * 4) + lengthOfMsg)
tcpSegLength = "{:04x}".format(totalMsgLength)

completeSegment = []
completeSegment.extend([srcIPHex,destIPHex,reservAndProtocol,tcpSegLength,noChecksumSeg])
# convert it in one big hex string
completeSegment = "".join(completeSegment)
sumCalculation = completeSegment

i = 0
total = int('0000000000000000',2)
while (len(sumCalculation[i:]) != 0):
	segHex = sumCalculation[i:i+4]
	if len(completeSegment) < 4:
		seg = int(segHex,16)
		total = ones_comp_add(total,seg)
	
	else: 
		seg = int(segHex,16)
		total = ones_comp_add(total,seg)
	i = i+4

total = format(total,'016b')

# flip all the 16 bits
total = ''.join('1' if x == '0' else '0' for x in total)
checksum = hex(int(total,2))[2:]

if (checksum == segChecksum):
	print int((segment[0:4]),16)
	print int((segment[4:8]),16)
	print int((segment[8:16]),16)
	print int((segment[16:24]),16)
	print int((segment[26:28]),16)
	print int((segment[28:32]),16)
	print int((segment[32:36]),16)
	# inBytes = (dataOffset*4), inHex = (dataOffset *4*2)
	print segment[dataOffset * 4 *2:] 
else:
	print "Invalid segment"
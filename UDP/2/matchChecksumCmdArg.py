# Pallavi
# @10.16.2016

#!/usr/bin/python
import sys


userInput = str(sys.argv[1])
sourceIP = str(sys.argv[2])
destinationIP = str(sys.argv[3])
userInput1 = userInput[:16]

userInput2 = userInput[16:]

list1 = []
list2 = []
def hexstringToDecimal(s):
    for i in range(0,len(s),4):
    	list1.append(s[i:i+4])

def hexMsgTOPerChar(s):
    for i in range(0,len(s),2):
    	list2.append(s[i:i+2])

MOD = 1 << 16

def ones_comp_add16(num1,num2):
    result = num1 + num2
    return result if result < MOD else (result+1) % MOD

hexstringToDecimal(userInput1)
hexMsgTOPerChar(userInput2)
# convert dot notation of IP addresses to 8 bit binary and store as list
sourceIPs = [format(int(x), '08b') for x in sourceIP.split('.')]
destinationIPs = [format(int(x), '08b') for x in destinationIP.split('.')]

# SourceIP calculation
sixteenBitNumber1 = b"".join([sourceIPs[0],sourceIPs[1]])
sixteenBitNumber2 = b"".join([sourceIPs[2],sourceIPs[3]])

sum1 = format((int(sixteenBitNumber1,2) + int(sixteenBitNumber2,2)),'016b')

# destinationIPs calculation
sixteenBitNumber3 = b"".join([destinationIPs[0],destinationIPs[1]])
sixteenBitNumber4 = b"".join([destinationIPs[2],destinationIPs[3]])

sum2 = format((int(sixteenBitNumber3,2) + int(sixteenBitNumber4,2)),'016b')

# Source and destination port calculation
sourcePortHex = list1[0]
sourcePort = format(int(sourcePortHex,16),'016b')

destinationPortHex = list1[1]
destinationPort = format(int(destinationPortHex,16),'016b')

sum3 = format((int(sourcePort,2) + int(destinationPort,2)), '016b')

# calculation of contant values UDP num and 8bit zero
eightBitZero = format(int('0'), '08b')
UDPnum = format(int('17'), '08b')
sum4 = b"".join([eightBitZero,UDPnum])

#calculate header (add twice)
headerlengthHex = list1[2]
headerlength = int(headerlengthHex,16)
sum5 = ones_comp_add16(headerlength,headerlength)
sum5 = format(sum5, '016b')

final1 = int(sum1,2)
final2 = int(sum2,2)
final3 = int(sum3,2)
final4 = int(sum4,2)
final5 = int(sum5,2)

result1 = ones_comp_add16(final1,final2)
result2 = ones_comp_add16(final3, final4)

result3 = ones_comp_add16(result1, result2)

result4 = ones_comp_add16(result3, final5)

result4 = format(int(result4), '016b')
result4 = int(result4,2)

total1 = result4 

# calculation of msg
i = 0
msg_hex = "".join(list2)
msg = msg_hex.decode('hex')

while i < len(msg):
	if len(msg) == 1:
		code1 = ord(msg[i])
		code1 = format(code1,'08b')
		code2 = format(int('0'),'08b')
		codeSixteenBit1 = b"".join([code1,code2])
		codeNumeric1 = int(codeSixteenBit1,2)
		total1 = ones_comp_add16(codeNumeric1,total1)
	if (len(msg)%2) == 0:
		code1 = ord(msg[i])
		code2 = ord(msg[i+1])
		code1 = format(code1,'08b')
		code2 = format(code2,'08b')
		codeSixteenBit1 = b"".join([code1,code2])
		codeNumeric1 = int(codeSixteenBit1,2)
		total1 = ones_comp_add16(codeNumeric1,total1)
	else:
		if i == (len(msg)-1):
			code1 = ord(msg[i])
			code1 = format(code1,'08b')
			code2 = format(int('0'),'08b')
			codeSixteenBit1 = b"".join([code1,code2])
			codeNumeric1 = int(codeSixteenBit1,2)
			total1 = ones_comp_add16(codeNumeric1,total1)
		else:
			code1 = ord(msg[i])
			code2 = ord(msg[i+1])
			code1 = format(code1,'08b')
			code2 = format(code2,'08b')
			codeSixteenBit1 = b"".join([code1,code2])
			codeNumeric1 = int(codeSixteenBit1,2)
			total1 = ones_comp_add16(codeNumeric1,total1)
	
	i= i+2

total1 = format(total1,'016b')

checksumGiven = list1[3]

# flip all the 16 bits
result10 = ''.join('1' if x == '0' else '0' for x in total1)

#checksum in hex
checksumWith0x = hex(int(result10,2))
checksum = checksumWith0x[2:]


if checksum == checksumGiven:
	print int(sourcePortHex,16)
	print int(destinationPortHex,16)
	print headerlength
	print checksumWith0x
	print msg
else:
	print "Invalid UDP segment"
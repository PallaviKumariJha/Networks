import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
IP = str(sys.argv[1])
port = int(sys.argv[2])
server_address = (IP,port)
sock.connect(server_address)

try:
	# Send data
    def print_char(changed):
        S_VAL = changed[0]
        E_VAL = changed[1]
        P_VAL = changed[2]
        P_VAL = int(P_VAL)
        length = ord(E_VAL) - ord(S_VAL)
        # put upperCase and lower case checks
        if length == 0:
            sock.sendall(S_VAL)
        else:
            value = ' '.join(chr(c) for c in range(ord(S_VAL), ord(E_VAL)+1, P_VAL))
            value = str(value+"\n")
            sock.sendall(value)
    
    while True:
        data = sock.recv(64)
        if (data.find('Start')!= -1):
            changed = data.replace(',', '').split(" ")[1::2]
            print_char(changed)   
        elif data.find('Welcome') != -1:
            continue
        else:
            sock.close()
finally:
    sock.close()
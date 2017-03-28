import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
port = int(sys.argv[1])
server_address = ('0.0.0.0', port)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(5)

def fib_iterative(n):
    a, b = 0, 1
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        while n > 0:
            a, b = b, a + b
            n -= 1
        return a

while True:
    # Wait for a connection=
    connection, client_address = sock.accept()

    # Receive the data in small chunks and retransmit it
    while True:
        data = connection.recv(64)
        if data:
            if data.find('Total') != -1:
                continue
            else:
                data = int(data)
                nthOrder = fib_iterative(data-1)
                nthOrder = str(nthOrder)+"\n"
                connection.sendall(nthOrder)
        else:
            break
    # Clean up the connection
    connection.close()

import socket

def send_rosstalk(ip, port, message):
    # Add /r/n to the message to comply with the specified format
    message += '\r\n'
    
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to the server
        s.connect((ip, port))
        
        # Send the message
        s.sendall(message.encode())

# Replace 'localhost' with the IP address of the listener
# Replace 'your text here' with the message you want to send
# send_rosstalk('10.10.80.101', 7795, 'your text here')

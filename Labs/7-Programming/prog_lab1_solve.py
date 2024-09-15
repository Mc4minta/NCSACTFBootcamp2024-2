import socket

def ascii_to_string(data):
    # Split the data into individual ASCII numbers
    ascii_numbers = data.split()

    # Convert each ASCII number to its corresponding character 
    # and join them into a string
    flag = ''.join(chr(int(num)) for num in ascii_numbers)

    return flag

def main():
    # Server details
    host = '127.0.0.1'
    port = 43239
    
    # Create a socket and connect to the server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    # Buffer to hold received data
    full_data = ""

    while True:
        # Receive data from the server in chunks of 1024 bytes
        data = client.recv(1024).decode()

        if not data:
            # No more data is being received, break the loop
            break

        # Append the received data to the buffer
        full_data += data

    # Convert the received ASCII numbers to a flag string
    flag = ascii_to_string(full_data)

    # Print the flag
    print("Flag: ", flag)

    # Close the connection
    client.close()

if __name__ == "__main__":
    main()



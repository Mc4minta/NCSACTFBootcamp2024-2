import socket

# Function to handle binary operations
def perform_operation(op_symbol, binary1, binary2):
    operations = {
        '<<': lambda x, y: bin(int(x, 2) << int(y, 2))[2:],
        '+': lambda x, y: bin(int(x, 2) + int(y, 2))[2:],
        '-': lambda x, y: bin(int(x, 2) - int(y, 2))[2:],
        '&': lambda x, y: bin(int(x, 2) & int(y, 2))[2:],
        '|': lambda x, y: bin(int(x, 2) | int(y, 2))[2:],
        '^': lambda x, y: bin(int(x, 2) ^ int(y, 2))[2:],
        '*': lambda x, y: bin(int(x, 2) * int(y, 2))[2:],
        '>>': lambda x, y: bin(int(x, 2) >> int(y, 2))[2:]
    }
    return operations[op_symbol](binary1, binary2)

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 55816))

    # Read initial instructions from server
    print(client_socket.recv(1024).decode())

    binary1 = binary2 = None

    while True:
        # Receive and display server message
        response = client_socket.recv(1024).decode()
        print(f"Server response: {response}")

        operation = None  # Ensure operation is initialized for each loop
        
        # Parse binary numbers and operation
        for line in response.split('\n'):
            if 'Binary Number 1' in line and ': ' in line:
                binary1 = line.split(': ')[1].strip()
            if 'Binary Number 2' in line and ': ' in line:
                binary2 = line.split(': ')[1].strip()
            if 'Operation' in line and ': ' in line:
                operation = line.split(': ')[1].replace("'", "").strip()

        if binary1 and binary2 and operation:
            result = perform_operation(operation, binary1, binary2)
            print(f"Result: {result}")
            client_socket.sendall(f"{result}\n".encode())

        # Check if challenge is completed
        if 'The flag is' in response:
            print("Challenge completed.")
            break

if __name__ == "__main__":
    main()

import socket
import random
import threading

def binary_operations():
    # Define all the possible operations with lambda functions
    operations = [
        ('<<', lambda x, y: bin(int(x, 2) << int(y, 2))[2:]),
        ('+', lambda x, y: bin(int(x, 2) + int(y, 2))[2:]),
        ('-', lambda x, y: bin(int(x, 2) - int(y, 2))[2:]),
        ('&', lambda x, y: bin(int(x, 2) & int(y, 2))[2:]),
        ('|', lambda x, y: bin(int(x, 2) | int(y, 2))[2:]),
        ('^', lambda x, y: bin(int(x, 2) ^ int(y, 2))[2:]),
        ('>>', lambda x, y: bin(int(x, 2) >> int(y, 2))[2:]),
        ('~', lambda x, _: bin(~int(x, 2) & 0xFFFFFFFF)[2:])  # 32-bit NOT operation
    ]
    return operations

def generate_random_binary(length=8):
    return ''.join(random.choice('01') for _ in range(length))

def handle_client(client_socket):
    client_socket.sendall(b"Welcome to the Binary Challenge!\n")
    client_socket.sendall(b"Your task is to perform the unique operations in the given order and find the final result in binary.\n\n")

    rand_binary1 = generate_random_binary()
    rand_binary2 = generate_random_binary()

    client_socket.sendall(f"Binary Number 1: {rand_binary1}\n".encode())
    client_socket.sendall(f"Binary Number 2: {rand_binary2}\n\n".encode())

    operations = binary_operations()
    random.shuffle(operations)  # Shuffle the operations to randomize

    num_questions = 6  # Set the number of questions to 6
    question_number = 1

    for op_symbol, op_function in operations[:num_questions]:  # Limit to 6 questions
        client_socket.sendall(f"Question {question_number}/{num_questions}:\n".encode())
        client_socket.sendall(f"Operation {question_number}: '{op_symbol}'\n".encode())

        if op_symbol == '~':
            client_socket.sendall(f"Perform NOT operation on Binary Number 1.\n".encode())
            expected_result = op_function(rand_binary1, None)
        else:
            client_socket.sendall(f"Perform the operation on Binary Number 1 and Binary Number 2.\n".encode())
            expected_result = op_function(rand_binary1, rand_binary2)
        
        client_socket.sendall(b"Enter the binary result: ")
        client_response = client_socket.recv(1024).strip().decode()

        if client_response == expected_result:
            client_socket.sendall(b"Correct!\n\n")
        else:
            client_socket.sendall(b"Incorrect. Try again.\n")
            client_socket.close()
            return
        
        question_number += 1

    client_socket.sendall(b"Congratulations! You have completed all the questions.\n")
    client_socket.sendall(b"The flag is: FLAG{BINARY_OPERATIONS}\n")
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 55816))
    server.listen(5)
    print("Server listening on port 55816...")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()

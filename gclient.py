import socket

host = "192.168.1.7"
port = 7777

def receive_until(prompt):
    buffer = ""
    while prompt not in buffer:
        data = s.recv(1024)
        if not data:
            return None
        buffer += data.decode()
    result, buffer_remainder = buffer.split(prompt, 1)
    buffer = prompt + buffer_remainder  # keep the prompt in the buffer
    return result + prompt

# Main client loop
while True:
    s = socket.socket()
    s.connect((host, port))

    menu = receive_until("Enter choice:")
    if menu is None:
        print("Connection closed by server.")
        break
    print(menu.strip())

    user_input = input("").strip()
    s.sendall(user_input.encode())

    # If the user chooses invalid input, terminate the connection.
    if user_input not in ['1', '2', '3']:
        print("Invalid choice, closing connection.")
        break

    while True:
        data = s.recv(1024)
        if not data:
            print("Disconnected from server.")
            break

        decoded = data.decode().strip()
        print(decoded)

        # Check if the correct number was guessed
        if "CORRECT!" in decoded:
            print("You guessed the correct number!")
            s.close()  # Close the connection after guessing correctly
            break

    
    s.close()
    input("\nPress Enter to play again or close the client.")

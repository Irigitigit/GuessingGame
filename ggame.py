import socket
import random
import time

host = "0.0.0.0"
port = 7777

def generate_random(difficulty):
    if difficulty == 1:
        return random.randint(1, 10)
    elif difficulty == 2:
        return random.randint(1, 50)
    return random.randint(1, 100)

def get_difficulty(c):
    difficulty_display = """
MENU
====
1) Easy
2) Medium 
3) Hard
Enter choice:"""
    c.sendall(difficulty_display.encode())
    choice = c.recv(1024).decode().strip()
    return int(choice)

# Initialize socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)
print("Server is listening on port", port)

while True:
    print("Waiting for connection...")
    conn, addr = s.accept()
    print(f"New client connected: {addr[0]}")

    try:
        difficulty = get_difficulty(conn)
        if difficulty not in [1, 2, 3]:
            conn.sendall(b"Invalid choice. Closing connection.\n")
            conn.close()
            continue
    except:
        conn.close()
        continue

    min_range = 1
    max_range = [10, 50, 100][difficulty - 1]
    guessme = generate_random(difficulty)
    print(f"[DEBUG] Number to guess: {guessme}")

    low = min_range
    high = max_range

    conn.sendall(b"\nAuto-guessing started...\n")

    while True:
        time.sleep(0.5)
        guess = (low + high) // 2
        conn.sendall(f"Auto guess: {guess}\n".encode())
        print(f"[AUTO GUESS]: {guess}")

        if guess == guessme:
            conn.sendall(b"CORRECT!\n")
            conn.close()
            break
        elif guess > guessme:
            conn.sendall(b"=Guess Lower\n")
            high = guess - 1
        else:
            conn.sendall(b"=Guess Higher\n")
            low = guess + 1

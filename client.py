import socket

def decode(code:str):return str(__import__('base64').b64decode(code))[2:-1].split(':')

server_host=decode(input('input server code: '))

HOST = str(server_host[0])
PORT = int(server_host[1])

def send_command(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(command.encode())
        response = s.recv(1024).decode()
        print(f"[RESPONSE] {response}")

if __name__ == "__main__":
    while True:
        choice = input("Enter command (SEND <data> or GET): ").strip()
        if choice:
            send_command(choice)

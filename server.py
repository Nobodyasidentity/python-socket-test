import socket
import threading

def encode(ip:str,port:int|str):return str(__import__('base64').b64encode(f'{ip}:{port}'.encode()))[2:-1]
IPv4=str(__import__('subprocess').run('ipconfig',capture_output=True)).split('4 Address. . . . . . . . . . . : ')[1].split('\\r')[0]
def find_free_port():
    from contextlib import closing
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return int(s.getsockname()[1])

HOST = str(IPv4)
PORT = 65432

print('server code:',encode(HOST,PORT))

latest_data = ""  # Shared data
lock = threading.Lock()  # To prevent race conditions

def handle_client(conn, addr):
    global latest_data
    print(f"[+] Connected by {addr}")
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            if data.strip() == "INFO":
                with lock:
                    print('sent info')
                conn.sendall(f'{HOST}:{PORT}\t"{latest_data}"'.encode())

            elif data.startswith("SEND "):
                with lock:
                    latest_data = data[5:]  # Remove "SEND " prefix
                    print(f"[STORE] Data updated to: {latest_data}")
                conn.sendall(b"Data received and stored.")
            elif data.strip() == "GET":
                with lock:
                    response = latest_data if latest_data else "No data available."
                conn.sendall(response.encode())
            else:
                conn.sendall(b"Invalid command. Use SEND <data> or GET.")
    finally:
        conn.close()
        print(f"[-] Disconnected from {addr}")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[SERVER] Listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    start_server()

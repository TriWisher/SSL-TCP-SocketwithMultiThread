import socket
import ssl
import threading

def receive_messages(ssl_client_scoket):
    try:
        while True:
            message = ssl_client_scoket.recv(1024).decode('utf-8')

            if not message:
                break
            print(message)

    finally:
        ssl_client_scoket.close()

def start_client():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations('./Certificates/cert.pem')

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_client_socket = context.wrap_socket(client_socket, server_hostname='Tri')

    ssl_client_socket.connect(('10.9.67.211', 12345))
    print('Connected to the server successfully!')

    receive_thread = threading.Thread(target=receive_messages, args=(ssl_client_socket,))
    receive_thread.start()

    try:
        nickname = input('Enter your nickname: ')
        ssl_client_socket.send(nickname.encode('utf-8'))

        while True:
            message = input()
            ssl_client_socket.send(nickname.encode('utf-8'))

    except KeyboardInterrupt:
        ssl_client_socket.close()

if __name__ == '__main__':
    start_client()
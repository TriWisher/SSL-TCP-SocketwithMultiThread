import socket
import threading
import ssl
import time

clients = {}


def broadcast(message, current_client_socket=None):
    for client_socket in clients:
        if client_socket != current_client_socket:
            client_socket.send(message.encode('utf-8'))


def handle_client(client_socket):
    try:
        client_socket.send('Enter your nickname: '.encode('utf-8'))
        nickname = client_socket.recv(1024).decode('utf-8')
        clients[client_socket] = nickname

        print(f'{nickname} has joined the chat !')
        broadcast(f'{nickname} has joined the chat!', client_socket)

        while True:
            message = client_socket.recv(1024).decode('utf-8')

            if not message:
                break

            broadcast(f'{nickname}: {message}', client_socket)
            print(f'{nickname}: {message}')

    finally:
        nickname = clients.pop(client_socket, 'Unknown')
        print(f'{nickname} has left the chat')
        broadcast(f'{nickname} has left the chat', client_socket)
        client_socket.close()


def start_server():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile='F:\Kulyeah\workspace_python\pythonProject1\Certificates\cert.pem',
                            keyfile='F:\Kulyeah\workspace_python\pythonProject1\Certificates\key.pem')

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('10.9.67.211', 12345))
    server_socket.listen(5)

    ssl_socket_server = context.wrap_socket(server_socket, server_side=True)
    print('Server running, awaiting connection...')
    time.sleep(2)

    while True:
        client_socket, client_address = ssl_socket_server.accept()
        print('Connection Established !')
        time.sleep(2)

        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


if __name__ == '__main__':
    start_server()

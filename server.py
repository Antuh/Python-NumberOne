import socket 
from select import select
tasks = []
to_read = {}
to_write = {}

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server_socket.bind(("0.0.0.0", 9990))
    server_socket.listen(0)
    print("[+] Waiting for incoming connections")

    while True:
        yield ('read', server_socket)
        cl_socket, remote_address = server_socket.accept()
        print(f"[+] Got a connection from {remote_address} ")
        tasks.append(process_client(cl_socket, remote_address))

def process_client(cl_socket: socket, remote_address):
    while True:
        yield ('read', cl_socket)
        message = cl_socket.recv(1024).decode()
        if not message:
            break
        else:
            print(f"Message from the client {remote_address}: "+ message)
            yield('write', cl_socket)
            cl_socket.send(message.encode())
    cl_socket.close()

def event_loop():
    while any([tasks, to_read, to_write]):
        while not tasks:
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])
            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))
            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))
        try:
            task = tasks.pop(0)
            reason, sock = next(task)
            if reason == 'read':
                to_read[sock] = task
            if reason == 'write':
                to_write[sock] = task
        except StopIteration:
            print('Done!')

if __name__ == "__main__":
    tasks.append(server())
    event_loop()
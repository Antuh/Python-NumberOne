import socket


def main():
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    client_socket.connect(('localhost',9990))
    print("Success connect")


    while True:
        try:
            message :str = input("Enter a message for the server>> ")
    
            client_socket.send(message.encode())
            message_server = client_socket.recv(1024).decode()

            print("Message from the server: "+message_server)
        
        except Exception:
            print("Что-то пошло не так...")
        except KeyboardInterrupt:
            client_socket.close()
            exit()
  
if __name__ == '__main__':
    main()
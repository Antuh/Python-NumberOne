import socket
import threading
 
servsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
servsock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
servsock.bind(('localhost',9090))
servsock.listen(True)
 
welcome = b'Welcome from new chat'
 
def main():
    while True:
        conn,addr = servsock.accept()
        ClientThread(conn,addr).start()
 
 
class ClientThread(threading.Thread):
 
    def __init__(self,conn,addr):
        self.conn = conn
        self.addr = addr
        threading.Thread.__init__(self)
 
    def run(self):
        try:
            self.conn.send(welcome)
            print(self.addr , ' "Подключился"')
            while True:
                data = self.conn.recv(1024)
                udata = data.decode('utf-8')
                print(udata)
        except ConnectionResetError:
             self.conn.close()
             print(self.addr , ' "Соединение разорванно"')
 
if __name__ == '__main__':
    main()
    servsock.close()
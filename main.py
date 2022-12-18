import socket
 
clntsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clntsock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
 
    
def connect():
    clntsock.connect(('localhost',9090))
    data = clntsock.recv(1024)
    udata = data.decode('utf-8')
    print(udata)
    while True:
        out = input('Mess: ')
        b_out = out.encode('utf-8')
        clntsock.send(b_out)
 
 
if __name__ == '__main__':
    connect()
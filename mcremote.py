import socket

class MCRemote:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def send(self, command):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect((self.host, self.port))
        s.sendall(self.username + '\n' + self.password + '\n\n')

        data = ' '
        try:
            while True:
                data = s.recv(1024)
        except Exception:
            pass

        s.sendall(command)
        s.close()

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        s.settimeout(1.0)
        s.sendall(self.username + '\n' + self.password + '\n\n')
        data = ''
        response = ''
        try:
            while True:
                response += s.recv(1024)
        except Exception:
            pass

        response = response.split('RemoteBukkit')[-1].split('\n')[1:]
        return ''.join(response).split('\x1b')[0]

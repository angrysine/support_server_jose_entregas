import socket
import threading
import time

class Robot():
    def __init__(self) -> None:
        self.clientes = 0
        self.data = ''
        host = '127.0.0.1' 
        port = 4000

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)  # Permite até 5 conexões pendentes

        print(f"Servidor escutando em {host}:{port}")

    def comunicacao(self):
        self.client_socket, self.addr = self.server.accept()
        print(f"Conexão aceita de {self.addr[0]}:{self.addr[1]}")
        client_handler = threading.Thread(target=self.handle_client, args=(self,))
        client_handler.start()
        

    def handle_client(self,none):
        self.clientes += 1
        try:
            while True:
                self.data = self.client_socket.recv(1024).decode('utf-8')
                print(f"seu dado : {self.data}")
                if not self.data:
                    break
                print(f"Mensagem recebida do cliente{self.clientes}: {self.data}")
                self.data = self.data
                response = "Mensagem recebida com sucesso!"
                self.client_socket.send(response.encode('utf-8'))
        except ConnectionResetError:
            print("A conexão foi redefinida pelo host remoto.")
        finally:
            self.client_socket.close()


    
    def requicoes(self):
        return self.data









def main():
    while True:
        m = Robot()
        time.sleep(1)
        print("Vinda do ZAP: ",m.requicoes())

if __name__ == "__main__":
    main()

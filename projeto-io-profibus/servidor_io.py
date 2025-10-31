import socket
import threading

class DispositivoIO:
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.estado_simulado = "DESLIGADO" 
        self.server_socket = None

    def iniciar_servidor(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print(f"--- Servidor (Dispositivo I/O) ouvindo em {self.host}:{self.port} ---")
        print(f"Estado inicial: {self.estado_simulado}")

        while True:
            print("Aguardando conexão do controlador...")
            conn, addr = self.server_socket.accept()
            print(f"Controlador {addr} conectou.")
            conn.close()

    def processar_comando(self, comando):
        
        if comando == "LER_STATUS":
            return self.estado_simulado
        else:
            return "COMANDO_INVALIDO"

if __name__ == "__main__":
    dispositivo = DispositivoIO('127.0.0.1', 65432)
    
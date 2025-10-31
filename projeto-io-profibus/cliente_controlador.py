import socket

class Controlador:
   
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None

    def conectar(self):
       
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"Esqueleto: Conectaria ao servidor em {self.host}:{self.port}")
            return True
        except socket.error as e:
            print(f"Erro ao conectar: {e}")
            return False

    def enviar_comando(self, comando):
        if self.client_socket is None:
            print("Não conectado.")
            return

        try:
            print(f"Enviando comando: {comando}")
            
            resposta_simulada = "DESLIGADO"
            print(f"Resposta (simulada): {resposta_simulada}")
            
        except socket.error as e:
            print(f"Erro na comunicação: {e}")

    def fechar(self):
        if self.client_socket:
            print("Conexão fechada.")


if __name__ == "__main__":
    print("--- Cliente (Controlador) ---")
    controlador = Controlador('127.0.0.1', 65432)
    
    if controlador.conectar():
        controlador.enviar_comando("LER_STATUS")
        controlador.fechar()
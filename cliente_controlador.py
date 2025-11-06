import socket

class Controlador:
   
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None

    def conectar(self):
       
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            print(f"Conectado ao servidor em {self.host}:{self.port}")
            return True
        except socket.error as e:
            print(f"Erro ao conectar: {e}")
            self.client_socket = None
            return False

    def enviar_comando(self, comando, timeout=2.0):
        if self.client_socket is None:
            print("Não conectado.")
            return None

        try:
            print(f"Enviando comando: {comando}")
            self.client_socket.sendall((comando + "\n").encode())
            self.client_socket.settimeout(timeout)
            resposta = b""
            # ler até newline
            while True:
                chunk = self.client_socket.recv(1024)
                if not chunk:
                    break
                resposta += chunk
                if b"\n" in chunk:
                    break
            resposta_text = resposta.decode().strip()
            print(f"Resposta: {resposta_text}")
            return resposta_text
            
        except socket.error as e:
            print(f"Erro na comunicação: {e}")
            return None

    def fechar(self):
        if self.client_socket:
            try:
                self.client_socket.close()
            except OSError:
                pass
            self.client_socket = None
            print("Conexão fechada.")


if __name__ == "__main__":
    import sys
    print("--- Cliente (Controlador) ---")
    host = '127.0.0.1'
    port = 65432
    cmd = "LER_STATUS"
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
    controlador = Controlador(host, port)
    
    if controlador.conectar():
        controlador.enviar_comando(cmd)
        controlador.fechar()
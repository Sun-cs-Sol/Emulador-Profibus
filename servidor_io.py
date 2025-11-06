import socket
import threading

class DispositivoIO:
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.estado_simulado = "DESLIGADO" 
        self.server_socket = None
        self._running = False

    def iniciar_servidor(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
       
        self.port = self.server_socket.getsockname()[1]
        self.server_socket.listen(1)
        self._running = True
        print(f"--- Servidor (Dispositivo I/O) ouvindo em {self.host}:{self.port} ---")
        print(f"Estado inicial: {self.estado_simulado}")

        while self._running:
            try:
                print("Aguardando conexão do controlador...")
                conn, addr = self.server_socket.accept()
            except OSError:
                
                break
            print(f"Controlador {addr} conectou.")
           
            t = threading.Thread(target=self._handle_client, args=(conn, addr), daemon=True)
            t.start()

    def _handle_client(self, conn, addr):
        try:
            data = conn.recv(1024)
            if not data:
                return
            comando = data.decode().strip()
            print(f"Recebido do {addr}: {comando}")
            resposta = self.processar_comando(comando)
            conn.sendall((resposta + "\n").encode())
            print(f"Enviado para {addr}: {resposta}")
        finally:
            conn.close()

    def processar_comando(self, comando):
        
        if comando == "LER_STATUS":
            return self.estado_simulado
        elif comando.startswith("SET_STATUS:"):
            _, valor = comando.split(":", 1)
            self.estado_simulado = valor
            return "OK"
        else:
            return "COMANDO_INVALIDO"

    def parar_servidor(self):
        self._running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except OSError:
                pass

if __name__ == "__main__":
    dispositivo = DispositivoIO('127.0.0.1', 65432)
    try:
        dispositivo.iniciar_servidor()
    except KeyboardInterrupt:
        print("Parando servidor...")
        dispositivo.parar_servidor()

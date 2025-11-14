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
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            self._running = True
            print(f"--- Servidor ouvindo em {self.host}:{self.port} ---")
            while self._running:
                try:
                    conn, addr = self.server_socket.accept()
                    threading.Thread(target=self._handle_client, args=(conn, addr), daemon=True).start()
                except socket.error as e:
                    print(f"Erro ao aceitar conexão: {e}")
        except Exception as e:
            print(f"Erro ao iniciar o servidor: {e}")
        finally:
            self.parar_servidor()

    # handle para uma única mensagem por conexão

    # def _handle_client(self, conn, addr):
    #     try:
    #         data = conn.recv(1024)
    #         if not data:
    #             return
    #         comando = data.decode().strip()
    #         print(f"Recebido do {addr}: {comando}")
    #         print(f"Estado atual: {self.estado_simulado}")
    #         resposta = self.processar_comando(comando)
    #         with open("log.txt", "a") as log_file:
    #             log_file.write(f"{addr} - Comando: {comando}, Resposta: {resposta}\n")
    #         conn.sendall((resposta + "\n").encode())
    #         print(f"Enviado para {addr}: {resposta}")
    #     finally:
    #         conn.close()

    def _handle_client(self, conn, addr):
        print(f"Nova conexão de {addr}")
        try:
            while True:
                data = conn.recv(1024)
                
                if not data:
                    print(f"Conexão encerrada pelo cliente {addr}")
                    break
                
                comando = data.decode().strip()
                print(f"Recebido do {addr}: {comando}")
                print(f"Estado atual: {self.estado_simulado}")
                
                resposta = self.processar_comando(comando)
                
                conn.sendall((resposta + "\n").encode()) 
                
                print(f"Enviado para {addr}: {resposta}")
                
                with open("log.txt", "a") as log_file:
                    log_file.write(f"{addr} - Comando: {comando}, Resposta: {resposta}\n")

        except ConnectionResetError:
            print(f"Conexão reiniciada/perdida com {addr}")
        except socket.timeout:
            print(f"Timeout na conexão com {addr}")
        except Exception as e:
            print(f"Erro inesperado no manuseio do cliente {addr}: {e}")
        finally:
            conn.close()
            print(f"Conexão com {addr} fechada.")

    def processar_comando(self, comando):
        print(f"Processando comando: {comando} ")
        if comando == "LER_STATUS":
            return self.estado_simulado
        elif comando.startswith("SET_STATUS:"):
            _, valor = comando.split(":", 1)
            print("Entrei no set status")
            if valor in ["LIGADO", "DESLIGADO"]:
                self.estado_simulado = valor
                print(f"Estado alterado para: {self.estado_simulado}")
                return "OK"
            else:
                return "VALOR_INVALIDO"
        elif comando == "LISTAR_COMANDOS":
            return "LER_STATUS, SET_STATUS:<VALOR>, LISTAR_COMANDOS"
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
    dispositivo = DispositivoIO('localhost', 8080)
    try:
        dispositivo.iniciar_servidor()
    except KeyboardInterrupt:
        print("Parando servidor...")
        dispositivo.parar_servidor()

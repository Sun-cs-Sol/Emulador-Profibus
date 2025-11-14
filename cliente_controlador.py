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
            self.client_socket.settimeout(2.0)  # Set a global timeout
            print(f"Conectado ao servidor em {self.host}:{self.port}")
            return True
        except socket.gaierror:
            print("Erro de endereço inválido.")
        except socket.timeout:
            print("Erro: Tempo de conexão esgotado.")
        except socket.error as e:
            print(f"Erro ao conectar: {e}")
        self.client_socket = None
        return False
    
    def enviar_comando(self, comando, buffer_size=4096):
        if self.client_socket is None:
            print("Não conectado.")
            return None

        try:

            if not comando.endswith("\n"):
                comando += "\n"

            print(f"Enviando comando: {comando.strip()}")

            self.client_socket.sendall(comando.encode('utf-8'))

            resposta = b""
            conexao_fechada_pelo_servidor = False

            while True:
                chunk = self.client_socket.recv(buffer_size)
                if not chunk:
                    conexao_fechada_pelo_servidor = True
                    break
                resposta += chunk
                if b"\n" in chunk:
                    break

            if conexao_fechada_pelo_servidor and not resposta:
                print("ERRO: O servidor fechou a conexão sem enviar uma resposta.")
                self.fechar()
                return None

            resposta_text = resposta.decode('utf-8', errors='replace').strip()
            print(f"Resposta: {resposta_text}")

            if conexao_fechada_pelo_servidor:
                 print("AVISO: Conexão fechada pelo servidor após a resposta. Tentando reconectar.")
                 self.fechar()
                

            return resposta_text
        
        except socket.timeout as e: 
            print(f"Erro de Timeout ao esperar a resposta para '{comando.strip()}': {e}")
            self.fechar()
            return None
            
        except socket.error as e:
            print(f"Erro na comunicação ao enviar o comando '{comando.strip()}': {e}")
            self.fechar()
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
    host = 'localhost'
    port = 8080
    controlador = Controlador(host, port)
    
    if controlador.conectar():
        while True:
            print("\n--- Menu ---")
            print("1. Ler Status")
            print("2. Alterar Status")
            print("3. Sair")
            opcao = input("Escolha uma opção: ")
            
            if opcao == "1":
                controlador.enviar_comando("LER_STATUS")
            elif opcao == "2":
                novo_status = input("Digite o novo status (LIGADO/DESLIGADO): ").upper()
                if novo_status in ["LIGADO", "DESLIGADO"]:
                    controlador.enviar_comando(f"SET_STATUS:{novo_status}")
                else:
                    print("Status inválido. Tente novamente.")
            elif opcao == "3":
                break
            else:
                print("Opção inválida.")

        controlador.fechar()
import unittest
import threading
import time

from src.servidor_io import DispositivoIO
from src.cliente_controlador import Controlador


class TestCoreNetwork(unittest.TestCase):
    def test_ler_status_integra(self):
        dispositivo = DispositivoIO('127.0.0.1', 0) 
        server_thread = threading.Thread(target=dispositivo.iniciar_servidor, daemon=True)
        server_thread.start()

        # aguarda até o servidor estar pronto
        timeout = 2.0
        start = time.time()
        while (dispositivo.server_socket is None) and (time.time() - start < timeout):
            time.sleep(0.01)
        self.assertIsNotNone(dispositivo.server_socket, "Servidor não inicializou")

        port = dispositivo.server_socket.getsockname()[1]

        client = Controlador('127.0.0.1', port)
        self.assertTrue(client.conectar())
        resposta = client.enviar_comando("LER_STATUS")
        self.assertEqual(resposta, "DESLIGADO")
        client.fechar()

        dispositivo.parar_servidor()
        server_thread.join(timeout=1)

if __name__ == "__main__":
    unittest.main()
# Simulador de I/O Profibus/Profinet 

Este projeto é um simulador de comunicação industrial Cliente/Servidor em Python, baseado no Tema 4 da disciplina

## Escopo - Semana 1

O objetivo é criar os esqueletos de um servidor (Dispositivo I/O) e um cliente (Controlador) que usarão sockets TCP para comunicação. O servidor manterá um estado simulado (ex: "LIGADO") e o cliente enviará comandos (ex: "LER_STATUS").

## Estrutura do Código 

* `servidor_io.py`: Contém a classe `DispositivoIO`. Será responsável por ouvir conexões, gerenciar o estado e responder aos comandos.
* `cliente_controlador.py`: Contém a classe `Controlador`. Será responsável por conectar ao servidor e enviar os comandos de leitura/escrita.

## Como Executar 

1.  Certifique-se de ter o Python 3.10+ instalado.
2.  Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3.  **Para rodar:**
    * Execute o servidor em um terminal: `python servidor_io.py`
    * Execute o cliente em outro terminal: `python cliente_controlador.py`
  

## Equipe 4 

- Ana Sofia - [@Sun-cs-Sol](https://github.com/Sun-cs-Sol) - [Linkedin](https://www.linkedin.com/in/ana-sofia-moura-27b003248/)
- Camila Maria - [@camilamta275](https://github.com/camilamta275) - [Linkedin](https://www.linkedin.com/in/camilamta275/)
- Lucas Rodrigues - [@lucxsz-web](https://github.com/lucxsz-web) - [Linkedin](https://www.linkedin.com/in/lucas-rodrigues-08261b2ba/)
- René Melo - [@renysoo](https://github.com/renysoo) - [Linkedin](https://www.linkedin.com/in/renelucena/)
- Victor Ferreira - [@vic-fmr](https://github.com/vic-fmr) - [Linkedin](https://www.linkedin.com/in/victor-ferreira-marques/)

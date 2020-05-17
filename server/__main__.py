import json
import yaml
import socket
import logging
from argparse import ArgumentParser

from resolvers import find_server_action
from handlers import handle_tcp_request


config = {
    'host': 'localhost',
    'port': 8000,
    'buffersize': 1024,
}

parser = ArgumentParser()
parser.add_argument('-c', '--config', type=str, required=False,
                    help='Sets config path')
parser.add_argument('-ht', '--host', type=str, required=False,
                    help='Sets server host')
parser.add_argument('-p', '--port', type=str, required=False,
                    help='Sets server port')

args = parser.parse_args()

if args.config:
    with open(args.config) as file1:
        file_config = yaml.safe_load(file1)
        config.update(file_config or {})

host = args.host if args.host else config.get('host')
port = args.port if args.port else config.get('port')
buffersize = config.get('buffersize')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=(
        logging.FileHandler('server.log'),
        logging.StreamHandler(),
    )
)

try:
    sock = socket.socket() # создать сокет
    sock.bind((host, port)) # привязать сокет к IP-адресу и порту сервера 
    sock.listen(5) # готовность принимать соединение

    logging.info(f'Server started with {host}:{port}')

    action_mapping = find_server_action()

    while True:
        client, (client_host, client_port) = sock.accept() # принять запрос на установку соединения
        logging.info(f'Client {client_host}:{client_port} was connected')

        bytes_request = client.recv(buffersize) # принять данные
        bytes_response = handle_tcp_request(bytes_request, action_mapping)

        client.send(bytes_response)
        client.close()
        
except KeyboardInterrupt:
    logging.info("Server shutdown")
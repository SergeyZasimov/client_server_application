import json
import yaml
import socket
from argparse import ArgumentParser

from resolvers import find_server_action
from protocol import validate_request, make_500, make_400, make_404, make_200


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

try:
    sock = socket.socket() # создать сокет
    sock.bind((host, port)) # привязать сокет к IP-адресу и порту сервера 
    sock.listen(5) # готовность принимать соединение

    print(f'Server started with {host}:{port}')

    action_mapping = find_server_action()

    while True:
        client, (client_host, client_port) = sock.accept() # принять запрос на установку соединения
        print(f'Client {client_host}:{client_port} was connected')

        bytes_request = client.recv(buffersize) # принять данные

        request = json.loads(bytes_request)

        if validate_request(request):
            action = request.get('action')
            controller = action_mapping.get(action)
            if controller:
                try:
                    response = controller(request)
                    print(f'Request: {bytes_request.decode()}')
                except Exception as err:
                    response = make_500(request)
                    print(err)
            else:
                response = make_404(request)
        else:
            response = make_404(request)
            print(f'Wrong request: {request}')

        string_response = json.dumps(response)
        client.send(string_response.encode())
        client.close()
except KeyboardInterrupt:
    print("Server shutdown")
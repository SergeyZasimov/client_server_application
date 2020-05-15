import sys
import yaml
from argparse import ArgumentParser

def make_request(text):
    return{
        'data': text
    }

if __name__ == '__main__':
    config = {
        'host': 'localhost',
        'port': 8000
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

    print(args)
    message = input('Enter your message: ')
    request = make_request(message)
    print(f'Send message to {host}: {port}')
    print(request)
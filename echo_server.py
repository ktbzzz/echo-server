import socket
import sys
import traceback
import time

def server(log_buffer=sys.stderr):
    # configure socket and address
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    address = ('127.0.0.1', 10000)

    # bind and listen
    server_socket.bind(address)
    server_socket.listen(1)

    print('making a server on {0}:{1}'.format(*address), file=log_buffer)

    try:
        while True:
            print('waiting for a connection', file=log_buffer)
            connection, client_address = server_socket.accept()

            try:
                print('connection - {0}:{1}'.format(*client_address), file=log_buffer)

                while True:
                    buffer_size = 16
                    data = connection.recv(buffer_size)
                    print('received "{0}"'.format(data.decode('utf8')))
                    print('sent "{0}"'.format(data.decode('utf8')))
                    connection.sendall(data)

                    if len(data) < buffer_size:
                        break
            except Exception as e:
                traceback.print_exc()
                sys.exit(1)
            finally:
                print('echo complete, client connection closed', file=log_buffer)
                connection.close()

    except KeyboardInterrupt:
        server_socket.close()
        print('quitting echo server', file=log_buffer)

if __name__ == '__main__':
    server()
    sys.exit(0)

import socket
import time


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # Set a timeout so the socket does not block
    # indefinitely when trying to receive data.
    server.settimeout(0.2)
    server.bind(("127.0.0.1", 5002))
    message = b"your very important message "
    while True:
        server.sendto(message + str(time.time()).encode(), ('<broadcast>', 37020))
        print("message sent!")
        time.sleep(1)


if __name__ == '__main__':
    main()

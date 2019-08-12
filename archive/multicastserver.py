import socket


def main():
    MCAST_GRP = '224.0.2.1'
    MCAST_PORT = 0xF1FA
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
    sock.sendto(b'Hello World!', (MCAST_GRP, MCAST_PORT))

    print('Server listening')
    while True:
        data, address = sock.recvfrom(1024)
        # data = d[0]

        if not data:
            break

        sock.sendto(b'yes, im here!', address)
        print(data)
        print(address)


if __name__ == '__main__':
    main()

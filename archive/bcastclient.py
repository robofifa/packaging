import socket
import ipaddress


def main():
    IP = '192.168.56.1'
    MASK = '255.255.255.0'

    host = ipaddress.IPv4Address(IP)
    net = ipaddress.IPv4Network(IP + '/' + MASK, False)
    print('IP:', IP)
    print('Mask:', MASK)
    print('Subnet:', ipaddress.IPv4Address(int(host) & int(net.netmask)))
    print('Host:', ipaddress.IPv4Address(int(host) & int(net.hostmask)))
    print('Broadcast:', net.broadcast_address)

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.bind((str(net.broadcast_address), 37020))
    while True:
        data, addr = client.recvfrom(1024)
        print("received message: %s" % data)


if __name__ == '__main__':
    main()

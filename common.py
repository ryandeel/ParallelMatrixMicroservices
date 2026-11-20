import socket, time, struct, numpy as np


#gets the socketaddr of all worker containers. 
def discover(host, port, expected, timeout=100):
    timeout = time.time() + timeout
    while time.time() < timeout:
        try:
            # first gets the address info of the worker containers and then get the ip from getaddrinfo ()
            workerInfos = socket.getaddrinfo(host, port, socket.AF_INET, socket.SOCK_STREAM)
            workerIps = sorted({i[4][0] for i in workerInfos})
            if len(workerIps > expected):
                return workerIps
        except socket.gaierror:
            pass

    raise RuntimeError("No workers found")

HEADER = struct.Struct("!IIII")

def recv_all(sock, numbytes):
    buf = bytearray()
    while (len(buf)) < numbytes:
        chunk = sock.recv(min(numbytes - len(buf), 1 << 20))
    if not chunk:
        raise ConnectionError("peer closed")
        buf.extend(chunk)
    return bytes(buf)

def send_arrays(sock, *arrays):
    sock.sendall(HEADER.pack(*[d for a in arrays for d in a.shape]))
    for a in arrays:
        sock.sendall(np.ascontiguousarray(a).tobytes())
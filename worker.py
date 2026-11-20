import socket, struct, numpy as np
from common import *

# create the socket, bind to port 5000 for TCP communication, open port
srv = socket.socket(); srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("0.0.0.0", 5000)); srv.listen()

while True:
    conn, _ = srv.accept()
    with conn:
        ar, ac, br, bc = HEADER.unpack(recv_all(conn, HEADER.size))
        A = np.frombuffer(recv_all(conn, ar*ac*8), dtype=np.float64).reshape(ar, ac)
        B = np.frombuffer(recv_all(conn, br*bc*8), dtype=np.float64).reshape(br, bc)
        C = A @ B
        conn.sendall(struct.pack("!II", *C.shape) + C.tobytes())
import os, threading, socket, numpy as np
from common import *

def run_rowpartition(ip, a_part, B, results, index):
    with socket.create_connection((ip, 5000)) as s:
        send_arrays(s, a_part, B)
        row, column = struct.unpack("!II", recv_all(s,8))
        results[index] = np.frombuffer(recv_all(s, row*column*8), dtype=np.float64).reshape(row, column)

n_workers = int(os.environ["N_WORKERS"])
ips = discover(os.environ["WORKER_HOST"], 5000, n_workers)

A = np.random.rand(2000, 2000); B = np.random.rand(2000, 2000)
blocks = np.array_split(A, len(ips), axis=0)
results = [None] * len(ips)

threads = [threading.Thread(target=run_rowpartition, args=(ip, blk, B, results, i))
           for i, (ip, blk) in enumerate(zip(ips, blocks))]
[t.start() for t in threads]; [t.join() for t in threads]

C = np.vstack(results)
print("correct:", np.allclose(C, A @ B))
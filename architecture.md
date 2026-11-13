# Architecture for Our Single-Node Setup

## Coordinator (1 container)

**What does this container do?**
- Takes in matrix A and B (generated or given)
- Breaks the matrices into blocks
- Stores the blocks in the Volume and sends a message to Redis giving it a new task
- Waits on the results array, similar to how workers wait for tasks
- When completed, it looks in the Volume
- Then assembles the blocks

**What TCP?**
- Keeps an open connection to check results
- Sends messages to the Redis container to store in the task queue

## Redis (1 container)

**What does this container do?**
- Contains two arrays: Tasks and Results
- Tasks is a queue that worker containers pull from
- Results is also a queue that the coordinator pulls from for assembly
- With this setup we don't need to manually build a load balancer; this container just looks for the first worker waiting for a task

## Workers (n instances of containers)

**What do these containers do?**
- Each worker waits for a task in Redis (workers don't look, they just wait)
- Once a new task is appended, Redis gives the task to a worker
- Once a worker gets a task, it pulls the block from the Volume
- The worker does the computation on the given block
- Once finished, it saves the matrix as a `.npy` file in the Volume and writes to the results array in Redis saying the task is completed

**What TCP?**
- Creates an open connection with Redis until it receives a task
- Sends a message to Redis marking the task as completed, which updates the results array

## Volume (not a container, just a data store)

- Disk used to save data only
- Stores the results of the computed matrix for each block (`.npy` files)
- The coordinator reads and gets data from here
- Workers store data here and also read from it

## Data Flow (Example: 2×2 Grid of Blocks)

A and B are each split into a 2×2 grid of blocks, so C has 4 blocks to compute.

```
1. Coordinator splits A and B into blocks
   A → A_0_0  A_0_1  A_1_0  A_1_1
   B → B_0_0  B_0_1  B_1_0  B_1_1

2. Coordinator ──saves blocks──▶ Volume
   /data/A_0_0.npy ... /data/B_1_1.npy

3. Coordinator ──adds tasks──▶ Redis (tasks)
   (0,0)  (0,1)  (1,0)  (1,1)          one task per block of C

4. Redis (tasks) ──one task each──▶ Workers
   Worker 1 ← (0,0)   Worker 2 ← (0,1)   Worker 3 ← (1,0)   Worker 4 ← (1,1)

5. Volume ──input blocks──▶ Worker   (e.g. Worker 2, task (0,1))
   loads A_0_0, B_0_1, A_0_1, B_1_1
   computes C_0_1 = A_0_0 · B_0_1 + A_0_1 · B_1_1

6. Worker ──saves result──▶ Volume
   /data/C_0_1.npy

7. Worker ──"(0,1) done"──▶ Redis (results)

8. Redis (results) ──"(0,1) done"──▶ Coordinator
   Volume ──C_0_1.npy──▶ Coordinator  (placed at row 0, column 1 of C)

9. Once all 4 results are in, the Coordinator has the full matrix C
```

- **Redis** only carries small messages: which block to compute and which block is done
- **Volume** carries the actual matrix data (`.npy` files)
- Files are always saved to the Volume **before** the message is sent to Redis, so the file is ready when the message arrives

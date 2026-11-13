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

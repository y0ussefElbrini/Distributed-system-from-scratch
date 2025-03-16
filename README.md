# Distributed-system-from-scratch

## Introduction

This project focuses on implementing a distributed word count system using the **MapReduce** paradigm. The system distributes data processing across multiple servers, leveraging parallel computing to enhance performance compared to a sequential implementation.

The goal is to empirically demonstrate **Amdahl’s Law**, showing how parallel processing improves execution time while identifying the impact of sequential operations on overall performance.

## Architecture

The system is built using a **client-server architecture** with communication via **sockets**. The main steps in the process are:

1. **Server Initialization:** The client sends a list of available servers to each server.
2. **Splitting Data:** The client partitions a large text file into smaller chunks (splits) and distributes them across the servers.
3. **Map Phase:** Each server processes its assigned split to generate intermediate key-value pairs (words).
4. **Shuffle Phase:** The intermediate results are redistributed among servers based on a hash function.
5. **Reduce Phase:** Each server counts occurrences of words assigned to it and sends the results to the client.
6. **Merge and Sort:** The client merges results and sorts words based on frequency.

## Key Challenges & Solutions

### **1. Parallel Execution & Synchronization**
**Problem:**  
Initially, tasks ran asynchronously, leading to synchronization issues (e.g., reduce starting before shuffle was completed).  

**Solution:**  
- Implemented acknowledgment messages between client and servers to ensure that each phase starts only after the previous one is completed.
- Optimized synchronization by separating the **sending** and **receiving** loops, ensuring all servers complete their tasks before proceeding to the next phase.

### **2. Shuffle Phase Optimization**
**Problem:**  
The initial shuffle algorithm was inefficient due to excessive socket connections—each word was sent individually, significantly increasing execution time.  

**Solution:**  
- Instead of sending words one by one, each server now batches words into a dictionary structure `{server_index: [words]}` and sends them in bulk.
- This reduced shuffle time from **321 seconds to 50 seconds** (for an 8-server setup processing a 750MB file).

## Performance Analysis

To validate performance gains, we compared:
- **Distributed processing vs. Sequential processing**
- Execution times for each phase with different numbers of servers.

### **Results**

| Number of Servers | Map (s) | Shuffle (s) | Reduce (s) | Sort (s) |
|------------------|--------|----------|---------|--------|
| 1 (Sequential)   | 50.99  | 28.50    | 19.43   | N/A    |
| 4               | 15.69  | 195.55   | 13.41   | 16.60  |
| 8               | 6.55   | 48.77    | 4.92    | 16.70  |
| 16              | 4.16   | 32.84    | 1.93    | 15.79  |
| 32              | 2.28   | 12.88    | 0.71    | 18.56  |

### **Interpretation**
- As more servers are added, **Map and Reduce phases** significantly speed up.
- The **Shuffle phase** was a bottleneck but improved after optimization.
- The **Sort phase** remains sequential, limiting overall speedup, aligning with **Amdahl’s Law**.

## Prerequisites

This project is designed to run in a **local network environment** at **Télécom Paris**, where all available Linux machines can be accessed via SSH. It requires adaptation for use in different environments.

### **Requirements**
- **Operating System:** Linux (Tested on Télécom Paris lab machines)
- **Programming Language:** Python 3.x
- **Dependencies:** Standard Python libraries (socket, struct, os, threading, time)
- **Network Access:** SSH access to the lab machines
- **Files Required:**
  - `getMachines.sh`
  - `deploy.sh`
  - `server.py`
  - `client.py`
  - `machines.txt` (generated dynamically)

## Setup and Execution

### **Step 1: Select Available Machines**
Before running the Python scripts, you must select the available machines and deploy the necessary files.

Run the following script to find available machines and store them in `machines.txt`:

```bash
bash getMachines.sh <number_of_machines>
```
This script:

- Fetches the list of available machines from `tp.telecom-paris.fr`
- Tests SSH connectivity to each machine
- Saves the accessible machines into `machines.txt`

### **Step 2: Deploy Files**
Run the following script to deploy the necessary files to the selected machines:

```bash
bash deploy.sh
```

This script:

- Copies all necessary files to the remote machines
- Starts the `server.py` script on each machine

### **Step 3: Run the Client**

Run the following command to start the client:

```bash
python3 client.py
```


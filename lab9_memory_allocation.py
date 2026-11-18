# Lab 9: First Fit, Best Fit, Worst Fit memory allocation

# STEP 1: read the memory blocks
nb = int(input())                      # number of memory blocks
blocks = []                            # list of block sizes
for i in range(nb):                    # read each block size (one per line)
    blocks.append(int(input()))

# STEP 2: read the processes
np_ = int(input())                     # number of processes
procs = []                             # list of memory needed by each process
for i in range(np_):                   # read each process size (one per line)
    procs.append(int(input()))


# This function runs one strategy: "first", "best" or "worst"
def allocate(method):
    # STEP 3: make a fresh copy of memory. Each item is [name, size].
    # "EM" means the block is empty.
    memory = []
    for size in blocks:                # for every block
        memory.append(["EM", size])    # start as empty

    unallocated = []                   # processes that couldn't fit

    # STEP 4: place each process one by one
    for p in range(np_):               # p = 0, 1, 2 ...
        need = procs[p]                # memory this process needs
        chosen = -1                    # -1 = no block chosen yet

        # look at every block to choose one
        for i in range(len(memory)):
            if memory[i][0] == "EM" and memory[i][1] >= need:   # empty AND big enough
                if method == "first":
                    chosen = i         # first fit: take the first block that fits
                    break              # stop searching
                elif method == "best":
                    if chosen == -1 or memory[i][1] < memory[chosen][1]:
                        chosen = i     # best fit: keep the SMALLEST block that fits
                elif method == "worst":
                    if chosen == -1 or memory[i][1] > memory[chosen][1]:
                        chosen = i     # worst fit: keep the LARGEST block

        # STEP 5: allocate or mark as unallocated
        if chosen == -1:               # no block fits
            unallocated.append("P" + str(p + 1))   # e.g. "P5"
        else:
            leftover = memory[chosen][1] - need     # space left after placing process
            memory[chosen] = ["P" + str(p + 1), need]   # block now belongs to process
            if leftover > 0:                        # some space remains
                memory.insert(chosen + 1, ["EM", leftover])  # leftover becomes a new empty block

    # STEP 6: print the memory layout
    for block in memory:               # each block
        print(block[0], block[1])      # e.g. "P1 115" or "EM 185"

    if len(unallocated) == 0:          # every process got memory
        print("Unallocated Processes: None")
    else:                              # some did not
        print("Unallocated Processes:", " ".join(unallocated))


# STEP 7: run all three strategies
print("First Fit:")
allocate("first")
print("Best Fit:")
allocate("best")
print("Worst Fit:")
allocate("worst")

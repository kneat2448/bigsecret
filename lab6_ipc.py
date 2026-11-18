# Lab 6: IPC using a Pipe (parent -> child) and Shared Memory (child -> parent)
# Works on Linux/macOS only

import os                              # for pipe, fork, read, write, wait
from multiprocessing import Value      # Value = an integer stored in shared memory

# STEP 1: take input from the user
n = int(input("Number of elements: "))   # read how many numbers
arr = input("Array: ")                 # read the numbers as text, e.g. "10 20 30 40 50"

# STEP 2: create the pipe and the shared memory BEFORE fork, so both processes get them
r, w = os.pipe()                       # pipe gives 2 ends: r = read end, w = write end
shared_sum = Value('i', 0)             # shared memory for one integer ('i'), starting at 0

# STEP 3: create the child process
print("Parent process created.")
pid = os.fork()                        # returns 0 in child, child's PID in parent

if pid == 0:
    # ---------- CHILD PROCESS ----------
    os.close(w)                        # child only reads, so close the write end
    data = os.read(r, 1024).decode()   # read up to 1024 bytes from pipe, convert bytes -> text
    print("Child received array through pipe.")

    total = 0                          # start the sum at 0
    for x in data.split():             # split text "10 20 30" into ["10", "20", "30"]
        total = total + int(x)         # convert each to int and add to total
    print("Child computed sum =", total)

    shared_sum.value = total           # write the sum into shared memory
    print("Child stored result in shared memory.")
    os._exit(0)                        # child finishes

else:
    # ---------- PARENT PROCESS ----------
    os.close(r)                        # parent only writes, so close the read end
    print("Parent writing array to pipe.")
    os.write(w, arr.encode())          # convert text -> bytes and send it into the pipe
    os.close(w)                        # close write end (tells child that data is complete)

    os.wait()                          # wait for the child to finish

    print("Parent read sum from shared memory.")
    print("Final Sum =", shared_sum.value)   # read the sum the child stored

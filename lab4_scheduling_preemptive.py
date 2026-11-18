# Lab 4: Preemptive Priority (PPS), SRTF and Round Robin (RR)
# Input: n, then n lines "PID AT BT PRIORITY", then the time quantum
# Preemptive = a running process can be stopped if a better one arrives.
# Trick for PPS and SRTF: run the CPU ONE time unit at a time,
# and after every unit choose the best process again.


# This function prints the final table for any algorithm
def print_table(name, n, pid, at, bt, st, ct):
    print("\n" + name)                         # print algorithm name
    print("PID ST CT RT WT TAT")               # print column headings
    for i in range(n):                         # go through each process
        tat = ct[i] - at[i]                    # Turnaround = Completion - Arrival
        wt = tat - bt[i]                       # Waiting = Turnaround - Burst
        rt = st[i] - at[i]                     # Response = Start - Arrival
        print("P" + str(pid[i]), st[i], ct[i], rt, wt, tat)  # print one row


# ---------------- PPS (Preemptive Priority Scheduling) ----------------
def pps(n, pid, at, bt, pr):
    rem = bt.copy()                            # remaining time = burst time at the start
    st = [-1] * n                              # start time, -1 means "not started yet"
    ct = [0] * n                               # completion times
    time = 0                                   # CPU clock
    completed = 0                              # number of finished processes

    while completed < n:                       # repeat until all processes finish
        # STEP 1: among ARRIVED and UNFINISHED processes, find SMALLEST PRIORITY NUMBER
        best = -1                              # nothing chosen yet
        for i in range(n):                     # check every process
            if at[i] <= time and rem[i] > 0:   # arrived AND still has work left
                if best == -1 or pr[i] < pr[best]:   # first found OR higher priority
                    best = i                   # remember it

        # STEP 2: if nobody is ready, CPU is idle for 1 unit
        if best == -1:                         # no process available
            time = time + 1                    # move clock by 1
            continue                           # check again

        # STEP 3: record start time if this is its first time on the CPU
        if st[best] == -1:                     # never started before
            st[best] = time                    # save start time

        # STEP 4: run it for only 1 unit
        rem[best] = rem[best] - 1              # 1 unit of work done
        time = time + 1                        # clock moves by 1

        # STEP 5: if it has no work left, it is finished
        if rem[best] == 0:                     # finished
            ct[best] = time                    # save completion time
            completed = completed + 1          # count it

    print_table("Preemptive Priority", n, pid, at, bt, st, ct)   # print results


# ---------------- SRTF (Shortest Remaining Time First) ----------------
# EXACTLY the same as PPS, only it compares REMAINING TIME instead of priority.
def srtf(n, pid, at, bt):
    rem = bt.copy()                            # remaining time of each process
    st = [-1] * n                              # -1 = not started
    ct = [0] * n                               # completion times
    time = 0                                   # CPU clock
    completed = 0                              # finished count

    while completed < n:                       # repeat until all finish
        # STEP 1: among ARRIVED and UNFINISHED, find SMALLEST REMAINING TIME
        best = -1                              # nothing chosen yet
        for i in range(n):                     # check every process
            if at[i] <= time and rem[i] > 0:   # arrived AND unfinished
                if best == -1 or rem[i] < rem[best]:   # first found OR less time left
                    best = i                   # remember it

        # STEP 2: nobody ready -> CPU idle
        if best == -1:                         # no process available
            time = time + 1                    # move clock by 1
            continue                           # check again

        # STEP 3: first time on CPU -> save start time
        if st[best] == -1:                     # never started
            st[best] = time                    # save start time

        # STEP 4: run for 1 unit
        rem[best] = rem[best] - 1              # 1 unit of work done
        time = time + 1                        # clock moves by 1

        # STEP 5: check if finished
        if rem[best] == 0:                     # no work left
            ct[best] = time                    # save completion time
            completed = completed + 1          # count it

    print_table("SRTF", n, pid, at, bt, st, ct)   # print results


# ---------------- RR (Round Robin) ----------------
# Like FCFS, but each process runs for at most 'tq' units, then goes to the back of the queue.
def round_robin(n, pid, at, bt, tq):
    rem = bt.copy()                            # remaining time of each process
    st = [-1] * n                              # -1 = not started
    ct = [0] * n                               # completion times
    queue = []                                 # the ready queue (stores process indexes)
    added = [False] * n                        # has this process been put in the queue yet?
    time = 0                                   # CPU clock
    completed = 0                              # finished count

    while completed < n:                       # repeat until all finish
        # STEP 1: add processes that have arrived to the queue
        for i in range(n):                     # check every process
            if added[i] == False and at[i] <= time:   # not added yet AND arrived
                queue.append(i)                # put it at the back of the queue
                added[i] = True                # mark as added

        # STEP 2: if the queue is empty, CPU is idle
        if len(queue) == 0:                    # nobody waiting
            time = time + 1                    # move clock by 1
            continue                           # check again

        # STEP 3: take the process at the front of the queue
        i = queue.pop(0)                       # remove and get the first element

        # STEP 4: first time on CPU -> save start time
        if st[i] == -1:                        # never started
            st[i] = time                       # save start time

        # STEP 5: run it for the time quantum (or less if it finishes earlier)
        run = min(tq, rem[i])                  # smaller of quantum and remaining time
        time = time + run                      # clock moves forward
        rem[i] = rem[i] - run                  # reduce remaining time

        # STEP 6: processes that arrived DURING this run join the queue first
        for j in range(n):                     # check every process
            if added[j] == False and at[j] <= time:   # not added AND has arrived
                queue.append(j)                # add to back of queue
                added[j] = True                # mark as added

        # STEP 7: put the current process back, or mark it finished
        if rem[i] > 0:                         # still has work left
            queue.append(i)                    # goes to the back of the queue
        else:                                  # no work left
            ct[i] = time                       # save completion time
            completed = completed + 1          # count it

    print_table("Round Robin", n, pid, at, bt, st, ct)   # print results


# ---------------- MAIN PROGRAM ----------------
n = int(input())                               # read number of processes
pid = []                                       # process IDs
at = []                                        # arrival times
bt = []                                        # burst times
pr = []                                        # priorities
for i in range(n):                             # read each process line
    p, a, b, r = map(int, input().split())     # split line into 4 integers
    pid.append(p)                              # save PID
    at.append(a)                               # save arrival time
    bt.append(b)                               # save burst time
    pr.append(r)                               # save priority
tq = int(input())                              # read time quantum for Round Robin

pps(n, pid, at, bt, pr)                        # run Preemptive Priority
srtf(n, pid, at, bt)                           # run SRTF
round_robin(n, pid, at, bt, tq)                # run Round Robin

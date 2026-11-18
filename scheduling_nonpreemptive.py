# FCFS, SJF and NPS (Non-Preemptive Priority) scheduling
# Input: first line = n, then n lines of "PID AT BT PRIORITY"
# Non-preemptive = once a process starts, it runs till it finishes.


# This function prints the final table for any algorithm
def print_table(name, n, pid, at, bt, st, ct):
    print("\n" + name)                         # print algorithm name (with a blank line before)
    print("PID ST CT RT WT TAT")               # print the column headings
    for i in range(n):                         # go through every process one by one
        tat = ct[i] - at[i]                    # Turnaround Time = Completion - Arrival
        wt = tat - bt[i]                       # Waiting Time = Turnaround - Burst
        rt = st[i] - at[i]                     # Response Time = Start - Arrival
        print("P" + str(pid[i]), st[i], ct[i], rt, wt, tat)  # print one row of the table


# ---------------- FCFS (First Come First Serve) ----------------
def fcfs(n, pid, at, bt):
    st = [0] * n                               # list to store start time of each process
    ct = [0] * n                               # list to store completion time of each process
    done = [False] * n                         # False = not finished yet, True = finished
    time = 0                                   # the CPU clock, starts at 0
    completed = 0                              # how many processes have finished

    while completed < n:                       # repeat until all processes are finished
        # STEP 1: find the unfinished process that ARRIVED FIRST
        best = -1                              # -1 means "nothing chosen yet"
        for i in range(n):                     # check every process
            if done[i] == False:               # only look at unfinished ones
                if best == -1 or at[i] < at[best]:   # first one found OR arrived earlier
                    best = i                   # remember this process as the best so far

        # STEP 2: if the CPU is free before the process arrives, wait for it
        if time < at[best]:                    # process hasn't arrived yet
            time = at[best]                    # move the clock to its arrival time (CPU idle)

        # STEP 3: run the chosen process completely
        st[best] = time                        # it starts at the current time
        time = time + bt[best]                 # clock moves forward by its burst time
        ct[best] = time                        # it finishes at the new time
        done[best] = True                      # mark it as finished
        completed = completed + 1              # one more process is complete

    print_table("FCFS", n, pid, at, bt, st, ct)   # print FCFS results


# ---------------- SJF (Shortest Job First) ----------------
def sjf(n, pid, at, bt):
    st = [0] * n                               # start times
    ct = [0] * n                               # completion times
    done = [False] * n                         # finished or not
    time = 0                                   # CPU clock
    completed = 0                              # number of finished processes

    while completed < n:                       # repeat until all processes finish
        # STEP 1: among processes that have ARRIVED, find the SMALLEST BURST TIME
        best = -1                              # nothing chosen yet
        for i in range(n):                     # check every process
            if done[i] == False and at[i] <= time:      # unfinished AND already arrived
                if best == -1 or bt[i] < bt[best]:      # first found OR shorter burst
                    best = i                   # remember it

        # STEP 2: if no process has arrived yet, CPU stays idle for 1 unit
        if best == -1:                         # nobody is ready
            time = time + 1                    # move clock by 1
            continue                           # go back to the start of the loop

        # STEP 3: run the chosen process completely
        st[best] = time                        # start time
        time = time + bt[best]                 # run for full burst
        ct[best] = time                        # completion time
        done[best] = True                      # mark finished
        completed = completed + 1              # count it

    print_table("SJF", n, pid, at, bt, st, ct)    # print SJF results


# ---------------- NPS (Non-Preemptive Priority) ----------------
# EXACTLY the same as SJF, only the comparison uses PRIORITY instead of burst time.
# Smaller priority number = higher priority.
def nps(n, pid, at, bt, pr):
    st = [0] * n                               # start times
    ct = [0] * n                               # completion times
    done = [False] * n                         # finished or not
    time = 0                                   # CPU clock
    completed = 0                              # number of finished processes

    while completed < n:                       # repeat until all finish
        # STEP 1: among ARRIVED processes, find the SMALLEST PRIORITY NUMBER
        best = -1                              # nothing chosen yet
        for i in range(n):                     # check every process
            if done[i] == False and at[i] <= time:      # unfinished AND arrived
                if best == -1 or pr[i] < pr[best]:      # first found OR higher priority
                    best = i                   # remember it

        # STEP 2: nobody ready -> CPU idle for 1 unit
        if best == -1:                         # no process available
            time = time + 1                    # move clock by 1
            continue                           # check again

        # STEP 3: run the chosen process completely
        st[best] = time                        # start time
        time = time + bt[best]                 # run for full burst
        ct[best] = time                        # completion time
        done[best] = True                      # mark finished
        completed = completed + 1              # count it

    print_table("NPS", n, pid, at, bt, st, ct)    # print NPS results


# ---------------- MAIN PROGRAM ----------------
n = int(input())                               # read number of processes
pid = []                                       # list for process IDs
at = []                                        # list for arrival times
bt = []                                        # list for burst times
pr = []                                        # list for priorities
for i in range(n):                             # read one line for each process
    p, a, b, r = map(int, input().split())     # split "0 0 7 3" into 4 integers
    pid.append(p)                              # save PID
    at.append(a)                               # save arrival time
    bt.append(b)                               # save burst time
    pr.append(r)                               # save priority

fcfs(n, pid, at, bt)                           # run FCFS
sjf(n, pid, at, bt)                            # run SJF
nps(n, pid, at, bt, pr)                        # run NPS

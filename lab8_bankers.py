# Lab 8: Banker's Algorithm (find a safe sequence to avoid deadlock)

# STEP 1: read input
m = int(input())                               # number of resource types (e.g. 3)
total = list(map(int, input().split()))        # total instances of each resource (e.g. 10 5 7)
n = int(input())                               # number of processes (e.g. 5)

alloc = []                                     # allocation matrix
maxm = []                                      # max need matrix
for i in range(n):                             # one line per process
    row = list(map(int, input().split()))      # e.g. "0 1 0 7 5 3" -> [0,1,0,7,5,3]
    alloc.append(row[0:m])                     # first m numbers = allocated  -> [0,1,0]
    maxm.append(row[m:])                       # remaining m numbers = max    -> [7,5,3]

# STEP 2: calculate the Need matrix (need = max - allocation)
need = []                                      # empty need matrix
for i in range(n):                             # for each process
    row = []                                   # need row for this process
    for j in range(m):                         # for each resource
        row.append(maxm[i][j] - alloc[i][j])   # need = max - allocated
    need.append(row)                           # add row to matrix

# STEP 3: calculate Available (available = total - everything already allocated)
avail = []                                     # empty available list
for j in range(m):                             # for each resource
    used = 0                                   # how much of this resource is allocated
    for i in range(n):                         # add up allocation of all processes
        used = used + alloc[i][j]
    avail.append(total[j] - used)              # free = total - used

# STEP 4: find the safe sequence
finish = [False] * n                           # no process has finished yet
seq = []                                       # safe sequence goes here

found = True                                   # set True so the loop runs the first time
while found:                                   # keep looping while some process could run
    found = False                              # assume nobody can run in this round
    for i in range(n):                         # check every process
        if finish[i] == False:                 # only unfinished processes
            # check if need <= available for EVERY resource
            can_run = True                     # assume it can run
            for j in range(m):                 # check each resource
                if need[i][j] > avail[j]:      # needs more than available
                    can_run = False            # so it cannot run now

            if can_run:                        # process can finish safely
                for j in range(m):             # when it finishes...
                    avail[j] = avail[j] + alloc[i][j]   # ...it gives back its resources
                finish[i] = True               # mark it finished
                seq.append("P" + str(i))       # add it to the safe sequence
                found = True                   # we made progress, so loop again

# STEP 5: print the result
if len(seq) == n:                              # all processes finished -> safe state
    print("<" + ", ".join(seq) + ">")          # prints like <P1, P3, P4, P0, P2>
else:                                          # some process could never finish
    print("Unsafe state")

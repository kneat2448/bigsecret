# Lab 10: FIFO, Optimal (OPR) and LRU page replacement

# STEP 1: read input
nf = int(input())                      # number of frames (e.g. 3)
n = int(input())                       # number of pages in the sequence (e.g. 20)
pages = []                             # the page sequence
for i in range(n):                     # read each page (one per line)
    pages.append(int(input()))


# This function prints the chart, faults and hits
# chart = list of frame-copies (one copy after each page)
# marks = list of "F"/"H"
def print_chart(chart, marks):
    for r in range(nf):                # one printed line per frame
        line = "|"                     # start the line with |
        for col in chart:              # each column = frames after one page
            if col[r] == -1:           # -1 means the frame was empty
                line = line + " |"     # show a space
            else:
                line = line + str(col[r]) + "|"   # show the page number
        print(line)                    # print this frame's line
    print("|" + "|".join(marks) + "|") # last line: F or H for each page
    print("No. of Page Faults:", marks.count("F"))   # count F's
    print("No. of Hits:", marks.count("H"))          # count H's
    print()                            # blank line


# ---------------- FIFO (First In First Out) ----------------
# Replace the page that came in EARLIEST.
def fifo():
    frames = [-1] * nf                 # all frames empty (-1)
    pointer = 0                        # points to the oldest frame (next to replace)
    chart = []                         # saves frames after each page
    marks = []                         # saves F/H
    for p in pages:                    # go through each page
        if p in frames:                # page already in memory
            marks.append("H")          # hit
        else:                          # page not in memory
            marks.append("F")          # fault
            frames[pointer] = p        # put page in the oldest frame
            pointer = (pointer + 1) % nf   # move pointer to next frame (wraps back to 0)
        chart.append(frames.copy())    # save a copy of current frames
    print("FIFO:")
    print_chart(chart, marks)          # print results


# ---------------- LRU (Least Recently Used) ----------------
# Replace the page that was used LONGEST AGO.
def lru():
    frames = [-1] * nf                 # all frames empty
    last_used = [-1] * nf              # time when each frame was last used
    chart = []                         # saves frames after each page
    marks = []                         # saves F/H
    for t in range(n):                 # t = current time (position in sequence)
        p = pages[t]                   # current page
        if p in frames:                # page already in memory
            marks.append("H")          # hit
            last_used[frames.index(p)] = t   # update its last used time to now
        else:                          # page not in memory
            marks.append("F")          # fault
            if -1 in frames:           # there is an empty frame
                k = frames.index(-1)   # use the first empty frame
            else:                      # all frames full
                k = last_used.index(min(last_used))   # frame with the oldest use time
            frames[k] = p              # put page in that frame
            last_used[k] = t           # it is used now
        chart.append(frames.copy())    # save a copy
    print("LRU:")
    print_chart(chart, marks)          # print results


# ---------------- Optimal ----------------
# Replace the page that will be needed FARTHEST in the future (or never again).
def optimal():
    frames = [-1] * nf                 # all frames empty
    chart = []                         # saves frames after each page
    marks = []                         # saves F/H
    for t in range(n):                 # t = current position
        p = pages[t]                   # current page
        if p in frames:                # page already in memory
            marks.append("H")          # hit
        else:                          # page not in memory
            marks.append("F")          # fault
            if -1 in frames:           # there is an empty frame
                k = frames.index(-1)   # use it
            else:                      # all frames full -> choose a victim
                k = 0                  # frame to replace
                farthest = -1          # farthest next-use found so far
                for f in range(nf):    # check each frame
                    next_use = 999999  # assume this page is never used again
                    for j in range(t + 1, n):        # look at future pages
                        if pages[j] == frames[f]:    # found its next use
                            next_use = j             # save position
                            break                    # stop looking
                    if next_use > farthest:          # used later than the others
                        farthest = next_use          # update farthest
                        k = f                        # this frame is the victim
            frames[k] = p              # replace victim with the new page
        chart.append(frames.copy())    # save a copy
    print("OPR:")
    print_chart(chart, marks)          # print results


# STEP 2: run all three algorithms
fifo()
optimal()
lru()

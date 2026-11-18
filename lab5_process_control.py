# Lab 5: Parent creates 2 child processes and waits for both
# Works on Linux/macOS only (Windows has no fork)

import os                          # 'os' module has fork, wait and exit functions

# STEP 1: create child 1
c1 = os.fork()                     # fork() makes a copy of this program
                                   # it returns 0 inside the CHILD
                                   # and returns the child's PID inside the PARENT
if c1 == 0:                        # this part runs only inside child 1
    print("Child 1 is running")    # child 1 does its work
    os._exit(0)                    # child 1 ends with exit code 0 (= success)

# STEP 2: create child 2 (only the parent reaches here, because child 1 already exited)
c2 = os.fork()                     # make child 2
if c2 == 0:                        # this part runs only inside child 2
    print("Child 2 is running")    # child 2 does its work
    os._exit(1)                    # child 2 ends with exit code 1 (= failure)

# STEP 3: only the PARENT reaches this point

pid, status = os.waitpid(c1, 0)    # parent waits until child 1 finishes
                                   # 'status' stores how the child ended
if os.WEXITSTATUS(status) == 0:    # WEXITSTATUS gets the exit code from status
    print("Child 1: Completed Successfully.")   # exit code 0 -> success
else:
    print("Child 1: Execution Failed.")         # any other code -> failure

pid, status = os.waitpid(c2, 0)    # parent waits until child 2 finishes
if os.WEXITSTATUS(status) == 0:    # check child 2's exit code
    print("Child 2: Completed Successfully.")   # exit code 0 -> success
else:
    print("Child 2: Execution Failed.")         # exit code 1 -> failure (this case)

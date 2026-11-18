# Lab 7: Sleeping Barber Problem using semaphores and a mutex

import threading                       # for threads, semaphores and locks
import time                            # for sleep()

# STEP 1: take input
chairs = int(input("Number of waiting chairs: "))      # number of waiting chairs
num_customers = int(input("Number of customers: "))    # number of customers

# STEP 2: create the synchronization tools
customers = threading.Semaphore(0)     # counts waiting customers; starts at 0
                                       # barber "sleeps" on this when it is 0
barber = threading.Semaphore(0)        # barber uses this to say "I am ready"
mutex = threading.Lock()               # lock so only one thread changes 'waiting' at a time

waiting = []                           # list of customer ids sitting in waiting chairs


# STEP 3: what the barber does (runs forever)
def barber_function():
    while True:                        # barber works in an endless loop
        if len(waiting) == 0:          # no customers in the shop
            print("Barber sleeping...")

        customers.acquire()            # sem_wait: barber sleeps here until a customer arrives

        mutex.acquire()                # lock before touching the shared list
        cid = waiting.pop(0)           # take the first waiting customer
        mutex.release()                # unlock

        barber.release()               # sem_post: tell the customer "come, I'm ready"
        print("Barber is cutting hair of Customer", cid)
        time.sleep(1)                  # haircut takes 1 second
        print("Barber finished haircut for Customer", cid)


# STEP 4: what each customer does
def customer_function(cid):
    print("Customer", cid, "arrived.")

    mutex.acquire()                    # lock before checking the shared list
    if len(waiting) < chairs:          # is there a free chair?
        waiting.append(cid)            # yes -> sit in a chair
        print("Customer", cid, "is waiting.")
        mutex.release()                # unlock

        customers.release()            # sem_post: wake up the barber / tell him I'm here
        barber.acquire()               # sem_wait: wait until barber is ready for me
    else:                              # no free chair
        print("Customer", cid, "left (no chair available).")
        mutex.release()                # unlock and leave


# STEP 5: create and start the barber thread
# daemon=True means this thread stops automatically when the main program ends
b = threading.Thread(target=barber_function, daemon=True)
b.start()                              # start the barber

# STEP 6: create and start customer threads
threads = []                           # list to store customer threads
for i in range(1, num_customers + 1):  # customers numbered 1 to n
    t = threading.Thread(target=customer_function, args=(i,))   # new thread for customer i
    threads.append(t)                  # save it
    t.start()                          # start it
    time.sleep(0.4)                    # small gap so customers arrive one after another

# STEP 7: wait for all customers to finish
for t in threads:                      # go through every customer thread
    t.join()                           # wait for it to finish (like pthread_join)

time.sleep(1.5)                        # give the barber time to finish the last haircut

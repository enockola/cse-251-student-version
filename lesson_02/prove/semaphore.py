import threading
import time

def shared_resource(num):
    print(f'#{num}: I am the shared resource.')
    time.sleep(2)

def worker_thread(num, semaphore):
    # The with statement will decrease the semaphore by one.  If the semaphore is zero, then the thread
    # will wait until another thread is finished with the semaphore where it increments it by one
    with semaphore:
        shared_resource(num)

def main():
    threads = []

    # Allow 3 threads access to the critical section at a time
    semaphore = threading.Semaphore(3)

    for i in range(0, 10):
        thread = threading.Thread(target=worker_thread, args=(i, semaphore))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
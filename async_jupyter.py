import asyncio
from threading import Thread, Lock
import ipynbname

from IPython.core.events import EventManager
from IPython import get_ipython

import datetime


def notebook_hash():
    return ipynbname.path()

notebook_loops = {}
notebook_locks = {}



def asyncio_in_thread(init_lock):
    global notebook_loops
    global notebook_locks

    init_loop(init_lock)
    

    loop = get_event_loop()
    loop.run_until_complete(cell_execution_loop(notebook_locks[notebook_hash()]))

async def cell_execution_loop(lock: Lock):

    # Lock so you can release in the loop
    lock.acquire()
    while True:
        lock.release()  # let the notebook cell thread execute
        lock.acquire()  # and immediately lock again

        await asyncio.sleep(0)  # Let the event loop execute a scheduled task

has_registered_release = False

def acquire_pre_cell():
    global has_registered_release
    
    print("Acquiring cell lock!")
    notebook_locks[notebook_hash()].acquire()

    if not has_registered_release:
        has_registered_release = True
        ipython = get_ipython()

        ipython.events.register('post_execute', release_post_cell)
        print("POST EXECUTE");



def release_post_cell():

    try:
        notebook_locks[notebook_hash()].release()
        print("Releasing cell lock!")

    except RuntimeError as e:
        print("Cannot release lock, during registration, because it was never acquired")

        # This is probably because this is the cell that registered the cell execution callbacks
    finally:
        pass


def register_thread_safe_cell_execution():

    print("registering cell execution callbacks ")
    ipython = get_ipython()
    ipython.events.register('pre_execute', acquire_pre_cell)
    print("registered")




def get_event_loop():
    global notebook_loops
    global notebook_locks
    
    return notebook_loops[notebook_hash()]


init_lock = Lock()
init_lock.acquire()

def init_loop(init_lock):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError as e:
            loop = asyncio.new_event_loop()
    
        notebook_loops[notebook_hash()] = loop
        lock = Lock()
        notebook_locks[notebook_hash()] = lock
    
        register_thread_safe_cell_execution()

        init_lock.release()


thread = Thread(target=asyncio_in_thread, args=(init_lock,), name = f'async_jupyter {datetime.datetime.now()}').start()

init_lock.acquire()
init_lock.release()





import time
import json
import threading

def bot_clerk(items, inv = None) :
    if inv is None :
        with open('inventory.dat', 'r') as file :
            inv = json.load(file)
    
    if not items :
        return []
    
    cart = []
    lock = threading.Lock()

    f_lists = [[] for i in range(3)]
    for j, item in enumerate(items) :
        f_lists[j % len(f_lists)].append(item)

    total_threads = []
    for f_list in f_lists :
        threaded = threading.Thread(target = bot_fetcher, args = (f_list, cart, lock, inv))
        total_threads.append(threaded)
        threaded.start()

    for threaded in total_threads :
        threaded.join()

    return cart


def bot_fetcher(items, cart, lock, inv) :
    for num in items :
        time.sleep(inv[num][1])
        data = [num, inv[num][0]]
        with lock :
            cart.append(data)

import numpy as np
import queue

def get_item_from_queue(Q, timeout=0.001):
    """ Attempts to retrieve an item from the queue Q. If Q is
        empty, None is returned.
    
        Blocks for 'timeout' seconds in case the queue is empty,
        so don't use this method for speedy retrieval of multiple
        items (use get_all_from_queue for that).
    """
    try: 
        item = Q.get(True, timeout)
    except queue.Empty: 
        return None

    return item

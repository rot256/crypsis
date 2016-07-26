import Queue
import threading
import multiprocessing

JOB_MAP = 0
JOB_STOP = 1
JOB_SEARCH = 2

class MapWorker(threading.Thread):
    def __init__(self, pool):
        threading.Thread.__init__(self)
        self.pool = pool

    def run(self):
        while 1:
            job = self.pool.jobs.get()
            assert isinstance(job, tuple)
            if job[0] == JOB_STOP:
                break
            elif job[0] == JOB_SEARCH:
                self.search(job)
            elif job[0] == JOB_MAP:
                self.map(job)
            else:
                raise ValueError('Unknown job type')
            self.pool.jobs.task_done()

    def search(self, job):
        _, func, entry, res = job
        if func(entry):
            res.append(entry)

    def map(self, job):
        _, func, entry, res = job
        res.append(func(entry))

class MapPool():
    def __init__(self, threads=multiprocessing.cpu_count()):
        self.lock = threading.Lock()
        self.jobs = Queue.Queue(threads)
        self.workers = []
        for _ in range(threads):
            worker = MapWorker(self)
            worker.daemon = True
            worker.start()
            self.workers.append(worker)

    """ Coordinates a search job"""
    def search(self, f, entries):
        results = []
        for entry in entries:
            if results:
                break
            job = (JOB_SEARCH, f, entry, results)
            self.jobs.put(job)
        if len(results) == 0:
            self.jobs.join()
        if len(results) == 0:
            return None
        return results[0]

    """ Coordinates a map job """
    def map(self, f, entries):
        results = []
        for entry in entries:
            job = (JOB_MAP, f, entry, results)
            self.jobs.put(job)
        return results

    """ Cleanup a worker pool """
    def close(self):
        job = (JOB_STOP, 0) # Stop unpacking my tuples python
        for _ in self.workers:
            self.jobs.put(job)
        for worker in self.workers:
            worker.join()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

def search(f, entries, threads=multiprocessing.cpu_count()):
    # Do a simple search
    assert threads > 0
    if threads == 1:
        for entry in entries:
            if f(entry):
                return entry
        return None

    # Use a worker pool
    with MapPool(threads) as pool:
        return pool.search(f, entries)

def map(f, entries, threads=multiprocessing.cpu_count()):
    # Do a simple map
    assert threads > 0
    if threads == 1:
        return [f(e) for e in entries]

    # Use a worker pool
    with MapPool(threads) as pool:
        return pool.map(f, entries)

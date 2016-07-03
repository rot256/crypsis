import Queue
import threading
import multiprocessing

class MapWorker(threading.Thread):
    def __init__(self, pool):
        threading.Thread.__init__(self)
        self.pool = pool

    def run(self):
        while 1:
            job = self.pool.jobs.get()
            if job['type'] == 'stop':
                break
            elif job['type'] == 'search':
                if job['function'](job['entry']):
                    job['result'].append(job['entry'])
            else:
                raise ValueError('Unknown job type')
            self.pool.jobs.task_done()

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

    def search(self, f, entries):
        results = []
        for entry in entries:
            if results:
                break
            self.jobs.put({
                'type': 'search',
                'function': f,
                'entry': entry,
                'result': results,
            })
        if len(results) == 0:
            self.jobs.join()
        if len(results) == 0:
            return None
        return results[0]

    def close(self):
        for _ in self.workers:
            self.jobs.put({
                'type': 'stop'
            })
        for worker in self.workers:
            worker.join()

def search(f, entries, threads):
    if threads == 1:
        for entry in entries:
            if f(entry):
                return entry
        return None
    pool = MapPool(threads)
    res = pool.search(f, entries)
    pool.close()
    return res

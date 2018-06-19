from queue import Queue
from threading import Thread

class Worker(Thread):
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.result = []
        self.start()
    
    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try: 
            	val = func(*args, **kargs)
            	self.result.append(val)    # add returning values to worker result list
            except Exception as e: 
            	print(e)
            self.tasks.task_done()

class ThreadPool:
    def __init__(self, num_threads):
    	self.tasks = Queue(num_threads)
    	self.workers = [Worker(self.tasks) for _ in range(num_threads)]

    def add_task(self, func, *args, **kargs):
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        self.tasks.join()

    def get_result(self):
    	self.wait_completion()
    	results = []
    	for worker in self.workers:
    		for val in worker.result:
    			results.append(val) 
    	return results

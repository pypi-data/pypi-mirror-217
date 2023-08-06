import timeit
import pickle

class ProcessTimer:
    def __init__(self, process_name):
        self.process_name = process_name
        self.start = timeit.default_timer()
    
    def end(self):
        self.end = timeit.default_timer()

    def save(self, path):
        process_time = {
            self.process_name: self.end - self.start
        }
        with open(path, 'wb') as f:
            pickle.dump(process_time, f, protocol=pickle.HIGHEST_PROTOCOL)
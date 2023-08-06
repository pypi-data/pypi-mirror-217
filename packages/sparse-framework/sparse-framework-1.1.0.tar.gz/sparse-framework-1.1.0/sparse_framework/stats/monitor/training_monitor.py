from importlib.util import find_spec

from . import Monitor

class TrainingMonitor(Monitor):
    def __init__(self):
        self.processed_samples = 0
        self.processed_tasks = 0
        self.loss = None

    def get_metrics(self):
        return ['samples_processed', 'tasks_processed', 'loss']

    def get_stats(self):
        return [self.processed_samples, self.processed_tasks, self.loss]

    def add_point(self, newly_processed_samples = 0, newly_processed_tasks = 0, loss = None):
        self.processed_samples += newly_processed_samples
        self.processed_tasks += newly_processed_tasks
        if loss:
            self.loss = loss

from importlib.util import find_spec

class Monitor():
    def get_metrics(self):
        return []

    def get_stats(self):
        return []

class MonitorContainer(Monitor):
    def __init__(self, nic):
        from .network_monitor import NetworkMonitor
        from .time_monitor import TimeMonitor
        from .training_monitor import TrainingMonitor

        self.monitors = []
        self.monitors.append(TimeMonitor())
        self.monitors.append(NetworkMonitor(nic))
        self.monitors.append(TrainingMonitor())

    def get_metrics(self):
        metrics = []
        for monitor in self.monitors:
            metrics += monitor.get_metrics()
        return metrics

    def get_stats(self):
        stats = []
        for monitor in self.monitors:
            stats += monitor.get_stats()
        return stats

    def batch_processed(self, batch_size, loss):
        for monitor in self.monitors:
            if type(monitor).__name__ == 'TrainingMonitor':
                monitor.add_point(newly_processed_samples = batch_size, loss = loss)

    def task_processed(self):
        for monitor in self.monitors:
            if type(monitor).__name__ == 'TrainingMonitor':
                monitor.add_point(newly_processed_tasks = 1)

    def connection_timeout(self):
        for monitor in self.monitors:
            if type(monitor).__name__ == 'NetworkMonitor':
                monitor.add_connection_timeout()

    def broken_pipe_error(self):
        for monitor in self.monitors:
            if type(monitor).__name__ == 'NetworkMonitor':
                monitor.add_broken_pipe_error()

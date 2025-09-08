
import psutil
import time
import threading
import statistics


class PerformanceMonitor:
    def __init__(self, sample_interval=0.1):
        self.sample_interval = sample_interval
        self.monitoring = False
        self.cpu_samples = []
        self.memory_samples = []
        self.thread = None

    def start_monitoring(self):
        if self.monitoring:
            return

        self.monitoring = True
        self.cpu_samples = []
        self.memory_samples = []
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()

    def stop_monitoring(self):
        if not self.monitoring:
            return {}

        self.monitoring = False
        if self.thread:
            self.thread.join(timeout=1.0)

        return self._calculate_stats()

    def _monitor_loop(self):
        while self.monitoring:
            try:
                cpu_percent = psutil.cpu_percent(interval=None)

                memory_info = psutil.virtual_memory()
                memory_mb = memory_info.used / (1024 * 1024)

                self.cpu_samples.append(cpu_percent)
                self.memory_samples.append(memory_mb)

                time.sleep(self.sample_interval)

            except Exception as e:
                print(f"Erro no monitoramento: {e}")
                break

    def _calculate_stats(self):
        if not self.cpu_samples or not self.memory_samples:
            return {}

        return {
            'cpu': {
                'mean': statistics.mean(self.cpu_samples),
                'max': max(self.cpu_samples),
                'min': min(self.cpu_samples),
                'std_dev': statistics.stdev(self.cpu_samples) if len(self.cpu_samples) > 1 else 0
            },
            'memory': {
                'mean': statistics.mean(self.memory_samples),
                'max': max(self.memory_samples),
                'min': min(self.memory_samples),
                'std_dev': statistics.stdev(self.memory_samples) if len(self.memory_samples) > 1 else 0
            },
            'samples_count': len(self.cpu_samples)
        }


class BenchmarkTimer:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.perf_counter()

    def stop(self):
        if self.start_time is None:
            raise ValueError("Timer não foi iniciado")

        self.end_time = time.perf_counter()
        return self.end_time - self.start_time

    def reset(self):
        self.start_time = None
        self.end_time = None

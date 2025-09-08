"""
Módulo de Monitoramento de Desempenho
Monitora uso de CPU, memória e tempo de execução
"""

import psutil
import time
import threading
import statistics


class PerformanceMonitor:
    """Classe para monitoramento de desempenho do sistema"""

    def __init__(self, sample_interval=0.1):
        """
        Inicializa o monitor de desempenho

        Args:
            sample_interval (float): Intervalo entre amostras em segundos
        """
        self.sample_interval = sample_interval
        self.monitoring = False
        self.cpu_samples = []
        self.memory_samples = []
        self.thread = None

    def start_monitoring(self):
        """Inicia o monitoramento em background"""
        if self.monitoring:
            return

        self.monitoring = True
        self.cpu_samples = []
        self.memory_samples = []
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()

    def stop_monitoring(self):
        """Para o monitoramento e retorna estatísticas"""
        if not self.monitoring:
            return {}

        self.monitoring = False
        if self.thread:
            self.thread.join(timeout=1.0)

        return self._calculate_stats()

    def _monitor_loop(self):
        """Loop principal de monitoramento"""
        while self.monitoring:
            try:
                # Coleta uso de CPU (percentual)
                cpu_percent = psutil.cpu_percent(interval=None)

                # Coleta uso de memória (em MB)
                memory_info = psutil.virtual_memory()
                memory_mb = memory_info.used / (1024 * 1024)

                self.cpu_samples.append(cpu_percent)
                self.memory_samples.append(memory_mb)

                time.sleep(self.sample_interval)

            except Exception as e:
                print(f"Erro no monitoramento: {e}")
                break

    def _calculate_stats(self):
        """Calcula estatísticas dos dados coletados"""
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
    """Classe para medição precisa de tempo"""

    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        """Inicia a medição"""
        self.start_time = time.perf_counter()

    def stop(self):
        """Para a medição e retorna o tempo decorrido"""
        if self.start_time is None:
            raise ValueError("Timer não foi iniciado")

        self.end_time = time.perf_counter()
        return self.end_time - self.start_time

    def reset(self):
        """Reinicia o timer"""
        self.start_time = None
        self.end_time = None

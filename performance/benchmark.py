
import os
import time
import statistics
from .monitor import PerformanceMonitor, BenchmarkTimer
from algorithms.aes import AES
from algorithms.blowfish import Blowfish


class BenchmarkSuite:
    def __init__(self):
        self.monitor = PerformanceMonitor()
        self.timer = BenchmarkTimer()

    def run_encryption_benchmark(self, algorithm, data_sizes, iterations=5):
        results = {
            'algorithm': algorithm.__class__.__name__,
            'key_size': getattr(algorithm, 'key_size', 'N/A'),
            'data_sizes': data_sizes,
            'results': []
        }

        for size in data_sizes:
            size_results = {
                'data_size': size,
                'encryption_times': [],
                'decryption_times': [],
                'cpu_usage': [],
                'memory_usage': []
            }

            for i in range(iterations):
                test_data = self._generate_test_data(size)

                encrypt_result = self._benchmark_operation(
                    lambda: algorithm.encrypt(test_data),
                    f"encrypt_{i}"
                )

                iv, ciphertext = encrypt_result[0]
                decrypt_result = self._benchmark_operation(
                    lambda: algorithm.decrypt(iv, ciphertext),
                    f"decrypt_{i}"
                )

                size_results['encryption_times'].append(encrypt_result[1])
                size_results['decryption_times'].append(decrypt_result[1])
                size_results['cpu_usage'].append(encrypt_result[2]['cpu']['mean'])
                size_results['memory_usage'].append(encrypt_result[2]['memory']['mean'])

            size_results['avg_encrypt_time'] = statistics.mean(size_results['encryption_times'])
            size_results['avg_decrypt_time'] = statistics.mean(size_results['decryption_times'])
            size_results['avg_cpu_usage'] = statistics.mean(size_results['cpu_usage'])
            size_results['avg_memory_usage'] = statistics.mean(size_results['memory_usage'])

            results['results'].append(size_results)

        return results

    def run_comprehensive_benchmark(self, data_sizes=None, iterations=5):
        if data_sizes is None:
            data_sizes = [1024, 10240, 102400, 1048576]

        results = {
            'timestamp': time.time(),
            'data_sizes': data_sizes,
            'iterations': iterations,
            'algorithms': []
        }

        aes_configs = [
            {'name': 'AES-128', 'key_size': 128},
            {'name': 'AES-192', 'key_size': 192},
            {'name': 'AES-256', 'key_size': 256}
        ]

        for config in aes_configs:
            aes = AES(key_size=config['key_size'])
            aes.generate_key()

            benchmark_result = self.run_encryption_benchmark(
                aes, data_sizes, iterations
            )
            benchmark_result['name'] = config['name']
            results['algorithms'].append(benchmark_result)

        blowfish_configs = [
            {'name': 'Blowfish-128', 'key_size': 128},
            {'name': 'Blowfish-256', 'key_size': 256},
            {'name': 'Blowfish-448', 'key_size': 448}
        ]

        for config in blowfish_configs:
            blowfish = Blowfish(key_size=config['key_size'])
            blowfish.generate_key()

            benchmark_result = self.run_encryption_benchmark(
                blowfish, data_sizes, iterations
            )
            benchmark_result['name'] = config['name']
            results['algorithms'].append(benchmark_result)

        return results

    def _benchmark_operation(self, operation, operation_name):
        self.monitor.start_monitoring()

        self.timer.start()
        try:
            result = operation()
        except Exception as e:
            print(f"Erro na operação {operation_name}: {e}")
            result = None
        execution_time = self.timer.stop()
        self.timer.reset()

        system_stats = self.monitor.stop_monitoring()

        return result, execution_time, system_stats

    def _generate_test_data(self, size):
        return os.urandom(size)



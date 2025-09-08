"""
Módulo de Benchmark - Sistema de testes de desempenho
"""

import os
import time
import statistics
from .monitor import PerformanceMonitor, BenchmarkTimer
from algorithms.aes import AES
from algorithms.blowfish import Blowfish


class BenchmarkSuite:
    """Suite completa de benchmarks para algoritmos de criptografia"""

    def __init__(self):
        self.monitor = PerformanceMonitor()
        self.timer = BenchmarkTimer()

    def run_encryption_benchmark(self, algorithm, data_sizes, iterations=5):
        """
        Executa benchmark de criptografia para um algoritmo

        Args:
            algorithm: Instância do algoritmo (AES ou Blowfish)
            data_sizes: Lista de tamanhos de dados para testar (em bytes)
            iterations: Número de iterações por tamanho

        Returns:
            dict: Resultados do benchmark
        """
        results = {
            'algorithm': algorithm.__class__.__name__,
            'key_size': getattr(algorithm, 'key_size', 'N/A'),
            'data_sizes': data_sizes,
            'results': []
        }

        for size in data_sizes:
            print(f"Testando {algorithm.__class__.__name__} com {size} bytes...")

            size_results = {
                'data_size': size,
                'encryption_times': [],
                'decryption_times': [],
                'cpu_usage': [],
                'memory_usage': []
            }

            for i in range(iterations):
                # Gera dados de teste
                test_data = self._generate_test_data(size)

                # Teste de criptografia
                encrypt_result = self._benchmark_operation(
                    lambda: algorithm.encrypt(test_data),
                    f"encrypt_{i}"
                )

                # Teste de descriptografia
                iv, ciphertext = encrypt_result[0]  # Pega resultado da criptografia
                decrypt_result = self._benchmark_operation(
                    lambda: algorithm.decrypt(iv, ciphertext),
                    f"decrypt_{i}"
                )

                # Registra resultados
                size_results['encryption_times'].append(encrypt_result[1])
                size_results['decryption_times'].append(decrypt_result[1])
                size_results['cpu_usage'].append(encrypt_result[2]['cpu']['mean'])
                size_results['memory_usage'].append(encrypt_result[2]['memory']['mean'])

            # Calcula médias para este tamanho
            size_results['avg_encrypt_time'] = statistics.mean(size_results['encryption_times'])
            size_results['avg_decrypt_time'] = statistics.mean(size_results['decryption_times'])
            size_results['avg_cpu_usage'] = statistics.mean(size_results['cpu_usage'])
            size_results['avg_memory_usage'] = statistics.mean(size_results['memory_usage'])

            results['results'].append(size_results)

        return results

    def run_comprehensive_benchmark(self, data_sizes=None, iterations=5):
        """
        Executa benchmark completo comparando AES e Blowfish

        Args:
            data_sizes: Lista de tamanhos de dados (padrão: 1KB, 10KB, 100KB, 1MB)
            iterations: Número de iterações por teste

        Returns:
            dict: Resultados completos do benchmark
        """
        if data_sizes is None:
            data_sizes = [1024, 10240, 102400, 1048576]  # 1KB, 10KB, 100KB, 1MB

        results = {
            'timestamp': time.time(),
            'data_sizes': data_sizes,
            'iterations': iterations,
            'algorithms': []
        }

        # Testa AES com diferentes tamanhos de chave
        aes_configs = [
            {'name': 'AES-128', 'key_size': 128},
            {'name': 'AES-192', 'key_size': 192},
            {'name': 'AES-256', 'key_size': 256}
        ]

        for config in aes_configs:
            print(f"\n=== Executando benchmark {config['name']} ===")
            aes = AES(key_size=config['key_size'])
            aes.generate_key()

            benchmark_result = self.run_encryption_benchmark(
                aes, data_sizes, iterations
            )
            benchmark_result['name'] = config['name']
            results['algorithms'].append(benchmark_result)

        # Testa Blowfish com diferentes tamanhos de chave
        blowfish_configs = [
            {'name': 'Blowfish-128', 'key_size': 128},
            {'name': 'Blowfish-256', 'key_size': 256},
            {'name': 'Blowfish-448', 'key_size': 448}
        ]

        for config in blowfish_configs:
            print(f"\n=== Executando benchmark {config['name']} ===")
            blowfish = Blowfish(key_size=config['key_size'])
            blowfish.generate_key()

            benchmark_result = self.run_encryption_benchmark(
                blowfish, data_sizes, iterations
            )
            benchmark_result['name'] = config['name']
            results['algorithms'].append(benchmark_result)

        return results

    def _benchmark_operation(self, operation, operation_name):
        """
        Executa uma operação com monitoramento de desempenho

        Args:
            operation: Função a ser executada
            operation_name: Nome da operação para debug

        Returns:
            tuple: (resultado, tempo_execucao, estatisticas_sistema)
        """
        # Inicia monitoramento
        self.monitor.start_monitoring()

        # Executa operação com medição de tempo
        self.timer.start()
        try:
            result = operation()
        except Exception as e:
            print(f"Erro na operação {operation_name}: {e}")
            result = None
        execution_time = self.timer.stop()
        self.timer.reset()

        # Para monitoramento
        system_stats = self.monitor.stop_monitoring()

        return result, execution_time, system_stats

    def _generate_test_data(self, size):
        """
        Gera dados de teste aleatórios

        Args:
            size (int): Tamanho dos dados em bytes

        Returns:
            bytes: Dados aleatórios
        """
        return os.urandom(size)


def print_benchmark_summary(results):
    """
    Imprime um resumo dos resultados do benchmark

    Args:
        results (dict): Resultados do benchmark
    """
    print("\n" + "="*80)
    print("RESUMO DO BENCHMARK DE CRIPTOGRAFIA")
    print("="*80)

    print(f"Data/hora: {time.ctime(results['timestamp'])}")
    print(f"Tamanhos de dados testados: {[f'{s/1024:.0f}KB' if s < 1048576 else f'{s/1048576:.1f}MB' for s in results['data_sizes']]}")
    print(f"Iterações por teste: {results['iterations']}")
    print()

    for algorithm in results['algorithms']:
        print(f"Algoritmo: {algorithm['name']}")
        print("-" * 40)

        for result in algorithm['results']:
            size_kb = result['data_size'] / 1024
            size_mb = result['data_size'] / (1024 * 1024)

            if size_kb < 1024:
                size_str = f"{size_kb:.0f}KB"
            else:
                size_str = f"{size_mb:.1f}MB"

            print(f"Tamanho: {size_str}")
            print(".4f")
            print(".4f")
            print(".1f")
            print(".1f")
            print()

        print("-" * 40)
        print()

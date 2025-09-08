#!/usr/bin/env python3
"""
Estudo de Desempenho Computacional: AES vs Blowfish
Script principal para execução dos benchmarks
"""

import json
import os
from datetime import datetime
from performance.benchmark import BenchmarkSuite


def main():
    """Função principal do programa"""
    # Configurações do benchmark
    data_sizes = [1024, 10240, 102400, 1048576]  # 1KB, 10KB, 100KB, 1MB
    iterations = 5

    # Executa benchmark
    suite = BenchmarkSuite()
    results = suite.run_comprehensive_benchmark(
        data_sizes=data_sizes,
        iterations=iterations
    )

    # Salva resultados automaticamente
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"results/benchmark_results_{timestamp}.json"

    # Cria pasta results se não existir
    os.makedirs("results", exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Estudo de Desempenho Computacional: AES vs Blowfish
Script principal para execução dos benchmarks
"""

import json
import time
from datetime import datetime
from performance.benchmark import BenchmarkSuite, print_benchmark_summary


def main():
    """Função principal do programa"""
    # Configurações do benchmark
    data_sizes = [1024, 10240, 102400, 1048576]  # 1KB, 10KB, 100KB, 1MB
    iterations = 5

    print("Estudo de Desempenho Computacional")
    print("Comparação: AES vs Blowfish")
    print("=" * 50)
    print(f"Tamanhos de dados: {[f'{s/1024:.0f}KB' if s < 1048576 else f'{s/1048576:.1f}MB' for s in data_sizes]}")
    print(f"Iterações por teste: {iterations}")
    print()

    # Executa benchmark
    suite = BenchmarkSuite()

    start_time = time.time()
    results = suite.run_comprehensive_benchmark(
        data_sizes=data_sizes,
        iterations=iterations
    )
    end_time = time.time()

    # Imprime resumo
    print_benchmark_summary(results)

    # Mostra tempo total de execução
    total_time = end_time - start_time
    print(".2f")
    print()

    # Salva resultados automaticamente
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"benchmark_results_{timestamp}.json"

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"Resultados salvos em: {output_file}")


if __name__ == "__main__":
    main()

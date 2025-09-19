#!/usr/bin/env python3

import json
import os
from datetime import datetime
from performance.benchmark import BenchmarkSuite


def main():
    data_sizes = [1024, 5120, 10240, 51200, 102400, 512000, 1048576, 5242880]  # 1KB até 5MB
    iterations = 5

    suite = BenchmarkSuite()
    results = suite.run_comprehensive_benchmark(
        data_sizes=data_sizes,
        iterations=iterations
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"results/benchmark_results_{timestamp}.json"

    os.makedirs("results", exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()

import json
import matplotlib.pyplot as plt
import glob


def load_latest_results():
    result_files = glob.glob("results/benchmark_results_*.json")
    if not result_files:
        raise FileNotFoundError("Nenhum arquivo de resultados encontrado!")

    latest_file = max(result_files)
    with open(latest_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def format_size(size_bytes):
    if size_bytes >= 1048576:
        return f"{size_bytes/1048576:.1f} MB"
    elif size_bytes >= 1024:
        return f"{size_bytes/1024:.0f} KB"
    return f"{size_bytes} bytes"


def create_comparison_chart(results):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle('Comparação AES vs Blowfish - Tempo de Criptografia', fontsize=14, fontweight='bold')

    sizes = [format_size(s) for s in results['data_sizes']]

    for algorithm in results['algorithms']:
        encrypt_times = [r['avg_encrypt_time'] * 1000 for r in algorithm['results']]
        ax1.plot(sizes, encrypt_times, marker='o', linewidth=2, label=algorithm['name'])

    ax1.set_title('Tempo por Algoritmo')
    ax1.set_xlabel('Tamanho dos Dados')
    ax1.set_ylabel('Tempo (ms)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    x = range(len(sizes))
    width = 0.15
    colors = ['blue', 'green', 'red', 'orange', 'purple', 'brown']

    for i, algorithm in enumerate(results['algorithms']):
        encrypt_times = [r['avg_encrypt_time'] * 1000 for r in algorithm['results']]
        ax2.bar([pos + i*width for pos in x], encrypt_times, width,
                label=algorithm['name'], color=colors[i], alpha=0.8)

    ax2.set_title('Comparação Direta')
    ax2.set_xlabel('Tamanho dos Dados')
    ax2.set_ylabel('Tempo (ms)')
    ax2.set_xticks([pos + 2.5*width for pos in x])
    ax2.set_xticklabels(sizes)
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('results/benchmark_chart.png', dpi=300, bbox_inches='tight')
    plt.close()


def save_summary_table(results):
    with open('results/benchmark_summary.txt', 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("RESUMO DOS RESULTADOS - TEMPO MÉDIO DE CRIPTOGRAFIA (ms)\n")
        f.write("="*70 + "\n\n")

        header = "Algoritmo".ljust(15)
        for size in results['data_sizes']:
            header += format_size(size).rjust(10)
        f.write(header + "\n")
        f.write("-" * 70 + "\n")

        for algorithm in results['algorithms']:
            row = algorithm['name'].ljust(15)
            for result in algorithm['results']:
                time_ms = result['avg_encrypt_time'] * 1000
                row += f"{time_ms:6.2f}".rjust(10)
            f.write(row + "\n")

        f.write("\n" + "="*50 + "\n")
        f.write("COMPARAÇÃO FINAL (1MB de dados):\n")
        f.write("="*50 + "\n")

        for algorithm in results['algorithms']:
            time_1mb = algorithm['results'][-1]['avg_encrypt_time'] * 1000
            f.write(f"{algorithm['name']:<15} {time_1mb:6.2f} ms\n")


def main():
    try:
        results = load_latest_results()

        save_summary_table(results)

        create_comparison_chart(results)

    except Exception:
        pass

if __name__ == "__main__":
    main()

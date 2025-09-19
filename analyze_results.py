import json
import matplotlib.pyplot as plt
import numpy as np
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


def create_key_size_comparison(results):
    """Gráfico 1: Comparação por tamanho de chave"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('Comparação de Performance por Tamanho de Chave', fontsize=16, fontweight='bold')
    
    key_sizes = [128, 192, 256]
    algorithms_by_key = {'AES': {}, 'Blowfish': {}, 'Twofish': {}}
    
    # Organizar dados por algoritmo e tamanho de chave
    for alg in results['algorithms']:
        alg_name = alg['name'].split('-')[0]
        key_size = int(alg['name'].split('-')[1])
        if key_size in key_sizes:
            algorithms_by_key[alg_name][key_size] = [r['avg_encrypt_time'] * 1000 for r in alg['results']]
    
    sizes = [format_size(s) for s in results['data_sizes']]
    colors = {'AES': '#1f77b4', 'Blowfish': '#ff7f0e', 'Twofish': '#2ca02c'}
    
    for i, key_size in enumerate(key_sizes):
        ax = axes[i]
        ax.set_title(f'Chave de {key_size} bits', fontweight='bold')
        
        for alg_name, alg_data in algorithms_by_key.items():
            if key_size in alg_data:
                ax.plot(sizes, alg_data[key_size], marker='o', linewidth=2, 
                       label=alg_name, color=colors[alg_name])
        
        ax.set_xlabel('Tamanho dos Dados')
        ax.set_ylabel('Tempo (ms)')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/key_size_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_cpu_usage_chart(results):
    """Gráfico 2: Uso de CPU por algoritmo"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle('Análise de Uso de CPU', fontsize=16, fontweight='bold')
    
    # Gráfico de barras - CPU médio por algoritmo
    alg_names = [alg['name'] for alg in results['algorithms']]
    cpu_averages = []
    
    for alg in results['algorithms']:
        cpu_values = []
        for result in alg['results']:
            cpu_values.extend(result['cpu_usage'])
        cpu_avg = np.mean([x for x in cpu_values if x > 0]) if any(x > 0 for x in cpu_values) else 0
        cpu_averages.append(cpu_avg)
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(alg_names)))
    bars = ax1.bar(alg_names, cpu_averages, color=colors, alpha=0.8)
    ax1.set_title('CPU Médio por Algoritmo', fontweight='bold')
    ax1.set_ylabel('Uso de CPU (%)')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Adicionar valores nas barras
    for bar, value in zip(bars, cpu_averages):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # Gráfico de dispersão - CPU vs Tempo
    ax2.set_title('CPU vs Tempo de Execução', fontweight='bold')
    for i, alg in enumerate(results['algorithms']):
        cpu_vals = []
        time_vals = []
        for result in alg['results']:
            for j, cpu in enumerate(result['cpu_usage']):
                if cpu > 0:
                    cpu_vals.append(cpu)
                    time_vals.append(result['encryption_times'][j] * 1000)
        
        if cpu_vals and time_vals:
            ax2.scatter(cpu_vals, time_vals, label=alg['name'], 
                       color=colors[i], alpha=0.7, s=50)
    
    ax2.set_xlabel('Uso de CPU (%)')
    ax2.set_ylabel('Tempo (ms)')
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/cpu_usage_chart.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_efficiency_chart(results):
    """Gráfico 3: Eficiência (Throughput vs Recursos)"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle('Análise de Eficiência', fontsize=16, fontweight='bold')
    
    # Throughput por algoritmo (MB/s)
    alg_names = [alg['name'] for alg in results['algorithms']]
    throughputs = []
    memory_usage = []
    
    for alg in results['algorithms']:
        # Calcular throughput para o maior arquivo (1MB)
        largest_result = alg['results'][-1]  # 1MB
        avg_time = largest_result['avg_encrypt_time']
        throughput = (1048576 / avg_time) / (1024 * 1024)  # MB/s
        throughputs.append(throughput)
        
        # Uso médio de memória
        avg_memory = np.mean(largest_result['memory_usage'])
        memory_usage.append(avg_memory / 1024)  # MB
    
    # Gráfico de throughput
    colors = plt.cm.viridis(np.linspace(0, 1, len(alg_names)))
    bars1 = ax1.bar(alg_names, throughputs, color=colors, alpha=0.8)
    ax1.set_title('Throughput (1MB)', fontweight='bold')
    ax1.set_ylabel('MB/s')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, alpha=0.3, axis='y')
    
    for bar, value in zip(bars1, throughputs):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
    
    # Gráfico de eficiência (Throughput/Memória)
    efficiency = [t/m for t, m in zip(throughputs, memory_usage)]
    bars2 = ax2.bar(alg_names, efficiency, color=colors, alpha=0.8)
    ax2.set_title('Eficiência (Throughput/Memória)', fontweight='bold')
    ax2.set_ylabel('MB/s por MB RAM')
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(True, alpha=0.3, axis='y')
    
    for bar, value in zip(bars2, efficiency):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
                f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('results/efficiency_chart.png', dpi=300, bbox_inches='tight')
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
        print("Gerando análises e gráficos...")
        
        # Salvar resumo
        save_summary_table(results)
        print("✓ Resumo salvo")
        
        # Gerar os 3 gráficos principais
        create_key_size_comparison(results)
        print("✓ Gráfico de comparação por tamanho de chave")
        
        create_cpu_usage_chart(results)
        print("✓ Gráfico de uso de CPU")
        
        create_efficiency_chart(results)
        print("✓ Gráfico de eficiência")
        
        print("\nTodos os gráficos foram gerados na pasta 'results/':")
        print("- key_size_comparison.png")
        print("- cpu_usage_chart.png") 
        print("- efficiency_chart.png")

    except Exception as e:
        print(f"Erro ao gerar análises: {e}")

if __name__ == "__main__":
    main()

# Estudo de Desempenho Computacional: AES vs Blowfish

Este projeto implementa um estudo comparativo de desempenho entre os algoritmos de criptografia AES (Advanced Encryption Standard) e Blowfish, medindo uso de CPU e consumo de memória.

## Estrutura do Projeto

```
crypto/
├── algorithms/
│   ├── __init__.py
│   ├── aes.py          # Implementação AES
│   └── blowfish.py     # Implementação Blowfish
├── performance/
│   ├── __init__.py
│   ├── monitor.py      # Monitor de desempenho
│   └── benchmark.py    # Sistema de benchmark
├── main.py             # Script principal
├── requirements.txt    # Dependências
└── README.md          # Esta documentação
```

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso Básico

### Demonstração dos Algoritmos

Execute sem argumentos para ver uma demonstração básica:

```bash
python main.py
```

### Benchmark Completo

Execute benchmark completo com configurações padrão:

```bash
python main.py
```

### Benchmark Personalizado

```bash
# Teste com tamanhos específicos de dados
python main.py --data-sizes 1024 5120 10240

# Teste rápido com menos dados
python main.py --quick-test

# Salvar resultados em arquivo JSON
python main.py --output resultados.json

# Configurar número de iterações
python main.py --iterations 10
```

## Algoritmos Implementados

### AES (Advanced Encryption Standard)
- **Tamanhos de chave suportados**: 128, 192, 256 bits
- **Modo**: CBC (Cipher Block Chaining)
- **Padding**: PKCS7
- **Tamanho do bloco**: 16 bytes

### Blowfish
- **Tamanhos de chave suportados**: 32-448 bits (múltiplos de 8)
- **Modo**: CBC (Cipher Block Chaining)
- **Padding**: PKCS7
- **Tamanho do bloco**: 8 bytes

## Métricas de Desempenho

O estudo mede:

1. **Tempo de execução**:
   - Tempo de criptografia
   - Tempo de descriptografia

2. **Uso de CPU**:
   - Média, máximo, mínimo e desvio padrão

3. **Consumo de memória**:
   - Média, máximo, mínimo e desvio padrão

## Exemplo de Saída

```
Estudo de Desempenho Computacional
Comparação: AES vs Blowfish
==================================================
Tamanhos de dados: ['1KB', '10KB', '100KB', '1MB']
Iterações por teste: 5

=== Executando benchmark AES-128 ===
Testando AES com 1024 bytes...
Testando AES com 10240 bytes...
...

Algoritmo: AES-128
----------------------------------------
Tamanho: 1KB
Tempo médio criptografia: 0.0002s
Tempo médio descriptografia: 0.0001s
Uso médio CPU: 15.2%
Uso médio memória: 45.8MB

Tamanho: 10KB
Tempo médio criptografia: 0.0008s
...
```

## Módulos

### algorithms/
- **`aes.py`**: Implementação completa do AES com interface simples
- **`blowfish.py`**: Implementação completa do Blowfish

### performance/
- **`monitor.py`**: Monitora uso de CPU, memória e tempo de execução
- **`benchmark.py`**: Coordena execução dos testes e coleta métricas

## API dos Algoritmos

### Uso Básico

```python
from algorithms.aes import AES
from algorithms.blowfish import Blowfish

# AES
aes = AES(key_size=256)
aes.generate_key()
iv, ciphertext = aes.encrypt(b"dados")
plaintext = aes.decrypt(iv, ciphertext)

# Blowfish
blowfish = Blowfish(key_size=128)
blowfish.generate_key()
iv, ciphertext = blowfish.encrypt(b"dados")
plaintext = blowfish.decrypt(iv, ciphertext)
```

### Monitoramento de Desempenho

```python
from performance.monitor import PerformanceMonitor

monitor = PerformanceMonitor()
monitor.start_monitoring()
# ... execute operações ...
stats = monitor.stop_monitoring()
print(f"CPU médio: {stats['cpu']['mean']}%")
print(f"Memória média: {stats['memory']['mean']}MB")
```

## Requisitos do Sistema

- Python 3.7+
- Bibliotecas listadas em `requirements.txt`

## Notas Técnicas

- Todos os algoritmos usam modo CBC com vetores de inicialização aleatórios
- Padding PKCS7 é aplicado automaticamente
- As chaves são geradas aleatoriamente para cada teste
- O monitoramento de sistema é feito em background durante a execução
- Os resultados incluem estatísticas completas (média, máximo, mínimo, desvio padrão)

## Extensões Futuras

- Suporte a outros modos de operação (ECB, CTR, GCM)
- Comparação com outros algoritmos (ChaCha20, Twofish)
- Análise de segurança (tempo para quebra de chave)
- Testes com hardware dedicado (GPU, TPM)

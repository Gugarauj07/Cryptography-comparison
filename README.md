# Benchmark Framework: AES vs Blowfish Performance Analysis

Framework de análise comparativa de desempenho entre algoritmos de criptografia simétrica, implementando medições precisas de tempo de execução, uso de CPU e consumo de memória.

## Funcionamento dos Algoritmos

### AES (Advanced Encryption Standard)

**Princípio de Funcionamento:**
- Algoritmo de substituição-permutação iterativa
- Opera em blocos de 128 bits (16 bytes)
- Utiliza chaves de 128, 192 ou 256 bits
- Consiste em múltiplas rodadas de transformação

**Processo de Criptografia:**
1. **Expansão da Chave**: A chave mestre é expandida em um conjunto de subchaves
2. **Adição da Chave Inicial**: XOR entre bloco de dados e primeira subchave
3. **Rodadas**: 10, 12 ou 14 rodadas (dependendo do tamanho da chave)
4. **Transformações por Rodada**:
   - SubBytes: Substituição não-linear usando S-Box
   - ShiftRows: Rotação cíclica das linhas da matriz
   - MixColumns: Mistura das colunas através de operações no campo finito
   - AddRoundKey: XOR com subchave da rodada

**Vantagens:**
- Altamente seguro e aprovado pelo NIST
- Boa performance em hardware dedicado
- Paralelização eficiente possível

### Blowfish

**Princípio de Funcionamento:**
- Algoritmo Feistel de 16 rodadas
- Opera em blocos de 64 bits (8 bytes)
- Chaves variáveis de 32 a 448 bits
- Usa duas operações básicas: adição e XOR

**Processo de Criptografia:**
1. **Inicialização**: Arrays P e S são preenchidos com constantes
2. **Expansão da Chave**: P-array é modificado usando a chave
3. **Criptografia**: 16 rodadas Feistel
4. **Rodada Feistel**:
   - Divisão do bloco em esquerda (L) e direita (R)
   - F-function: Mistura usando S-boxes e operações aritméticas
   - L = L XOR resultado da F-function
   - Troca L ↔ R

**Características:**
- Algoritmo simétrico rápido
- Baixo consumo de memória
- Boa performance em software

## Implementação Técnica

### Arquitetura do Sistema

#### Camada de Algoritmos (`algorithms/`)
- **`aes.py`**: Classe AES com métodos encrypt/decrypt
- **`blowfish.py`**: Classe Blowfish com métodos encrypt/decrypt
- **Interface unificada**: Mesma API para ambos os algoritmos
- **Tratamento de erros**: Validação de parâmetros e estados

#### Camada de Monitoramento (`performance/`)
- **`monitor.py`**: Coleta métricas de sistema em tempo real
- **`PerformanceMonitor`**: Threading para monitoramento não-bloqueante
- **`BenchmarkTimer`**: Medição de tempo de alta precisão
- **Métricas**: CPU, memória, tempo de execução

#### Camada de Benchmark (`performance/`)
- **`benchmark.py`**: Orquestração completa dos testes
- **`BenchmarkSuite`**: Coordenação entre algoritmos e monitoramento
- **Controle estatístico**: Médias, desvios padrão, intervalos de confiança
- **Configuração experimental**: Tamanhos de dados, iterações, algoritmos

#### Camada de Análise (`analyze_results.py`)
- **Processamento de dados**: Carregamento e validação de resultados
- **Geração de relatórios**: Tabelas e gráficos comparativos
- **Visualização**: Gráficos matplotlib para análise visual
- **Formatação**: Arquivos TXT e PNG para diferentes usos

## Protocolo de Testes

### Configuração Experimental
- **Tamanhos de dados**: 1KB, 10KB, 100KB, 1MB
- **Iterações por teste**: 5 execuções
- **Geração de dados**: Pseudo-aleatória (os.urandom)
- **Chaves de teste**: Geradas aleatoriamente por algoritmo
- **Ambiente controlado**: Sistema isolado durante testes

### Métricas Coletadas

#### Temporais
- **Tempo de criptografia**: Duração da operação de cifração
- **Tempo de descriptografia**: Duração da operação de decifração
- **Latência total**: Soma criptografia + descriptografia
- **Throughput**: Dados processados por unidade de tempo

#### Recursos de Sistema
- **Uso de CPU**: Percentual médio, máximo e mínimo
- **Consumo de memória**: Pico e média durante execução
- **Overhead de sistema**: Impacto no sistema operacional

### Controle Estatístico
- **Média aritmética**: Valor central das métricas
- **Desvio padrão**: Variabilidade dos resultados
- **Distribuição**: Análise de normalidade dos dados
- **Confiabilidade**: Intervalo de confiança dos resultados

## O que foi Implementado

### Execução Automática (`main.py`)
- **Benchmark completo**: Executa todos os algoritmos sem intervenção manual
- **Configuração fixa**: Testa 1KB, 10KB, 100KB, 1MB com 5 iterações cada
- **Salvamento automático**: Resultados organizados em `results/` com timestamp

### Sistema de Monitoramento (`performance/monitor.py`)
- **Threading dedicado**: Monitoramento em background não-bloqueante
- **Coleta contínua**: Amostras de CPU e memória durante toda a execução
- **Timer de alta precisão**: Utiliza `time.perf_counter()` para medições exatas
- **Estatísticas completas**: Calcula média, máximo, mínimo e desvio padrão

### Orquestração de Testes (`performance/benchmark.py`)
- **Controle experimental rigoroso**: Mesma configuração para todos os algoritmos
- **Validação de integridade**: Verifica que criptografia ↔ descriptografia funcionam
- **Gestão inteligente de recursos**: Liberação adequada de memória entre testes
- **Tratamento robusto de erros**: Sistema continua mesmo com falhas individuais

### Análise de Resultados (`analyze_results.py`)
- **Processamento automático**: Localiza e carrega o último resultado disponível
- **Geração de múltiplos formatos**: Tabela textual + gráfico visual comparativo
- **Comparação direta**: Todas as métricas lado a lado para fácil análise
- **Organização de arquivos**: Tudo salvo de forma estruturada na pasta `results/`

## Protocolo Experimental Detalhado

### Sequência de Execução
1. **Preparação de Dados**: Geração de conteúdo pseudo-aleatório para cada tamanho
2. **Configuração de Algoritmo**: Chave aleatória única para cada teste
3. **Inicialização do Monitor**: Início da coleta de métricas de sistema
4. **Execução Controlada**: Criptografia seguida de descriptografia com validação
5. **Análise Estatística**: Cálculo de médias e limpeza de recursos

### Controle de Variáveis Independentes
- **Ambiente consistente**: Mesmo hardware/software para todos os testes
- **Dados idênticos**: Mesmo conjunto de dados para comparação justa
- **Execução sequencial**: Um algoritmo por vez para isolamento perfeito
- **Repetibilidade estatística**: 5 execuções por configuração para confiabilidade

### Métricas Técnicas Calculadas
- **Throughput**: Quantidade de dados processados por unidade de tempo
- **Latência**: Tempo total gasto por operação completa
- **Eficiência computacional**: Recursos consumidos por byte processado
- **Escalabilidade**: Como o desempenho varia com diferentes tamanhos de dados

## Arquivos de Saída

### Dados Brutos (`results/benchmark_results_*.json`)
Estrutura hierárquica completa contendo:
- Todas as medições individuais coletadas durante os testes
- Permite análise estatística aprofundada e personalizada
- Possibilita reprodução de gráficos específicos por métrica
- Serve como backup completo para validação de resultados

### Relatório Consolidado (`results/benchmark_summary.txt`)
- **Visão tabular comparativa**: Todos os algoritmos lado a lado
- **Métricas principais destacadas**: Foco no tempo médio de criptografia
- **Resumo executivo claro**: Comparação final para volumes maiores

### Visualização Gráfica (`results/benchmark_chart.png`)
- **Gráfico de linhas**: Mostra tendências claras por tamanho de dados
- **Gráfico de barras**: Comparação direta e visual entre algoritmos
- **Eixos duplos inteligentes**: Tempo e uso de CPU simultaneamente
- **Legendas informativas**: Identificação imediata dos algoritmos testados

## Aspectos Técnicos de Segurança

### Vetores de Inicialização (IV)
- **Geração criptográfica**: Utiliza `os.urandom` para entropia máxima
- **Unicidade garantida**: Novo IV gerado para cada operação individual
- **Tamanho apropriado**: 16 bytes para AES, 8 bytes para Blowfish

### Gerenciamento Seguro de Chaves
- **Geração robusta**: Entropia máxima disponível no sistema operacional
- **Armazenamento temporário**: Chaves mantidas apenas na memória volátil
- **Destruição automática**: Limpeza via garbage collector do Python

### Padding Criptográfico
- **Padrão PKCS#7**: Implementado conforme RFC 5652
- **Compatibilidade total**: Padrão amplamente adotado na indústria
- **Segurança verificada**: Resistente a ataques de oracle de padding

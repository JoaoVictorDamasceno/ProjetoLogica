# Avaliação de LLMs em Consequência Lógica: Texto Direto vs. Z3 Solver

Este projeto propõe um arcabouço experimental para avaliar a capacidade de raciocínio lógico do modelo **Gemini 3.1 Flash Lite**. O objetivo é mensurar e comparar duas abordagens de resolução de problemas de consequência lógica:
1. **Abordagem Direta:** A LLM recebe premissas e conclusões em português e deve julgar diretamente a validade do argumento.
2. **Abordagem via Solver (Z3):** A LLM recebe o problema em português e deve programar um script em Python utilizando a biblioteca `z3-solver` para deduzir a resposta matematicamente.

---

## Arquitetura do projeto

O código está estruturado modularmente dentro do diretório `src/`:
* `logic_generator.py`: Cria fórmulas proposicionais aleatórias (Ground Truth).
* `z3_solver.py`: Valida matematicamente as fórmulas geradas usando o Z3 (gabarito oficial).
* `nl_translator.py`: Traduz os operadores lógicos abstratos para sentenças em português.
* `dataset_builder.py`: Unifica os módulos acima para gerar e salvar o lote de dados estruturado.
* `llm_direct.py`: Gerencia a engenharia de prompt para a Abordagem 1 (Direta).
* `llm_solver.py`: Gerencia a geração de código e execução em subprocesso para a Abordagem 2 (Z3).
* `experiment_runner.py`: Script unificado que executa o experimento completo de ponta a ponta de forma resiliente.
* `metrics_analyzer.py`: Processa os JSONs de resultados e calcula Acurácia, Precisão, Recall e F1-Score.
* `visualize_metrics.py`: Consome os relatórios estatísticos e plota o gráfico comparativo final.

---

## Como executar o projeto

### 1. Pré-requisitos
Certifique-se de ter o Python 3.10 ou superior instalado. Clone o repositório, crie seu ambiente virtual e instale as dependências listadas no arquivo `requirements.txt`:

```bash
# Criar e ativar ambiente virtual se necessário
python -m venv venv
source venv/bin/activate  # No Windows use: venv\Scripts\activate

# Instalar dependências automaticamente
pip install -r requirements.txt
```

### 2. Configuração de credenciais
Crie um arquivo chamado `.env` na raiz do projeto e insira sua chave da API do Google Gemini:
```env
GEMINI_API_KEY=SUA_CHAVE_AQUI
```

### 3. Pipeline de execução

Execute os scripts na ordem abaixo a partir da raiz do projeto para reproduzir o experimento:

**Passo A - Gerar a base de dados:**
Gera os argumentos lógicos, valida com Z3 local, traduz para português e salva em `data/dataset_final.json`.
```bash
python src/dataset_builder.py
```

**Passo B - Rodar o experimento com a LLM:**
Consome o dataset gerado, envia as requisições para o Gemini e executa o salvamento incremental em `data/results_full.json`.
```bash
python src/experiment_runner.py
```

**Passo C - Extrair métricas mientíficas:**
Compara as previsões obtidas pela IA com o gabarito real e gera relatórios estatísticos de acertos e falhas.
```bash
python src/metrics_analyzer.py
```

**Passo D - Gerar visualização gráfica:**
Lê as métricas extraídas no passo anterior e plota o gráfico de barras duplo.
```bash
python src/visualize_metrics.py
```

---

## Resultados Esperados
Após a execução completa, o diretório `data/` conterá os seguintes artefatos consolidados:
* `metrics_report.json`: Relatório estático com Acurácia, Precisão, Recall e F1-Score.
* `error_analysis.json`: Lista de IDs catalogando os Falsos Positivos e Falsos Negativos da IA.
* `metrics_comparison.png`: Gráfico renderizado em alta resolução comparando visualmente as abordagens.

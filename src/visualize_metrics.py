import json
import os
import matplotlib.pyplot as plt
import numpy as np

def generate_charts(input_file="data/metrics_report.json", output_file="data/metrics_comparison.png"):
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Arquivo não encontrado: {input_file}. Rode o metrics_analyzer.py primeiro.")
        
    with open(input_file, 'r', encoding='utf-8') as f:
        report = json.load(f)
        
    labels = ['Acurácia', 'Precisão', 'Recall', 'F1-Score']
    direct_metrics = report['direct_approach']
    solver_metrics = report['solver_approach']
    
    direct_values = [
        direct_metrics['accuracy'],
        direct_metrics['precision'],
        direct_metrics['recall'],
        direct_metrics['f1']
    ]
    
    solver_values = [
        solver_metrics['accuracy'],
        solver_metrics['precision'],
        solver_metrics['recall'],
        solver_metrics['f1']
    ]
    
    x = np.arange(len(labels))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width/2, direct_values, width, label='Abordagem Direta (LLM)', color='#4C72B0')
    rects2 = ax.bar(x + width/2, solver_values, width, label='Abordagem via Código (Z3)', color='#55A868')
    
    ax.set_ylabel('Pontuação (0.0 a 1.0)')
    ax.set_title('Comparação de Desempenho: Raciocínio Direto vs. Z3 Solver')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 1.1)
    ax.legend(loc='lower right')
    
    ax.bar_label(rects1, padding=3, fmt='%.2f')
    ax.bar_label(rects2, padding=3, fmt='%.2f')
    
    fig.tight_layout()
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    plt.savefig(output_file, dpi=300) # Salva com alta resolução
    print(f"Gráfico gerado com sucesso! Arquivo salvo em: {output_file}")

if __name__ == "__main__":
    generate_charts()
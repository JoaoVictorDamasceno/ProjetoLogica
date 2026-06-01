import json
import os
import time

from llm_direct import evaluate_direct_logic
from llm_solver import generate_z3_code, execute_generated_code

def call_with_retry(func, *args, max_retries=3, base_delay=5.0):
    for attempt in range(max_retries):
        try:
            result = func(*args)
            
            # Se a função rodou sem dar exceção e trouxe um resultado válido
            if result is not None:
                return result
                
            print(f"    [Aviso] Resposta nula ou fora do padrão. Tentativa {attempt + 1}/{max_retries}")
            
        except Exception as e:
            print(f"    [Erro] Falha na comunicação: {e}. Tentativa {attempt + 1}/{max_retries}")
        
        # Se não for a última tentativa
        if attempt < max_retries - 1:
            tempo_espera = base_delay * (attempt + 1)
            print(f"    -> Aguardando {tempo_espera}s antes de tentar novamente...")
            time.sleep(tempo_espera)
            
    print("    [Falha Crítica] Máximo de tentativas alcançado. Pulando amostra.")
    return 

def run_full_experiment(input_file="data/dataset_final.json", output_file="data/results_full.json", limit=None, delay=5.0):
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Arquivo não encontrado: {input_file}")
        
    with open(input_file, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
        
    if limit:
        dataset = dataset[:limit]
        
    print(f"=== Iniciando Experimento Completo para {len(dataset)} amostras ===")
    results = []
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    for i, item in enumerate(dataset):
        print(f"\n[{i+1}/{len(dataset)}] ID: {item['id']}")
        
        result_item = item.copy()
        
        #ABORDAGEM 1: Raciocínio Direto
        print("  -> Rodando Abordagem 1 (Direta)...")
        pred_direct = call_with_retry(
            evaluate_direct_logic, 
            item["premises_text"], 
            item["conclusion_text"]
        )
        result_item["llm_direct_prediction"] = pred_direct
        time.sleep(delay)
        
        #ABORDAGEM 2: Código Z3
        print("  -> Rodando Abordagem 2 (Z3 Code)...")
        z3_code = call_with_retry(
            generate_z3_code, 
            item["premises_text"], 
            item["conclusion_text"]
        )
        
        pred_solver = None
        if z3_code:
            print("  -> Executando código Python/Z3 gerado...")
            pred_solver = execute_generated_code(z3_code)
            
        result_item["generated_code"] = z3_code
        result_item["llm_solver_prediction"] = pred_solver
        
        results.append(result_item)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
            
        print(f"  [Status] Salvo. Esperado: {item['ground_truth_valid']} | Direto: {pred_direct} | Z3: {pred_solver}")
        
        if i < len(dataset) - 1:
            time.sleep(delay)

    print(f"\n=== Experimento finalizado com sucesso! ===")
    print(f"Resultados consolidados em: {output_file}")

if __name__ == "__main__":
    run_full_experiment(limit=10, delay=5.0)
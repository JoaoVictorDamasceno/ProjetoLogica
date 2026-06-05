import json
import os

def calculate_metrics(y_true, y_pred):
    valid_pairs = [(t, p) for t, p in zip(y_true, y_pred) if p is not None]
    
    if not valid_pairs:
        return {
            "accuracy": 0, 
            "precision": 0, 
            "recall": 0, 
            "f1": 0, 
            "total_valid": 0, 
            "failures": len(y_true)
        }
    
    # TP (True Positive), TN (True Negative), FP (False Positive), FN (False Negative)
    tp = sum(1 for t, p in valid_pairs if t is True and p is True)
    tn = sum(1 for t, p in valid_pairs if t is False and p is False)
    fp = sum(1 for t, p in valid_pairs if t is False and p is True)
    fn = sum(1 for t, p in valid_pairs if t is True and p is False)
    
    accuracy = (tp + tn) / len(valid_pairs)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "total_valid": len(valid_pairs),
        "failures": len(y_true) - len(valid_pairs)
    }

def extract_error_cases(dataset):
    errors = {
        "direct_false_positives": [],
        "direct_false_negatives": [],
        "solver_false_positives": [],
        "solver_false_negatives": [],
        "execution_failures": []
    }
    
    for item in dataset:
        gt = item["ground_truth_valid"]
        pred_direct = item.get("llm_direct_prediction")
        pred_solver = item.get("llm_solver_prediction")
        
        # analisando Erros da Abordagem Direta
        if pred_direct is not None:
            if pred_direct != gt: 
                if pred_direct is True and gt is False:
                    errors["direct_false_positives"].append({"id": item["id"], "type": item["type"]})
                elif pred_direct is False and gt is True:
                    errors["direct_false_negatives"].append({"id": item["id"], "type": item["type"]})
                else:
                    errors["execution_failures"].append({"id": item["id"], "approach": "direct"})
                    
        # Analisando Erros da Abordagem Z3
        if pred_solver is not None:
            if pred_solver != gt:  
                if pred_solver is True and gt is False:
                    errors["solver_false_positives"].append({"id": item["id"], "type": item["type"]})
                elif pred_solver is False and gt is True:
                    errors["solver_false_negatives"].append({"id": item["id"], "type": item["type"]})
                else:
                    errors["execution_failures"].append({"id": item["id"], "approach": "solver"})
                    
    return errors

def run_analysis(input_file="data/results_full.json", output_metrics="data/metrics_report.json", output_errors="data/error_analysis.json"):
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Arquivo não encontrado: {input_file}. Rode o experiment_runner.py primeiro.")
        
    with open(input_file, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
        
    print(f"=== Iniciando Análise de Métricas ({len(dataset)} amostras) ===")
    
    y_true = [item["ground_truth_valid"] for item in dataset]
    y_pred_direct = [item.get("llm_direct_prediction") for item in dataset]
    y_pred_solver = [item.get("llm_solver_prediction") for item in dataset]
    
    metrics_direct = calculate_metrics(y_true, y_pred_direct)
    metrics_solver = calculate_metrics(y_true, y_pred_solver)
    
    report = {
        "direct_approach": metrics_direct,
        "solver_approach": metrics_solver
    }
    
    os.makedirs(os.path.dirname(output_metrics), exist_ok=True)
    with open(output_metrics, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=4)
        
    errors = extract_error_cases(dataset)
    with open(output_errors, 'w', encoding='utf-8') as f:
        json.dump(errors, f, indent=4, ensure_ascii=False)
        
    print("\n[RESULTADOS - ABORDAGEM 1: RACIOCÍNIO DIRETO]")
    print(json.dumps(metrics_direct, indent=2))
    print("\n[RESULTADOS - ABORDAGEM 2: LLM + Z3 SOLVER]")
    print(json.dumps(metrics_solver, indent=2))
    
    
if __name__ == "__main__":
    run_analysis()
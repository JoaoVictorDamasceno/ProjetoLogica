import os
import json
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Configura a chave da API do Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Chave GEMINI_API_KEY não encontrada no arquivo .env")

client = genai.Client(api_key=api_key)

MODEL_ID = 'gemini-3.5-flash'

def evaluate_direct_logic(premises_text, conclusion_text):
    premises_formatted = "\n".join([f"{i+1}. {p}" for i, p in enumerate(premises_text)])
    
    prompt = f"""Você é um especialista em lógica formal. 
Avalie se a conclusão apresentada é uma consequência lógica estrita das premissas fornecidas.

Premissas:
{premises_formatted}

Conclusão:
{conclusion_text}

Responda APENAS com a palavra "VÁLIDO" se a conclusão for uma consequência lógica, ou "INVÁLIDO" se não for. Não adicione nenhuma explicação.
"""
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt
        )
        
        answer = response.text.strip().upper()
        
        if "INVÁLIDO" in answer:
            return False
        elif "VÁLIDO" in answer:
            return True
        else:
            print(f"Aviso: Resposta fora do padrão detectada: {answer}")
            return None 
            
    except Exception as e:
        print(f"Erro ao chamar a API do Gemini: {e}")
        return None

def run_direct_evaluation(input_file="data/dataset_final.json", output_file="data/results_direct.json", limit=15, delay=5.0):
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Arquivo não encontrado: {input_file}. Rode o dataset_builder.py primeiro.")
        
    with open(input_file, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
        
    if limit:
        dataset = dataset[:limit]
        
    print(f"Iniciando avaliação direta de {len(dataset)} exemplos (Pausa de {delay}s entre chamadas)...")
    
    results = []
    for i, item in enumerate(dataset):
        print(f"Processando [{i+1}/{len(dataset)}] ID: {item['id']}...", end=" ")
        
        llm_prediction = evaluate_direct_logic(
            item["premises_text"], 
            item["conclusion_text"]
        )
        
        print(f"Resposta LLM: {llm_prediction} | Esperado: {item['ground_truth_valid']}")
        
        result_item = item.copy()
        result_item["llm_direct_prediction"] = llm_prediction
        results.append(result_item)
        
        if i < len(dataset) - 1:
            time.sleep(delay)
            
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
        
    print(f"\nAvaliação concluída. Resultados salvos em: {output_file}")

if __name__ == "__main__":
    run_direct_evaluation(limit=15, delay=5.0)
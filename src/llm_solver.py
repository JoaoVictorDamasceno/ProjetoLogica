import os
import json
import time
import subprocess
import tempfile
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Chave GEMINI_API_KEY não encontrada no arquivo .env")

client = genai.Client(api_key=api_key)
MODEL_ID = 'gemini-3.1-flash-lite'

def generate_z3_code(premises_text, conclusion_text):
    premises_formatted = "\n".join([f"{i+1}. {p}" for i, p in enumerate(premises_text)])
    prompt = f"""Você é um engenheiro de software especialista em Python e Z3 Solver.
Escreva um script Python completo usando a biblioteca `z3` para verificar se a conclusão abaixo é
uma consequência lógica das premissas.
Premissas:
{premises_formatted}
Conclusão:
{conclusion_text}
REGRAS OBRIGATÓRIAS:
1. Declare variáveis booleanas apropriadas no Z3.
2. Adicione as premissas ao solver.
3. Use prova por contradição (adicione a negação da conclusão ao solver).
4. Se solver.check() == unsat, imprima EXATAMENTE "RESULTADO_Z3: VÁLIDO".
5. Se não, imprima EXATAMENTE "RESULTADO_Z3: INVÁLIDO".
6. RETORNE APENAS O CÓDIGO PYTHON. Não adicione blocos de markdown (```python), não
escreva explicações.
"""
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f" [Erro API] Falha ao gerar código: {e}")
        return None

def execute_generated_code(code_string):
    if not code_string:
        return None
    
    clean_code = code_string.replace("```python", "").replace("```", "").strip()
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as temp_file:
        temp_file.write(clean_code)
        temp_path = temp_file.name
        
    try:
        result = subprocess.run(["python", temp_path], capture_output=True, text=True, timeout=10)
        output = result.stdout.upper()
        
        # Fallback
        if result.returncode != 0:
            print(f" [Erro de Sintaxe no Código da IA] {result.stderr.strip()}")
            return None
            
        if "RESULTADO_Z3: VÁLIDO" in output:
            return True
        elif "RESULTADO_Z3: INVÁLIDO" in output:
            return False
        else:
            print(f" [Erro Lógico] Saída não reconhecida. Stdout: {output}")
            return None
    except subprocess.TimeoutExpired:
        print(" [Erro Timeout] O código demorou muito para rodar.")
        return None
    finally:
        os.remove(temp_path)

def run_solver_evaluation(input_file="data/dataset_final.json", output_file="data/results_solver.json", limit=15, delay=5.0):
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Arquivo não encontrado: {input_file}")
        
    with open(input_file, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
        
    if limit:
        dataset = dataset[:limit]
        
    print(f"Iniciando Abordagem 2 (LLM + Z3) para {len(dataset)} exemplos...")
    results = []
    
    for i, item in enumerate(dataset):
        print(f"\n[{i+1}/{len(dataset)}] Processando ID: {item['id']}")
        print(" 1. Solicitando código ao Gemini...")
        generated_code = generate_z3_code(item["premises_text"], item["conclusion_text"])
        
        print(" 2. Executando código gerado no ambiente local...")
        llm_prediction = execute_generated_code(generated_code)
        
        print(f" -> Resultado do Código: {llm_prediction} | Gabarito Esperado: {item['ground_truth_valid']}")
        
        result_item = item.copy()
        result_item["llm_solver_prediction"] = llm_prediction
        result_item["generated_code"] = generated_code
        results.append(result_item)
        
        if i < len(dataset) - 1:
            time.sleep(delay)
            
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
        
    print(f"\nAvaliação concluída. Resultados salvos em: {output_file}")

if __name__ == "__main__":
    run_solver_evaluation(limit=5, delay=5.0)
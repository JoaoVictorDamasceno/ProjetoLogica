import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configura a chave da API do Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Chave GEMINI_API_KEY não encontrada no arquivo .env")

genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-3.5-flash')

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
        response = model.generate_content(prompt)
        answer = response.text.strip().upper()
        
        # Converte a resposta em texto para um valor booleano
        if "INVÁLIDO" in answer:
            return False
        elif "VÁLIDO" in answer:
            return True
        else:
            print(f"Aviso: Resposta fora do padrão detectada: {answer}")
            return None # Retorna None se a LLM não seguir as instruções
            
    except Exception as e:
        print(f"Erro ao chamar a API do Gemini: {e}")
        return None
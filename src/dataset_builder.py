import json
import os
import uuid
from logic_generator import generate_batch
from z3_solver import check_logical_consequence
from nl_translator import (
    translate_formula_to_text,
    generate_vocabulary_mapping,
    VARIABLES
)

def create_final_dataset(filename="../data/dataset_final.json", size=100):
    # Garante que a pasta data existe
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    print(f"Gerando batch de {size} argumentos brutos...")
    dataset_raw = generate_batch(size)

    dataset_final = []

    print("Processando Z3 e tradução de linguagem natural...")

    for item in dataset_raw:

        if item.get("ground_truth_valid") is None:
            is_valid = check_logical_consequence(
                item["premises"],
                item["conclusion"]
            )

            item["ground_truth_valid"] = is_valid

        vocab_mapping = generate_vocabulary_mapping(VARIABLES)

        premises_text = [
            translate_formula_to_text(p, vocab_mapping)
            for p in item["premises"]
        ]

        conclusion_text = translate_formula_to_text(
            item["conclusion"],
            vocab_mapping
        )

        record = {
            "id": str(uuid.uuid4())[:8],  # Gera um ID curto e único
            "type": item["type"],
            "premises_formula": item["premises"],
            "conclusion_formula": item["conclusion"],
            "premises_text": premises_text,
            "conclusion_text": conclusion_text,
            "ground_truth_valid": item["ground_truth_valid"]
        }

        dataset_final.append(record)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dataset_final, f, indent=4, ensure_ascii=False)

    print(f"Dataset final criado com sucesso em: {filename}")

if __name__ == "__main__":
    #gera um dataset de 200 exemplos
    create_final_dataset(size=200)
    
    with open("../data/dataset_final.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
        print("\n--- Amostra do Dataset Gerado ---")
        print(json.dumps(data[0], indent=2, ensure_ascii=False))
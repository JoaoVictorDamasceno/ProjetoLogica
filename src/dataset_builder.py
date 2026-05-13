import json
import os
from logic_generator import generate_batch
from z3_solver import check_logical_consequence

def create_raw_dataset(filename="../data/dataset_raw.json", size=50):

    # garante que a pasta data existe
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    print(f"Gerando batch de {size} argumentos...")
    dataset = generate_batch(size)

    print("Calculando o Ground Truth via Z3...")
    for item in dataset:
        if item.get("ground_truth_valid") is None:
           is_valid = check_logical_consequence(
            item["premises"],
            item["conclusion"]
        )
           item["ground_truth_valid"] = is_valid

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)

    print(f"Dataset bruto criado com sucesso em: {filename}")

if __name__ == "__main__":
    create_raw_dataset(size=100)
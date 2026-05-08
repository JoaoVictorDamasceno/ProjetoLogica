import random

# Variáveis proposicionais padrão
VARIABLES = ['P', 'Q', 'R', 'S']

def generate_simple_argument():
    
    var1, var2 = random.sample(VARIABLES, 2)
    
    is_valid = random.choice([True, False])
    
    if is_valid:
        premises = [f"{var1} IMPLIES {var2}", var1]
        conclusion = var2
    else:
        premises = [f"{var1} IMPLIES {var2}", var2]
        conclusion = var1
        
    return {
        "premises": premises,
        "conclusion": conclusion,
        "type": "simple_implication",
        "ground_truth_valid": is_valid
    }

def generate_complex_formula(depth=1):
    if depth == 0:
        return random.choice(VARIABLES)
        
    op = random.choice(['AND', 'OR', 'IMPLIES', 'NOT'])
    
    if op == 'NOT':
        # NOT só recebe um argumento
        inner = generate_complex_formula(depth - 1)
        return f"NOT({inner})"
    else:
        # Operadores binários
        left = generate_complex_formula(depth - 1)
        right = generate_complex_formula(depth - 1)
        return f"({left} {op} {right})"

def generate_complex_argument(num_premises=3, max_depth=2):
    premises = [generate_complex_formula(depth=random.randint(0, max_depth)) for _ in range(num_premises)]
    conclusion = generate_complex_formula(depth=random.randint(0, max_depth))
    
    return {
        "premises": premises,
        "conclusion": conclusion,
        "type": "complex_random",
        "ground_truth_valid": None
    }

def generate_batch(size=10):
    batch = []
    for _ in range(size):
        if random.choice(["simple", "complex"]) == "simple":
            batch.append(generate_simple_argument())
        else:
            batch.append(generate_complex_argument())
    return batch
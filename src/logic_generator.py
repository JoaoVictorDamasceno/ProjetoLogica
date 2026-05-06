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
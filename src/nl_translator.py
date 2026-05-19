import random

# Banco de proposições simples para preencher as variáveis lógicas
PROPOSITIONS_BANK = [
    "chove",
    "a rua fica molhada",
    "o sol brilha",
    "eu vou à praia",
    "o sistema falha",
    "o alarme dispara",
    "a energia cai",
    "o trânsito fica lento",
    "o prazo é cumprido",
    "o cliente aprova"
]

def generate_vocabulary_mapping(variables_needed):
    if len(variables_needed) > len(PROPOSITIONS_BANK):
        raise ValueError("Variáveis necessárias excedem o tamanho do banco de proposições")
        
    sampled_props = random.sample(PROPOSITIONS_BANK, len(variables_needed))
    return dict(zip(variables_needed, sampled_props))

# Variáveis globais baseadas no gerador
VARIABLES = ['P', 'Q', 'R', 'S']

def translate_formula_to_text(formula_str, vocab_mapping):
    s = formula_str.strip()
    
    # Caso base
    if s in vocab_mapping:
        return vocab_mapping[s]
        
    # Tratamento de Negação
    if s.startswith("NOT(") and s.endswith(")"):
        inner_text = translate_formula_to_text(s[4:-1], vocab_mapping)
        return f"não é verdade que {inner_text}"
        
    if s.startswith("(") and s.endswith(")"):
        nivel = 0
        engloba_tudo = True
        for char in s[1:-1]:
            if char == '(': nivel += 1
            elif char == ')': nivel -= 1
            if nivel < 0: 
                engloba_tudo = False
                break
        if engloba_tudo:
            return translate_formula_to_text(s[1:-1], vocab_mapping)

    nivel = 0
    for i in range(len(s) - 1, -1, -1):
        if s[i] == ')': nivel += 1
        elif s[i] == '(': nivel -= 1
        elif nivel == 0 and s[i] == ' ':
            # Substituição usando templates de texto
            for op in [" IMPLIES ", " AND ", " OR "]:
                if s[i-len(op)+1 : i+1] == op:
                    esq = translate_formula_to_text(s[:i-len(op)+1], vocab_mapping)
                    dir = translate_formula_to_text(s[i+1:], vocab_mapping)
                    
                    if "IMPLIES" in op: 
                        return f"se {esq}, então {dir}"
                    if "AND" in op: 
                        return f"{esq} e {dir}"
                    if "OR" in op: 
                        return f"{esq} ou {dir}"
                        
    return formula_str
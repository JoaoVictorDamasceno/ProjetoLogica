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
        raise ValueError("Variáveis necessárias excedem o tamanho do banco de proposições.")
        
    sampled_props = random.sample(PROPOSITIONS_BANK, len(variables_needed))
    return dict(zip(variables_needed, sampled_props))

# Variáveis globais baseadas no gerador
VARIABLES = ['P', 'Q', 'R', 'S']
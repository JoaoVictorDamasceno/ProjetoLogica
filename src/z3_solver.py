from z3 import Bool, And, Or, Not, Implies, Solver, unsat

# Criação das variáveis booleanas no Z3
Z3_VARS = {name: Bool(name) for name in ['P', 'Q', 'R', 'S']}

def parse_to_z3(formula_str):
    """
    Converte a string da fórmula proposicional para uma expressão do Z3.
    """
    s = formula_str.strip()

    # Caso Base: Variável simples
    if s in Z3_VARS:
        return Z3_VARS[s]
    
    if s.startswith("NOT(") and s.endswith(")"):
        return Not(parse_to_z3(s[4:-1]))
    
    # remove parênteses externos redundantes
    if s.startswith("(") and s.endswith(")"):
        nivel = 0
        engloba_tudo = True
        for char in s[1:-1]:
            if char == '(': nivel += 1
            elif char == ')': nivel -= 1
            if nivel < 0: # parênteses fecharam antes do final
                engloba_tudo = False
                break
        if engloba_tudo:
            return parse_to_z3(s[1:-1])
        
    # encontra o operador principal
    nivel = 0
    for i in range(len(s) - 1, -1, -1):
        if s[i] == ')': nivel += 1
        elif s[i] == '(': nivel -= 1
        elif nivel == 0 and s[i] == ' ':
            for op in [" IMPLIES ", " AND ", " OR "]:
                if s[i-len(op)+1 : i+1] == op:
                    esq = parse_to_z3(s[:i-len(op)+1])
                    dir = parse_to_z3(s[i+1:])

                    if "IMPLIES" in op: return Implies(esq, dir)
                    if "AND" in op: return And(esq, dir)
                    if "OR" in op: return Or(esq, dir)

    raise ValueError(f"Erro de sintaxe. Não foi possível fazer o parse de: {formula_str}")
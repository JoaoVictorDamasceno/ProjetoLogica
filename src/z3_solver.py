from z3 import Bool, And, Or, Not, Implies, Solver, unsat

Z3_VARS = {name: Bool(name) for name in ['P', 'Q', 'R', 'S']}

def parse_to_z3(formula_str):
    s = formula_str.strip()

    # Caso base
    if s in Z3_VARS:
        return Z3_VARS[s]
    
    # Tratamento de negação
    if s.startswith("NOT(") and s.endswith(")"):
        nivel = 0
        engloba_tudo = True
        for char in s[4:-1]:
            if char == '(': nivel += 1
            elif char == ')': nivel -= 1
            if nivel < 0: 
                engloba_tudo = False
                break
        if engloba_tudo:
            return Not(parse_to_z3(s[4:-1]))
    
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
            return parse_to_z3(s[1:-1])
        
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

def check_logical_consequence(premises_strs, conclusion_str):
    solver = Solver()
    for p_str in premises_strs:
        z3_premise = parse_to_z3(p_str)
        solver.add(z3_premise)

    z3_conclusion = parse_to_z3(conclusion_str)
    solver.add(Not(z3_conclusion))

    is_valid = (solver.check() == unsat)
    return bool(is_valid)

if __name__ == "__main__":
    # Testando Modus Ponens
    print("Modus Ponens Válido?", check_logical_consequence(["P IMPLIES Q", "P"], "Q"))
    
    # Testando Falácia
    print("Falácia Válida?", check_logical_consequence(["P IMPLIES Q", "Q"], "P"))
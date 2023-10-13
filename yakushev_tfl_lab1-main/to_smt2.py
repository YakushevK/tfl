from models import Constructor
from copy import deepcopy


def collect_nonunit_coefs(arity: dict[str,int]):
    unit_coefs = set()
    nonunit_coefs = set()
    monotoins2 = []
    for name, ar in arity.items():
        s = ''
        s += '(assert (or (and '
        if ar>0:
            for i in range(1, ar+1):
                nonunit_coefs.add(f'{name}{i}')
                s += f'(> {name}{i} 1) '
            s = s[:-1]
        else:
            s += 'false'
        unit_coefs.add(f'{name}{ar+1}')
        s += f') (> {name}{ar+1} 0)))'
        monotoins2.append(s)

    coefs = unit_coefs | nonunit_coefs
    
    declarations = [f'(declare-const {c} Int)'for c in coefs]
    # для гарантии выполнения f(x) = x 
    monotoins = [f'(assert (>= {c} 1))' for c in nonunit_coefs]
    monotoins += [f'(assert (>= {c} 0))' for c in unit_coefs]
    
    return declarations, monotoins + monotoins2


def arithm_to_smt(coefs: list[list[str]]) -> str:
    coefs_prods = ['(* ' + ' '.join(c) + ')' for c in coefs]
    prods_sum = '(+ ' + ' '.join(coefs_prods) + ')'
    return prods_sum


def build_ineqs_list(c1: Constructor, c2: Constructor):
    d1, d2 = deepcopy(c1.d), deepcopy(c2.d)
    
    for k in (set(d1.keys()) | set(d2.keys())):
        if k not in d1:
            d1[k] = [['0']]
        if k not in d2:
            d2[k] = [['0']]
    
    # если нет единички, обязательно добавляем
    # видимо, слева и справа просто по одной переменной
    # напр. x = y
    if '1' not in d1:
        d1['1'] =[['0']]
        d2['1'] =[['0']]
    # разбираемся с частью для единички
    pairs = []
    for k in set(d1.keys()) - set(['1']):
        pairs.append((arithm_to_smt(d1[k]), arithm_to_smt(d2[k])))

    # единичку отдельно
    unit_pair = (arithm_to_smt(d1['1']), arithm_to_smt(d2['1']))

    return pairs, unit_pair

        
counter = 0


def build_ineqs_system(pairs: list[tuple[str, str]], unit_pair: tuple[str, str]):
    global counter
    counter+=1
    name1 = f's{counter}'
    counter+=1
    name2 = f's{counter}'

    sys1 = [f'(> {f1} {f2})' for f1, f2 in pairs]
    sys2 = [f'(>= {f1} {f2})' for f1, f2 in pairs]

    sys1.append(f'(>= {unit_pair[0]} {unit_pair[1]})')
    sys2.append(f'(> {unit_pair[0]} {unit_pair[1]})')

    otst = '\n' + ' '*8
    otst2 = '\n' + ' '*12
    system1 = f'(assert (= {name1} ' + otst + '(and ' + otst2 + otst2.join(sys1)+ ')' + '))'
    system2 = f'(assert (= {name2} ' + otst + '(and ' + otst2 + otst2.join(sys2)+ ')' + '))'
    system_total = f'(or {name1} {name2})'

    decl1 = f'(declare-const {name1} Bool)'
    decl2 = f'(declare-const {name2} Bool)'

    # system1 = f'(assert ( = {name1} ' + '( and ' + ' '.join(sys1)+ ')' + '))'
    # system1 = f'(assert ( = {name2} ' + '( and ' + ' '.join(sys2)+ ')' + '))'
    return [decl1, decl2], [system1, system2], [system_total] 

def to_smt2(trs: list[tuple[Constructor, Constructor]], file:str, arity:dict[str,str]):
    sys_decls = []
    sys_defs = []
    sys_usages = []

    for trl, trr in trs:
        sys_decl, sys_def, sys_usg = build_ineqs_system(*build_ineqs_list(trl, trr))
        sys_decls += sys_decl
        sys_defs += sys_def
        sys_usages += sys_usg

    total_string = f'(assert (and {" ".join(sys_usages)}))'

    declarations, monotonics = collect_nonunit_coefs(arity)

    with open(file, 'w') as f:
        f.writelines('\n'.join([ 
            '(set-logic QF_NIA)',
            '',

            '; КОЭФФИЦИЕНТЫ',
            *declarations,
            *monotonics,
            '',

            '; СИСТЕМЫ',
            *sys_decls,
            '',

            '; ОПРЕДЕЛЕНИЕ СИСТЕМ',
            *sys_defs,
            '',

            total_string,
            '',

            '(check-sat)'
        ]))
        


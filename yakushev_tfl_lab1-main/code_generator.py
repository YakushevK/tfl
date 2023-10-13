from models import Constructor


def generate_variables_code(variables):
    s = 'from models import Constructor\n\n\n'
    
    for v in variables:
        d = {v:[["1"]]}
        s += f'{v} = Constructor({d})\n'

    with open('temp_variables.py', 'w') as f:
        f.write(s)

def generate_constructors_code(constructors):
    s = 'from models import Constructor\n\n\narity=dict()'

    for c in constructors:
        func_code = '' + \
'''
def {fname}(*args):
    # проверяем количество аргументов
    if '{fname}' not in arity:
        arity['{fname}'] = len(args)
    assert len(args) == arity['{fname}']
    # print('{fname}:', args)
    if len(args) == 0:
        return Constructor(dict([('1', [['1']])])) * ('{fname}'+'1')

    res = args[0] * ('{fname}'+'1')
    for i, arg in enumerate(args[1:]):
        res = res + arg * ('{fname}'+str(i+2))
    res = res + Constructor(
        dict([
            ('1', [['1']])
        ]
    )) * ('{fname}'+str(len(args)+1))
    return res
        

'''.format(fname = c)
        s += func_code

    with open('temp_funcs.py', 'w') as f:
        f.write(s)
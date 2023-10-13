from __future__ import annotations
from copy import deepcopy


class Constructor:
    d: dict[str, list[list[str]]]
    
    def __init__(self, d):
        self.d = d

    def __add__(self, o: Constructor):
        assert type(o) == type(self)
        d = deepcopy(self.d)

        for k, val in o.d.items():
            if k in d:
                d[k] = d[k] + val
            else:
                d[k] = val
        
        return Constructor(d)

    def __mul__(self, p: str):
        d = deepcopy(self.d)
        for k in d:
            d[k] = [l + [p] for l in self.d[k]]
        return Constructor(d)

    def __rmul__(self, p: str):
        return self.__mul__(p)
    
    def __repr__(self):
        each_var = []
        for k, ps in self.d.items():
            prods = [''.join(filter(lambda x: x!='1', prod)) for prod in ps]
            prods_sum = '+'.join(prods)
            total = '(' +prods_sum + ')' + k 
            each_var.append(total)
        return '{' + ' + '.join(each_var) + '}'
        # return '(+ (* ' + ' '.join([f'{"(+ " + " ".join(["(* " + " ".join(v) + ")" for v in vs]) + ")"} {k})' for k, vs in self.d.items()]) + ')'
    
    def __str__(self):
        return repr(self)


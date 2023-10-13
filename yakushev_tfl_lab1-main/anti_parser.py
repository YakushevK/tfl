import re


def _parse(s, variables):
    n = len(s)
    i = 0
    while i < n:
        x = s[i]
        if x.isalpha() and \
            x not in variables and \
            (i == len(s)-1 or s[i+1]!='('):
            s = s[:i+1]+'()'+s[i+2:]
            n+=2
        i+=1

    elems = ['']
    i = 0
    for x in s:
        if x.isspace():
            continue
        match x:
            case '(':
                i+=1
            case ')':
                i -=1
            case _:
                pass
        elems[-1] += x
        if i == 0:
            elems.append('')
    # получили список подстрок "верхнего уровня"
    elems = elems[:-1]

    groups = []
    cur = []
    for i, x in enumerate(elems):
        if x == '=':
            cur += ','
        elif x.startswith('('):
            cur.append(x)
        elif x.isalpha() and x in variables:
            assert ord('a') <= ord(x) <= ord('z')
            cur.append(x)
            cur.append('')
        elif x.isalpha():
            assert ord('a') <= ord(x) <= ord('z')
            cur.append(x)

        if len(cur) == 5:
            groups.append('(' + ''.join(cur) + ')')
            cur = []     

    assert cur == []   
    print(groups)
    return groups


def parse(file):
    raw = open(file).read()
    raw = re.sub(r'\s', '', raw)
    r1 = r'^variables=([a-z](?:\,[a-z])*)(.*=.*)+$'
    match = re.match(r1, raw, flags = re.X|re.A)
    variables = set(match.groups()[0].split(','))
    rss = _parse(match.groups()[1], variables)
    constrs = set(filter(str.isalpha, ''.join(rss))).difference(variables)

    return variables, constrs, rss



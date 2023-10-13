import sys
import os
from anti_parser import parse
from code_generator import generate_variables_code, generate_constructors_code
from to_smt2 import to_smt2

def main():
    # вычисляем 
    try:
        trs = [eval(rs) for rs in rss]
    except NameError as e:
        print('evaluation failed')
        print('вероятно, используется необъявленная переменная')
        print(e)
        os._exit(1)
    except Exception as e:
        print('evaluation failed')
        print(e)
        os._exit(1)
    else:
        # печатаем в файл
        to_smt2(trs, sys.argv[2], arity)


if __name__ == '__main__':
    # парсим 
    variables, constrs, rss = parse(sys.argv[1])
    # print('variables:', variables)
    # print('constructors:', constrs)
    # print('trs:', rss)

    # генерируем код
    generate_variables_code(variables)
    generate_constructors_code(constrs)

    # импортируем нагенерированное
    from temp_funcs import *
    from temp_variables import *

    # перегоняем в smt2
    main()


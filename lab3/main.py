from cmath import sin


def rectangle_method(f, a, b, e, min_n = 4, max_itr = 10):
    """Метод прямоугольников"""
    data = {}

    type = input('\nТип метода: \n1)Левые \n2)Правые \n3)Средние \nВаш выбор: ')
    while (type != '1') and (type != '2') and (type != '3'):
        print("Нужно ввести либо 1, либо 2, либо 3!")
        type = input('\nТип метода: \n1)Левые \n2)Правые \n3)Средние \nВаш выбор: ')
    n = min_n
    result = float('inf')
    maxN = 1000000
    while n <= n * (2 ** max_itr) and n <=maxN:
        try:
            last_result = result
            result = 0
            x = a

            h = (b - a) / n
            for i in range(n):
                if type == '1':
                    result += f(x)
                elif type == '2':
                    result += f(x+h)
                elif type == '3':
                    result += f(x + h / 2)
                x += h
            result *= h

            if (1/3) * abs(last_result - result) < e:
                break
            else:
                n *= 2

        except ZeroDivisionError:
            print('\Интеграл либо не существует, либо является бесконечностью')
            break
    if (n >= maxN):
        print('Введенная точность не достигнута меньше чем максисальной итерации')
    data['result'] =result
    data['n'] = n

    return data

def trapezoid_method(f,a,b,e,min_n = 4, max_itr = 10):
    """Метод трапеции"""
    data = {}
    n = min_n
    maxN = 10000000

    result = float('inf')
    while (n <= n * (2 ** max_itr)) and n <= maxN:
        last_result = result
        result = (f(a) + f(b)) / 2

        h = (b-a) / n
        x = a + h

        for i in range(n - 1):
            result += f(x)
            x += h
        result *= h

        if (1/3) * abs(last_result - result) < e:
            break
        else:
            n *= 2
    if n >= maxN:
        print('Введенная точность не достигнута меньше чем максисальной итерации')
    data['result'] = result
    data['n'] = n

    return data
    

def getfunc(func_id):
    """Получить выбранную функцию"""
    if func_id == '1':
        return lambda x: x**2
    elif func_id == '2':
        return lambda x: x**3
    elif func_id == '3':
        return lambda x: sin(x)
    elif func_id == '4':
        return lambda x: -2 * x**3 - 5 * x**2 + 7 * x - 14

def getmethod(method_id):
    """Получить выбранный метод"""
    if method_id == '1':
        return 'rectangle_method'
    elif method_id == '2':
        return 'trapezoid_method'
    else: 
        return None


def getdata_input():
    """Получить данные с клавиатуры"""
    data = {}

    print('\nВыберите функцию.')
    print('1) x²')
    print('2) x³')
    print('3) sin(x)')
    print('4) -2x³ - 5x² + 7x - 13')
    
    while True:
        try: 
            func_id = input('Функция: ')
            func = getfunc(func_id)
            if func is None:
                raise AttributeError
            break
        except AttributeError:
            print('Функции нет в списке.')
    data['func'] = func

    print('\nВыберите метод решения.')
    print('1) Метод прямоугольников')
    print('2) Метод трапеции')
    while True:
        try:
            method_id = input('Метод решения: ')
            method = getmethod(method_id)
            if method is None:
                raise AttributeError
            break
        except AttributeError:
            print('Метода нет в списке.')
    data['method'] = method

    print('\nВведите пределы интегрирования.')
    while True:
        try:
            a,b = map(float, input('Пределы интегрирования: ').split())
            if a > b :
                a, b = b, a
            break
        except ValueError:
            print('Пределы интегрирования должны быть числами, введенными через пробел.')
    data['a'] = a
    data['b'] = b
    
    print('\nВведите погрешность вычисления.')
    while True:
        try:
            error = float(input('Погрешность вычисления: '))
            if error <= 0:
                raise ArithmeticError
            break
        except (ValueError, ArithmeticError):
            print('Погрешность вычисления должна быть положительным числом.')
    data['error'] = error

    return data
        

def main():
    print('\n\n\tЛабораторная работа №3 (13)')
    print("\t Численное интегрирование")
    data = getdata_input()

    if data['method'] == 'rectangle_method':
        answer = rectangle_method(data['func'],data['a'], data['b'], data['error'])
    elif data['method'] == 'trapezoid_method':
        answer = trapezoid_method(data['func'],data['a'], data['b'], data['error'])
    else:
        answer = None

    print('\n\nРезультаты вычисления.')
    print(f"Значение интеграла: {answer['result']}")
    print(f"Количество разбиении: {answer['n']}")

    input('Нажмите Enter, чтобы выйти')

main()
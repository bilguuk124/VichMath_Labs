import numpy as np
import matplotlib.pyplot as plt
from NonLinearSystems import CalculatorSystems

TEST1 = "iofiles/test1.txt"
TEST2 = "iofiles/test2.txt"
TEST3 = 'iofiles/test3.txt'

def d(n,x,f,h=0.00000001):
    """ Найти значение произодной функции """
    if n <= 0:
        return None
    elif n == 1:
        return (f(x+h) - f(x)) / h
    
    return (d(n-1, x+h, f) - d(n-1, x, f)) / h

def halfDivision_method(a,b,f,e):
    '''Метод половинного деления'''
    if f(a) * f(b) > 0:
        print("Уравнение содержит 0 или несколько корней 1")
        return None
    itr = 1
    table = [['№','a','b','x','F(a)','F(b)','F(x)','|a-b|']]
    while True:
        x = (a + b) / 2
        table.append([itr,a,b,x,f(a),f(b),f(x),abs(a-b)])
        if f(a) * f(x) > 0:
            a = x
        else:
            b = x
        itr += 1
        if abs(a-b) <= e or abs(f(x)) < e:
            break
    x = (a+b) / 2
    table.append([itr,a,b,x,f(a),f(b),f(x),abs(a-b)])
    return x, f(x), itr , table

def iteration_method(x0, f, e, maxitr=100):
    """ Метод простой итерации """
    log = [['x0', 'f(x0)', 'x', 'g(x0)', '|x - x0|']]

    def g(g_x):
        return g_x + (-1 / d(1, g_x, f)) * f(g_x)

    x = g(x0)
    log.append([x0, f(x0), x, g(x0), abs(x - x0)])

    itr = 0
    while abs(x - x0) > e and itr < maxitr:
        if d(1, x, g) >= 1:
            return None
        x0, x = x, g(x)
        log.append([x0, f(x0), x, g(x0), abs(x - x0)])
        itr += 1

    return x, f(x), itr, log

def plot(x,y):
    """ Отрисовать график по заданным x и y """
    #Настраиваем всплывающее окно
    plt.rcParams['toolbar'] = 'None'
    plt.gcf().canvas.manager.set_window_title("График функции")
    #Настраиваем оси
    ax = plt.gca()
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.plot(1, 0, marker=">", ms=5, color='k', transform = ax.get_yaxis_transform(),clip_on = False)
    ax.plot(0, 1, marker="^", ms = 5, color='k', transform = ax.get_xaxis_transform(),clip_on = False)

    #Отрисовываем график
    plt.plot(x,y)
    plt.show(block=False)

def getfunc(function_num):
    """ Получить выбранную функцию """
    if function_num == '1':
        return np.linspace(-1, 3, 200), \
            lambda x: x ** 3 - 4.5 * (x ** 2) - 9.21 * x - 0.383
    elif function_num == '2':
        return np.linspace(-3,2,200), \
            lambda x: x ** 3 -2 * x ** 2 + 4 
    elif function_num == '3':
        return np.linspace(-20, 20, 200), \
            lambda x: np.sin(x) + 0.1
    elif function_num == '4':
        return np.meshgrid(np.linspace(-5,5,200), np.linspace(-5,5,200)), \
            lambda x,y : x**2 + y**2 - 4
    elif function_num == '5':
        return np.meshgrid(np.linspace(-5,5,200),np.linspace(-5,5,200)), \
            lambda x,y: y - 3 * (x**2)
    else:
        return None

def getdata_file():
    """ Получить данные из файла """
    file_choice = input('\nВыберите тестовый файл: \n1)Тест метода половинного деления \n2)Тест метода простой итерации \n3)Тест метода Ньютона на систему нелинейных уравнений \nВаш выбор: ')
    while True:
        if file_choice == '1':
            file_choice = TEST1
            break
        elif file_choice == '2':
            file_choice = TEST2
            break
        elif file_choice == '3':
            file_choice = TEST3
            break
        else:
            print('Нужно ввести 1 или 2 или 3 !')


    with open(file_choice, 'rt') as fin:
        try:
            data = {}
            function = None
            method = fin.readline().strip()
            if(method != '1') and (method != '2') and (method != '3'):
                raise ValueError
            if (method == '1') or (method=='2'):
                function_data = getfunc(fin.readline().strip())
                if function_data is None:
                    raise ValueError
                x, function = function_data
                plot(x, function(x))
                data['function'] = function
            data['method'] = method
            
            if method == '1':
                a,b = map(float, fin.readline().strip().split())
                if a > b:
                    a,b = b,a
                elif a == b:
                    raise ArithmeticError
                elif (function(a) * function(b) > 0):
                    raise ArithmeticError
                data['a'] = a
                data['b'] = b
            elif method == '2':
                x0 = float(fin.readline().strip())
                data['x0'] = x0
            elif method == '3':
                x0, y0 = map(float, fin.readline().strip().split())
                arr1, functionF = getfunc('4')
                arr2, functionG = getfunc('5')     
                data['x0'] = x0
                data['y0'] = y0
                data['functionF'] = functionF
                data['functionG'] = functionG

            error = float(fin.readline().strip())
            if error < 0:
                raise ArithmeticError
            data['error'] = error
            return data

        except (ValueError, AttributeError, ArithmeticError):
            plt.close()
            return None
        

def getdata_input():
    """ Получить данные с клавиатуры """
    data = {}
    

    print("\nВыберите метод решения.")
    print("1) Метод половинного деления")
    print("2) Метод простой итерации")
    print("3) Метод Ньютона")
    method = input("Метод решения: ")
    while (method != '1') and (method != '2') and (method != '3'):
        print("Выберите метод решения из списка.")
        method = input("Метод решения: ")
    data['method'] = method
    
    if(data['method'] == '1' or data['method'] == '2'):
        print("\nВыберите функцию.")
        print("1) x³ - 4.5x² - 9.21x + 0.383")
        print("2) x³ - x + 4")
        print("3) sin(x) + 0.1")
        function_data = getfunc(input("Функция: "))
        while function_data is None:
            print("Выберите функцию из списка.")
            function_data = getfunc(input("Функция: "))
        x, function = function_data
        plot(x, function(x))
        data['function'] = function

    if method == '1':
        print("\nВыберите границы интервала.")
        while True:
            try:
                a,b = map(float, input("Границы интервала: ").split())
                if a > b:
                    a,b = b,a
                elif a==b:
                    raise ArithmeticError
                elif function(a) * function(b) > 0:
                    raise AttributeError
                break
            except ValueError:
                print("Границы интервала должны быть числами, введенными через пробел.")
            except ArithmeticError:
                print("Границы интервала не могут быть равны.")
            except AttributeError:
                print("Интервал содержит ноль или несколько корней.")
        data['a'] = a
        data['b'] = b
    elif method == '2':
        print("\nВыберите начальное приближение.")
        while True:
            try:
                x0 = float(input("Начальное приближение: "))
                break
            except ValueError:
                print("Начальное приближение должно быть числом")
        data['x0'] = x0

    elif method == '3':
        print("\nВ данной задаче будет рассмотрена система уравнений:")
        print("x² + y² = 4")
        print("y = 3x²")
        print('\nВыберите начальное приближение.')
        while True:
            try:
                x0 = float(input("Начальное приближение x0: "))
                y0 = float(input('Начальное приближение y0: '))
                arr1, functionF = getfunc('4')
                arr2, functionG = getfunc('5')
                break
            except ValueError:
                print('Начальное приближение должны быть числами!')
        data['x0'] = x0
        data['y0'] = y0
        data['functionF'] = functionF
        data['functionG'] = functionG
    
    
    print("\nВыберите погрешность вычисления.")
    while True:
        try:
            error = float(input("Погрешность вычисления: "))
            if error <=0:
                raise ArithmeticError
            break
        except (ValueError, ArithmeticError):
            print("Погрешность вычисления должна быть положительным числом.")
    data['error'] = error

    return data

def main():
    print("\nЛабораторная работа №2 (13)")
    print("Численное решение нелинейных уравнений")

    print("Взять исходные данные из файла(+) или ввести с клавиатуры(-)?")
    inchoice = input("Режим ввода: ")
    while(inchoice != ('+') and inchoice != ('-')):
        print("Введите '+' или '-' для выбора способа ввода.")
        inchoice = input("Режим ввода: ")
    
    if inchoice == '+':
        data = getdata_file()
        if data is None:
            print('\nПри считывании данных из файла произошла ошибка')
            print('Режим ввода переключен на ручной')
            data = getdata_input()
    else:
        data = getdata_input()
    try:
        answer = None
        if data['method'] == '1':
            answer = halfDivision_method(data['a'],data['b'],data['function'],data['error'])
            if answer is None:
                print("Не выполняется условие сходимости.")
                raise ValueError
        elif data['method'] == '2':
            answer = iteration_method(data['x0'], data['function'], data['error'])
            if answer is None:
                print('Не выполняется условие сходимости.')
                raise ValueError
        elif data['method'] == '3':
            calculator = CalculatorSystems(data['x0'], data['y0'], data['error'], data['functionF'], data['functionG'])
            answer = calculator.calculate()
            del calculator
        if data['method'] == '1' or data['method'] == '2':
            print(f"\nКорень уравнения: {answer[0]}")
            print(f"Значение функции в корне: {answer[1]}")
            print(f"Число итерации: {answer[2]}")

            print("\nВывести таблицу трассировки? (+/-)")
            logchoice = input("Таблица трассировки: ")
            while (inchoice != '+') and (inchoice != '-'):
                print("Введите '+' или '-' для выбора, выводить ли таблицу трассировки.")
                logchoice = input("Таблица трассировки: ")
            if logchoice == '+':
                for j in range(len(answer[3][0])):
                    print('%12s' % answer[3][0][j], end = '')
                print()
                for i in range(1, len(answer[3])):
                    for j in range(len(answer[3][i])):
                        print('%12.3f' % answer[3][i][j], end='')
                    print()
        elif data['method'] == '3':
            print("\n\nОтвет:\nКорни: x =", answer[0], ', y =',answer[1])
            print('Количество итерации:', answer[2])
            print("Погрешность:" , answer[3] , "\n")
            print("F(x,y) = ",answer[4])
            print("G(x,y) = ",answer[5])
    except ValueError:
        pass

    input("\n\nНажмите Enter, чтобы выйти.")

main()
# Лабораторная работа #6 (13)
# @ Пурэвсурэн Билгуун P3213

import numpy as np
import matplotlib.pyplot as plt
from math import exp

def get_error(f,a,b,y0,h,p):
    n = int((b-a) / h)
    error = [0]
    y = 0

    if p == 2:
        y2 = euler_method(f,a,b,y0,h)
        b2 = 1
        j = 0
        while True:
            y = euler_method(f,a,b2,y0,2*h)
            if len(y) >= 2 * len(y2):
                break
            b2+=1

        for i in range(1,len(y2)*2):
            if i % 2 == 0:
                error.append(np.abs((y[i][1] - y2[j][1])/3))
            else:
                j += 1
                
    elif p == 4:
        y2 = milna_method(f,a,b,y0,h)
        b2 = 1
        j = 0

        while True:
            y = milna_method(f,a,b2,y0,2*h)
            if len(y) >= 2 * len(y2):
                break
            b2+=1

        for i in range(1,len(y2)*2):
            if i % 2 == 0:
                error.append(np.abs((y[i][1] - y2[j][1])/15))
            else:
                j += 1

    return error


def euler_method(f,a,b,y0,h):
    """ Усовершенствованный метод Эйлера """
    dots = [(a,y0)]
    n = int((b-a) / h)
    for i in range(1, n+1):
        h2 = h / 2
        y = dots[i-1][1] + h * f(dots[i-1][0] + h2, dots[i-1][1] + h2 * f(dots[i-1][0],dots[i-1][1]))
        dots.append((dots[i-1][0] + h,y))

    return dots
    

def milna_method(f,a,b,y0,h):
    """ Метод Милна """
    n = int((b-a) / h)
    b0 = min(b, a + 3 * h)
    dots = euler_method(f,a, b0, y0, h)
    if len(dots) <= 3:
        return dots
    for i in range(4, n+1):
        y_prognoz = dots[i-4][1] + ((4*h)/3)*(2*f(dots[i-3][0], dots[i-3][1]) - f(dots[i-2][0],dots[i-2][1]) + 2*f(dots[i-1][0],dots[i-1][1]))
        y_correct = dots[i-2][1] + (h/3) * (f(dots[i-2][0],dots[i-2][1]) + 4 * f( dots[i-1][0],dots[i-1][1]) + f(dots[i-1][0]+h, y_prognoz))
        dots.append((dots[i-1][0]+h, y_correct))
    return dots

def plot(x,y,acc_x,acc_y):
    """ Отрисовать графики точного и численного решении """
    # Настраиваем окно
   # plt.gcf().canvas.manager.set_widow_title('График')

    # Настраиваем оси
    ax = plt.gca()
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('None')
    ax.spines['top'].set_color('None')
    ax.plot(1,0, marker = '>', ms = 5, color = 'k',
            transform = ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 1, marker='^', ms = 5, color = 'k',
            transform=ax.get_xaxis_transform(), clip_on = False)
    
    # Отрисовываем график
    plt.plot(x, y, label='y(x)')
    plt.plot(acc_x, acc_y, label='Точный')

    plt.legend()
    plt.show(block=False)

def gettask(task_id):
    """ Получить выбранную функцию """
    if task_id == '1':
        return lambda x, y: y + (1 + x) * (y ** 2), \
               lambda x: -1 / x, \
               1, \
               1.5, \
               -1
    elif task_id == '2':
        return lambda x, y: (x ** 2) - 2 * y, \
               lambda x: 0.75 * exp(-2 * x) + 0.5 * (x ** 2) - 0.5 * x + 0.25, \
               0, \
               1, \
               1
    else:
        return None

def getdata_input():
    """ Получить данные с клавиатуры """
    data = {}

    print("\nВыберите метод дифференцирования.")
    print(" 1 — Усовершенствованный метод Эйлера")
    print(" 2 — Метод Милна")
    while True:
        try:
            method_id = input("Метод дифференцирования: ")
            if method_id != '1' and method_id != '2':
                raise AttributeError
            break
        except AttributeError:
            print("Метода нет в списке!")
    data['method_id'] = method_id

    print('\nВыберите задачу.')
    print(" 1) y' = y + (1 + x)y²\n     на [1; 1.5] при y(1) = -1")
    print(" 2) y' = x² - 2y\n     на [0; 1] при y(0) = 1")
    while True:
        try:
            task_id = input('Задача: ')
            func, acc_func, a, b, y0 = gettask(task_id)
            if func is None:
                raise AttributeError
            break
        except AttributeError:
            print('Функции нет в списке!')
    data['f'] = func
    data['acc_f'] = acc_func
    data['a'] = a
    data['b'] = b
    data['y0'] = y0

    print('\nВведите шаг точек.')
    while True:
        try:
            h = float(input('Шаг точек: '))
            if h <= 0:
                raise AttributeError
            break
        except (ValueError, AttributeError):
            print('Шаг точек должен быть положительным числом.')
    data['h'] = h

    return data


def main():
    print('\tЛабораторная работа #6 (13)')
    print('\tЧисленное дифференцирования')

    data = getdata_input()
    p = 0
    if data['method_id'] == '1':
        data['p'] = 2
        answer = euler_method(data['f'],data['a'], data['b'], data['y0'], data['h'])
        error = get_error(data['f'],data['a'], data['b'], data['y0'], data['h'],data['p'])
    elif data['method_id'] == '2':
        data['p'] = 4
        answer = milna_method(data['f'],data['a'], data['b'], data['y0'], data['h'])
        error = get_error(data['f'],data['a'], data['b'], data['y0'], data['h'],data['p'])
    else:
        answer = None
        error = None

    if answer is None or error is None:
        print('\n\nВо время вычисления произошла ошибка!')

    else:
        x = np.array([dot[0] for dot in answer])
        y = np.array([dot[1] for dot in answer])
        acc_x = np.linspace(np.min(x), np.max(x), 100)
        acc_y = [data['acc_f'](i) for i in acc_x]
        plot(x, y, acc_x, acc_y)

        print("\n\nРезультаты вычисления.")
        print("%12s%12s%12s%12s%12s%12s" % ("n","x", "y", "Точный","e","Рунге"))
        for i in range(len(answer)):
            print("%12i%12.3f%12.4f%12.4f%12.4f%12.4f" % (i,answer[i][0], answer[i][1], data['acc_f'](answer[i][0]), np.abs(data['acc_f'](answer[i][0])-answer[i][1]),error[i]))

    input("\n\nНажмите Enter, чтобы выйти.")
main() 
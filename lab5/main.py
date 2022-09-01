# Лабораторная работа #5 (13)
# @ Пурэвсурэн Билгуун, PЗ213

import numpy as np
import matplotlib.pyplot as plt
from math import sin, sqrt, factorial


def lagrange_polynomial(dots, x):
    """ Многочлен Лагранжа """
    result = 0

    n = len(dots)
    for i in range(n):
        c1 = c2 = 1
        for j in range(n):
            if i != j:
                c1 *= x - dots[j][0]
                c2 *= dots[i][0] - dots[j][0]
        result += dots[i][1] * c1 / c2

    return result


def t_calc(t, n, forward=True):
    """ Вычислить параметр 't' """
    result = t
    j = 1
    if forward:
        for i in range(1,n):
            if i % 2 != 0:
                result *= t - j
            else:
                result *= t + j
                j += 1
    else:
        for i in range(1, n):
            if i % 2 != 0:
                result *= t + j
            else:
                result *= t - j
                j+=1

    return result

def bessel_t(t,n):
    if (n == 0):
        return 1
    result = t
    for i in range(1, int(n/2+1)):
        result *= (t-i)
    for i in range(1, int(n/2)):
        result *= (t+i)
    return result


def gauss_polynomial(dots, x):
    """ Интерполяционные формулы Гаусса"""
    n = len(dots)
    h = dots[1][0] - dots[0][0]
    a = [[0] * n for _ in range(n)]
    for i in range(n):
        a[i][0] = dots[i][1]

    for i in range(1, n):
        for j in range(n - i):
            a[j][i] = a[j + 1][i - 1] - a[j][i - 1]

    if x <= dots[n // 2][0]:
        # Первая интерполяционная формула Гаусса
        x0 = n // 2

        t = (x - dots[x0][0]) / h
        result = a[x0][0]
        temp = x0
        for i in range(1, n):
            if i % 2 == 0:
                temp -= 1
            result += (t_calc(t, i) * a[temp][i]) / factorial(i)
    else:
        # Вторая интерполяционная формула Гасса
        x0 = n // 2

        t = (x - dots[x0][0]) / h

        temp = x0
        result = a[x0][0]
        for i in range(1, n):
            if i % 2 != 0 :
                temp -= 1
            result += (t_calc(t, i, False) * a[temp][i]) / factorial(i)

    return result

def stirling_polynomial(dots,x):
    """ Интерполяционная формула Стирлинга"""
    n = len(dots)
    h = dots[1][0] - dots[0][0]
    a = [[0] * n for _ in range(n)]
    for i in range(n):
        a[i][0] = dots[i][1]

    for i in range(1, n):
        for j in range(n - i):
            a[j][i] = a[j + 1][i - 1] - a[j][i - 1]
    # Первая интерполяционная формула Гаусса
    x0 = n // 2

    t1 = (x - dots[x0][0]) / h
    result1 = a[x0][0]
    temp1 = x0
    for i in range(1, n):
        if i % 2 == 0:
            temp1 -= 1
        result1 += (t_calc(t1, i) * a[temp1][i]) / factorial(i)
    # Вторая интерполяционная формула Гасса
    x0 = n // 2

    t2 = (x - dots[x0][0]) / h

    temp2 = x0
    result2 = a[x0][0]
    for i in range(1, n):
        if i % 2 != 0 :
            temp2 -= 1
        result2 += (t_calc(t2, i, False) * a[temp2][i]) / factorial(i)
    
    # И среднеарифметическое значение
    result = (result1 +result2)/2
    return result

def bessel_polynomial(dots,x):
    """ Интерполяционная формула Беселя"""
    n = len(dots)
    h = dots[1][0] - dots[0][0]
    a = [[0] * n for _ in range(n)]
    for i in range(n):
        a[i][0] = dots[i][1]

    for i in range(1, n):
        for j in range(n - i):
            a[j][i] = a[j + 1][i - 1] - a[j][i - 1]
    x0 = 0
    if ((n%2) > 0):
        x0 = int(n/2)
    else:
        x0 = int(n/2-1)

    t = (x - dots[x0][0])/h
    result = (a[x0][0] + a[x0+1][0])/2

    for i in range(1,n):
        if i % 2:
            result += ((t-0.5) * bessel_t(t,i-1) * a[x0][i])/factorial(i)
        else:
            result += (bessel_t(t,i) * (a[x0][i]+a[x0-1][i])/(factorial(i)*2))
            x0 -= 1
    return result
    



def plot(x, y, plot_x, plot_y):
    """ Отрисовать график по заданным координатам узлов и точкам многочлена """
    # Настраиваем всплывающее окно
    # plt.rcParams['toolbar'] = 'None'
    plt.gcf().canvas.manager.set_window_title("График")
    # Настриваем оси
    ax = plt.gca()
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.plot(1, 0, marker=">", ms=5, color='k',
            transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 1, marker="^", ms=5, color='k',
            transform=ax.get_xaxis_transform(), clip_on=False)

    # Отрисовываем график
    plt.plot(x, y, 'o', plot_x, plot_y)
    plt.show(block=False)


def getfunc(func_id):
    """ Получить выбранную функцию """
    if func_id == '1':
        return lambda x: sqrt(x)
    elif func_id == '2':
        return lambda x: x ** 2
    elif func_id == '3':
        return lambda x: sin(x)
    else:
        return None


def make_dots(f, a, b, n):
    dots = []

    h = (b - a) / (n - 1)
    for i in range(n):
        dots.append((a, f(a)))
        a += h

    return dots


def getdata_input():
    """ Получить данные с клавиатуры """
    data = {}

    print("\nВыберите метод интерполяции.")
    print(" 1 — Многочлен Лагранжа")
    print(" 2 — Интерполяционные формулы Гаусса")
    print("------------------------------------------")
    print(" 3 - Интерполяционная формула Стирлинга")
    print(" 4 - Интерполяционная формула Беселя")
    while True:
        try:
            method_id = input("Метод решения: ")
            if method_id != '1' and method_id != '2' and method_id != '3' and method_id != '4':
                raise AttributeError
            break
        except AttributeError:
            print("Метода нет в списке.")
    data['method_id'] = method_id

    print("\nВыберите способ ввода исходных данных.")
    print(" 1 — Набор точек")
    print(" 2 — Функция")
    while True:
        try:
            input_method_id = input("Способ: ")
            if input_method_id != '1' and input_method_id != '2':
                raise AttributeError
            break
        except AttributeError:
            print("Способа нет в списке.")

    dots = []
    if input_method_id == '1':
        print("Вводите координаты через пробел, каждая точка с новой строки.")
        print("Чтобы закончить, введите 'END'.")
        while True:
            try:
                current = input()
                if current == 'END':
                    if len(dots) < 2:
                        raise AttributeError
                    break
                x, y = map(float, current.split())
                dots.append((x, y))
            except ValueError:
                print("Введите точку повторно - координаты должны быть числами!")
            except AttributeError:
                print("Минимальное количество точек - две!")
    elif input_method_id == '2':
        print("\nВыберите функцию.")
        print(" 1 — √x")
        print(" 2 - x²")
        print(" 3 — sin(x)")
        while True:
            try:
                func_id = input("Функция: ")
                func = getfunc(func_id)
                if func is None:
                    raise AttributeError
                break
            except AttributeError:
                print("Функции нет в списке.")
        print("\nВведите границы отрезка.")
        while True:
            try:
                a, b = map(float, input("Границы отрезка: ").split())
                if a > b:
                    a, b = b, a
                break
            except ValueError:
                print("Границы отрезка должны быть числами, введенными через пробел.")
        print("\nВыберите количество узлов интерполяции.")
        while True:
            try:
                n = int(input("Количество узлов: "))
                if n < 2:
                    raise ValueError
                break
            except ValueError:
                print("Количество узлов должно быть целым числом > 1.")
        dots = make_dots(func, a, b, n)
    data['dots'] = dots

    print("\nВведите значение аргумента для интерполирования.")
    while True:
        try:
            x = float(input("Значение аргумента: "))
            break
        except ValueError:
            print("Значение аргумента должно быть числом.")
    data['x'] = x

    return data


def main():
    print("\tЛабораторная работа #5 (13)")
    print("\t   Интерполяция функций")

    data = getdata_input()
    x = np.array([dot[0] for dot in data['dots']])
    y = np.array([dot[1] for dot in data['dots']])
    plot_x = np.linspace(np.min(x), np.max(x), 100)
    plot_y = None
    if data['method_id'] == '1':
        answer = lagrange_polynomial(data['dots'], data['x'])
        plot_y = [lagrange_polynomial(data['dots'], x) for x in plot_x]
    elif data['method_id'] == '2':
        answer = gauss_polynomial(data['dots'], data['x'])
        plot_y = [lagrange_polynomial(data['dots'], x) for x in plot_x]
    elif data['method_id'] == '3':
        answer = stirling_polynomial(data['dots'],data['x'])
        plot_y = [lagrange_polynomial(data['dots'],x) for x in plot_x]
    elif data['method_id'] == '4':
        answer = bessel_polynomial(data['dots'],data['x'])
        plot_y = [lagrange_polynomial(data['dots'], x) for x in plot_x]
    else:
        answer = None

    if answer is not None:
        plot(x, y, plot_x, plot_y)

    print("\n\nРезультаты вычисления.")
    print(f"Приближенное значение функции: {answer}")

    input("\n\nНажмите Enter, чтобы выйти.")


main()
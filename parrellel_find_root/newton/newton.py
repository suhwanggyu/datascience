import math

th = 0
eq = []
dif = []

def upsilon(new, old) :
    if new == 0 : 
        return abs(new - old)
    return abs((new - old) / new) * 100


def func(point) :
    global eq
    result = 0
    for idx, coefficient in enumerate(eq) :
        result += pow(point, idx) * coefficient
    return result

def differential(equation) :
    result = []
    for idx, coefficient in enumerate(equation) :
        if idx != 0 :
            result.append(idx * coefficient)
    return result

def derivatedfunc(point) :
    global eq
    result = 0
    for idx, coefficient in enumerate(dif) :
        result += pow(point, idx) * coefficient
    return result


def newton(old) :
    global th
    de = derivatedfunc(old)
    if de == 0 :
        return False

    new = old - (func(old)/de)
    count = 0
    flag = True
    while upsilon(new, old) > th :
        tmp = new
        de = derivatedfunc(new)
        if de == 0 :
            print("Wrong initial point")
            flag = False
            break
        new = new - (func(new)/de)
        if count > 1000 and abs(new - tmp) - abs(tmp - old) > 0 :
            print("Wrong initial point")
            flag = False
            break
        old = tmp
        count = count + 1
    if flag == False :
        return False
    return new

def setAndCalculate(seed, threshold, equation, diffEquation) :
    global th
    global eq
    global dif
    th = threshold
    eq = equation
    dif = diffEquation
    return newton(seed)
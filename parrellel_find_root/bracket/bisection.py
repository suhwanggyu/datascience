import math
th = 0
eq = []

def upsilon(new, old) :
    return abs((new - old) / new) * 100

def func(point) :
    global eq
    result = 0
    for idx, coefficient in enumerate(eq) :
        result += pow(point, idx) * coefficient
    return result

def bisection(lower, upper, result) :
    center = (lower+upper)/2
    if func(lower) * func(upper) > 0 :
        return False
    elif func(lower) == 0 :
        result.append(lower)
        return [lower]
    elif func(upper) == 0 :
        result.append(upper)
        return [upper]
    elif upsilon(center, lower) < th :
        result.append(center)
        return [center]
    else : 
        bisection(lower, center, result)
        bisection(center, upper, result)
        return result
            

def setAndCalculate(bracket, threshold, equation) :
    global th
    global eq
    th = threshold
    eq = equation
    result = []
    bisection(bracket[0], bracket[1], result)
    return result
import argparse
import multiprocessing
import time
from bracket import bisection
from newton import newton
from functools import partial

thm = 0.01
resultm = []

if __name__ == "__main__" :
    parser = argparse.ArgumentParser(description="Methmod")
    parser.add_argument("-m", "--methmod", help="Set Methmod for finding root")
    parser.add_argument("-p", "--parallel", help="Parallel version or not")
    parser.add_argument("-e", "--equation", help="Set target polynomial equation")
    args = parser.parse_args()
    eq = list(map(float, args.equation.strip('[]').split(',')))
    
    if args.methmod == "bisection" :
        bracket = []
        processCount = 1
        resultmtmp = []
        t = 0

        for i in range(-5000000,5000000) :
            lower = i*0.001
            upper = i*0.001 + 0.001
            bracket.append((lower, upper))
        if args.parallel == "Y" :
            processCount = multiprocessing.cpu_count()
            pool = multiprocessing.Pool(processes= processCount)
            func = partial(bisection.setAndCalculate, threshold = thm, equation= eq)
            t = time.time()
            resultmtmp = pool.map(func, bracket)
            pool.close()
            pool.join()
        elif args.parallel == "N" :
            t = time.time()
            for elem in bracket :
                resultmtmp.append(bisection.setAndCalculate(elem, thm, eq)) # 단일 코어로 실행 (탐색구간이 작을 경우)
        print(f'Using time : {time.time()-t}')
        
        for elem in resultmtmp :
            if len(elem) != 0 :
                for root in elem :
                    resultm.append(root)
        

    elif args.methmod == "newton" :
        seed=[]
        for i in range(0,50000) :
            seed.append(i*0.1)
            seed.append(-i*0.1)
        processCount = 1
        diff = newton.differential(eq)
        if args.parallel == "Y" :
            processCount = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes= processCount)
        func = partial(newton.setAndCalculate, threshold = thm, equation = eq, diffEquation = diff)
        t = time.time()
        resultm = pool.map(func, seed) # 병렬로 실행
        for elem in seed :
            resultm.append(newton.setAndCalculate(elem, thm, eq, diff))
        print(f'Using time : {time.time()-t}')
        pool.close()
        pool.join()
    
    elif args.methmod == "hybrid" :
        bracket = []
        diff = newton.differential(eq)
        for i in range(-500000,500000) :
            lower = i*0.001
            upper = i*0.001 + 0.001
            bracket.append((lower, upper))
        processCount = 1
        if args.parallel == "Y" :
            processCount = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes= processCount)
        func = partial(bisection.setAndCalculate, threshold = 40, equation= eq)
        t = time.time()
        resultmtmp = pool.map(func, bracket)
        first = time.time()-t
        pool.close()
        pool.join()
        tmpseed = []
        seed = []
        for elem in resultmtmp :
            if len(elem) != 0 :
                for root in elem :
                    seed.append(root)
        for idx, element in enumerate(tmpseed) :
            if element != False:
                seed.append(element)
        t = time.time()
        for elem in seed :
            resultm.append(newton.setAndCalculate(elem, thm, eq, diff))
        second = time.time()-t
        print(f'Using time : {first + second}')

    try :
        resultm.sort()
    except :
        print("Don't sort")
    final = []
    for idx, element in enumerate(resultm) :
        if (type(element) != bool or element != False) and (idx == 0 or abs(resultm[idx-1] - element) > 0.001):
            final.append(element)
    for elem in final :
        print(f'Answer : {elem}')
        
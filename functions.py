import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import binom
import math
import operator as op
from functools import reduce


MINN=500
MAXN=700

def nck(n, k): #Fast C implementation
    r = min(k, n-k)
    numer = reduce(op.mul, range(n, n-k, -1), 1)
    denom = reduce(op.mul, range(1, k+1), 1)
    return numer // denom

def reliability(m,n,rate=0.001):
    def f(t): #Calculates the reliability of an m out of n system after time t
        p=math.exp(-rate*t)
        return 1-binom.cdf(m-1,n,p)
    return f

def log_availability(g,lam=0.001,mu=1.0):
    r=lam/mu
    def f(n): #Calculates the steady-state availability of a g(n) out of n system, returns it in the nines (-log10(1-x)) metric
        bad_sum=0.0
        for i in range(n-g(n)+1,n+1):
            bad_sum+=pow(r,i)*nck(n,i)
        bad_sum=math.log10(bad_sum)
        bad_sum-=math.log10(r+1)*n
        return -bad_sum
    return f

def find_linear():
    candidates=[]
    def make_minus(i):
        def f(n):
            return max(math.floor(n/2)+1,n-i)
        return f
    def make_prop(c):
        def f(n):
            return max(math.floor(n/2)+1,math.ceil(c*n))
        return f
    def make_log():
        def f(n):
            return max(math.floor(n/2)+1,math.ceil(n-math.log(n)))
        return f

    for i in range(1,51):
        #candidates.append([make_minus(i),f"n-{i} out of n"])
        pass
    for c in np.linspace(0.9,1.0,10)[:-1]:
        #candidates.append([make_prop(c),f"{c}*n out of n"])
        pass
    candidates.append([make_log(),f"n-log(n) out of n"])

    def eval(g):
        f=log_availability(g[0])
        v=np.array([f(x) for x in range(MINN,MAXN+1)])
        diff_sum=np.sum(np.abs((v[1:]-v[:-1])))
        return diff_sum
    #most_linear =  reduce(lambda l1, l2: l1 if eval(l1)<=eval(l2) else l2, candidates)
    #return most_linear
    return candidates[-1]

def availability(g,lam=0.001,mu=1.0):
    r=lam/mu
    def f(n):
        good_sum=0.0
        for i in range(0,n-g(n)+1):
            good_sum+=pow(r,i)*nck(n,i)
        good_sum/=pow(r+1,n)
        return good_sum
    return f

if __name__=="__main__":
    goal=log_availability(lambda x:2)(3)
    print(goal)
    def create():
        def f():
            pass
        return f
    for i in range(3,200):
        curr=math.floor(i/2)+1
        v=abs(log_availability(lambda x:math.floor(i/2)+1)(i)-goal)
        for j in range(math.floor(i/2)+1,i):
            x=abs(log_availability(lambda x:j)(i)-goal)
            if(x<v):
                v=x
                curr=j
        print(f"{i-curr} out of {i}")
        
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import binom
import math
import operator as op
from functools import reduce


MINN=2
MAXN=100
STEP=5

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

def availability(g,lam=0.001,mu=1.0):
    r=lam/mu
    def f(n):
        good_sum=0.0
        for i in range(0,n-g(n)+1):
            good_sum+=pow(r,i)*nck(n,i)
        good_sum/=pow(r+1,n)
        return good_sum
    return f

def gen_const_m(x):
    def f(n):
        return x
    return f

def log_availability(g,lam=0.001,mu=1.0):
    r=lam/mu
    def f(n): #Calculates the steady-state availability of a g(n) out of n system, returns it in the nines (-log10(1-x)) metric
        bad_sum=0.0
        for i in range(n-g(n)+1,n+1):
            bad_sum+=pow(r,i)*nck(n,i)
        bad_sum=math.log10(bad_sum)
        bad_sum-=n*math.log10(r+1)
        return -bad_sum
    return f

def find_linear(use_log=False, start_m=2,start_n=3): #Find the f(n) for which availability(f(n),n) is constant for all n
    goal=(log_availability if use_log else availability)(gen_const_m(start_m))(start_n)
    a=[0]*(MAXN+STEP+1)
    for i in range(MINN,MAXN+STEP+1):
        a[i]=math.floor(i/2)+1
        v=abs((log_availability if use_log else availability)(gen_const_m(math.floor(i/2)+1))(i)-goal)
        for j in range(math.floor(i/2)+1,i):
            x=abs((log_availability if use_log else availability)(gen_const_m(j))(i)-goal)
            if(x<v):
                v=x
                a[i]=j
        #print(f"{a[i]} out of {i}")
    def g(n):
        return a[n]
    return g

if __name__=="__main__":
    find_linear()
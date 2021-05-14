import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import binom
import math
import operator as op
from functools import reduce


MINN=3
MAXN=100
STEP=5

def nck(n, k): #Fast C implementation of n choose k
    r = min(k, n-k)
    numer = reduce(op.mul, range(n, n-k, -1), 1)
    denom = reduce(op.mul, range(1, k+1), 1)
    return numer // denom


def gen_const_m(x):
    def f(n):
        return x
    return f

def reliability(m,n,rate=0.001):
    def f(t): #Calculates the reliability of an m out of n system after time t
        p=math.exp(-rate*t)
        return 1-binom.cdf(m-1,n,p)
    return f


def log_availability_iterative(g,lam=0.001,mu=1.0):
    r=lam/mu
    p=r/(1+r)
    def f(n): #Calculates the steady-state availability of a g(n) out of n system, returns it in the nines (-log10(1-x)) metric
        bad_sum=0.0
        for i in range(n-g(n)+1,n+1):
            bad_sum+=nck(n,i)*pow(p,i)*pow(1-p,n-i)
        nines=-math.log10(bad_sum)
        return nines
    return f

def availability_iterative(g,lam=0.001,mu=1.0):
    r=lam/mu
    p=r/(1+r)
    def f(n):
        sum=0.0
        for i in range(0,n-g(n)+1):
            sum+=nck(n,i)*pow(p,i)*pow(1-p,n-i)
        return sum
    return f


def find_linear(use_log=False, start=MINN, finish=MAXN, benchmark_m=2, benchmark_n=3): #Find the f(n) for which availability(f(n),n) is constant for all n
    goal=(log_availability_iterative if use_log else availability_iterative)(gen_const_m(benchmark_m))(benchmark_n)
    a=[0]*(finish+STEP+1)
    for i in range(start,finish+STEP+1):
        a[i]=math.floor(i/2)+1
        v=(log_availability_iterative if use_log else availability_iterative)(gen_const_m(math.floor(i/2)+1))(i)
        for j in range(1,i): #could have range(math.floor(i/2)+1,i) instead, but it gives nices start for small node numbers
            avail=(log_availability_iterative if use_log else availability_iterative)(gen_const_m(j))(i)
            if(avail>goal and avail<v):
                v=avail
                a[i]=j
        print(f"{a[i]} out of {i}")

    def g(n):
        return a[n]
    return g

def create_seq():
    with open("sequence.txt","w") as f:
        for i in range(2,5):
            f.write(str(i-1)+" ")
        for i in range(5,28):
            f.write(str(i-2)+" ")
        for i in range(28,96):
            f.write(str(i-3)+" ")
        for i in range(96,215):
            f.write(str(i-4)+" ")
        for i in range(215,383):
            f.write(str(i-5)+" ")
        for i in range(383,500):
            f.write(str(i-6)+" ")

if __name__=="__main__":
    #find_linear(start=500,finish=500)
    create_seq()


""" UNUSED """

def availability(g,lam=0.001,mu=1.0): #Doesn't work for large n-s, because binom.cdf has limited precision
    r=lam/mu
    p=r/(1+r)
    def f(n):
        return binom.cdf(n-g(n),n,p)
    return f


def log_availability(g,lam=0.001,mu=1.0): #Doesn't work for large n-s, because binom.cdf has limited precision
    r=lam/mu
    p=r/(1+r)
    def f(n): #Calculates the steady-state availability of a g(n) out of n system, returns it in the nines (-log10(1-x)) metric
        suff=1-binom.cdf(n-g(n),n,p)
        return -math.log10(suff)
    return f


import math


def f1(x):
    return 1.1 * x*3 - 1.6 * x*2 + 3 * x - 5

def f1_prime(x):
    return 3 * 1.1 * x**2 - 2 * 1.6 * x + 3

def f1_double_prime(x):
    return 6 * 1.1 * x - 2 * 1.6

def f1_triple_prime(x):
    return 6 * 1.1

def f2(x):
    return 1.6 * math.exp(x) - 4.2 * x + 2.75

def f2_prime(x):
    return 1.6 * math.exp(x) - 4.2

def f2_double_prime(x):
    return 1.6 * math.exp(x)

def f2_triple_prime(x):
    return 1.6 * math.exp(x)


def taylor_series_approximation(f, f_prime, f_double_prime, f_triple_prime, a, x):
   
    term0 = f(a)
    term1 = f_prime(a) * (x - a)
    term2 = f_double_prime(a) * (x - a)**2 / math.factorial(2)
    term3 = f_triple_prime(a) * (x - a)**3 / math.factorial(3)
    
   
    return term0 + term1 + term2 + term3


a1 = 0.5
x1 = 0.6
approximation1 = taylor_series_approximation(f1, f1_prime, f1_double_prime, f1_triple_prime, a1, x1)
print("Aproximacion de f(0.6) para esta funcion:", approximation1)


a2 = 0.4
x2 = 0.45
approximation2 = taylor_series_approximation(f2, f2_prime, f2_double_prime, f2_triple_prime, a2, x2)
print("Aproximacion de f(0.45) para esta funcion:", approximation2)
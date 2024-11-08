def f(x):
    return x**4

def f_prime(x):
    return 4 * x**3

def f_double_prime(x):
    return 12 * x**2

def f_triple_prime(x):
    return 24 * x


def taylor_approximation(x, h):
    term0 = f(x)
    term1 = f_prime(x) * h
    term2 = f_double_prime(x) * (h**2) / 2
    return term0 + term1 + term2

def remainder_term(x, h):
    c = x  
    return f_triple_prime(c) * (h**3) / 6

x = 1
h = 0.125


approximation = taylor_approximation(x, h)
remainder = remainder_term(x, h)

print("Series de aproximacion de series de la funcion f(x + h):", approximation)
print("Error estimado:", remainder)
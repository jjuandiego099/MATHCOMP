import math

def taylor_series_exp_neg_x(x, tol=1e-8):
   
    n = 0
    term = 1  
    sum_approx = term  
    prev_sum = 0
    error = 100  
    
    while error > tol:
        n += 1
        term *= -x / n  
        prev_sum = sum_approx
        sum_approx += term
     
        error = abs((sum_approx - prev_sum) / sum_approx) * 100
    
    return sum_approx, error, n


def reciprocal_taylor_series_exp_neg_x(x, tol=1e-8):
 
    n = 0
    term = 1  
    sum_approx = term  
    prev_sum = 0
    error = 100 
    
    while error > tol:
        n += 1
        term *= x / n  
        prev_sum = sum_approx
        sum_approx += term
        error = abs((sum_approx - prev_sum) / sum_approx) * 100
    
    sum_approx_reciprocal = 1 / sum_approx
    return sum_approx_reciprocal, error, n


x = 0.85

result_taylor, error_taylor, iterations_taylor = taylor_series_exp_neg_x(x)
print("Using Taylor Series for e^(-x):")
print(f"Result: {result_taylor:.8f}")
print(f"Relative Approximate Error: {error_taylor:.8f}%")
print(f"Iterations: {iterations_taylor}\n")

result_reciprocal, error_reciprocal, iterations_reciprocal = reciprocal_taylor_series_exp_neg_x(x)
print("Using Reciprocal of Taylor Series for e^(x):")
print(f"Result: {result_reciprocal:.8f}")
print(f"Relative Approximate Error: {error_reciprocal:.8f}%")
print(f"Iterations: {iterations_reciprocal}")
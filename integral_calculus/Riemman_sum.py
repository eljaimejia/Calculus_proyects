import sympy as sp
class RiemannSum:
    def __init__(self, f, a, b, n, method='left'):
        self.f = f
        self.a = a
        self.b = b
        self.n = n
        self.method = method   

    def calculate(self):  
        x = sp.symbols('x')
        delta_x = (self.b - self.a) / self.n
        total_sum = 0

        for i in range(self.n):
            if self.method == 'left':
                x_i = self.a + i * delta_x
            elif self.method == 'right':
                x_i = self.a + (i + 1) * delta_x
            elif self.method == 'midpoint':
                x_i = self.a + (i + 0.5) * delta_x
            else:
                raise ValueError("Method must be 'left', 'right', or 'midpoint'.")

            total_sum += self.f.subs(x, x_i) * delta_x

        return total_sum

input_function = input("Enter the function f(x): ")
f = sp.sympify(input_function)
a = float(input("Enter the lower limit a: "))
b = float(input("Enter the upper limit b: "))
n = int(input("Enter the number of subintervals n: "))
method = input("Enter the method (left, right, midpoint): ") 

riemann_sum = RiemannSum(f, a, b, n, method)
result = riemann_sum.calculate()
print(f"The Riemann sum is: {result}")

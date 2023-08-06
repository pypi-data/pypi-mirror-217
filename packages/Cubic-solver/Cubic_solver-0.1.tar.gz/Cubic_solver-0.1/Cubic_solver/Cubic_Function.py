import math
import numpy as np
import matplotlib.pyplot as plt

class Cubic_Function:
    """ 
    cubic equation class for calculating the roots of the cubic equation
    
    Attributes:
    a ,b ,c and d are the coefficents of the cubic function
    """
    def __init__(self,a,b,c,d):
        self.a=a
        self.b=b
        self.c=c
        self.d=d
    
    def get_p_and_q(self):
        """
        Calculates the values of p and q as defined in Cardano's formula for solving cubic equations.

        Returns:
        p (float): The value of p.
        q (float): The value of q.
        """
        p = (3*self.a*self.c - self.b**2) / (3*self.a**2)
        q = (2*self.b**3 - 9*self.a*self.b*self.c + 27*self.a**2*self.d) / (27*self.a**3) 
        return p , q
    
    def find_roots(self):
        """
        Finds the roots of the cubic equation ax^3 + bx^2 + cx + d = 0 using Cardano's formula.

        Returns:
        tuple: A tuple of three complex numbers representing the roots of the equation.
        """
        p,q = self.get_p_and_q()
        delta = ((q/2)**2) + ((p/3)**3)
        if(delta > 0):
            u = (-q / 2 + cmath.sqrt(delta)) ** (1 / 3)
            v = (-q / 2 - cmath.sqrt(delta)) ** (1 / 3)
            x1 = u + v - self.b / (3 * self.a)
            x2 = -(u + v) / 2 - self.b / (3 * self.a) + cmath.sqrt(3) / 2 * (u - v) * 1j
            x3 = -(u + v) / 2 - self.b / (3 * self.a) - cmath.sqrt(3) / 2 * (u - v) * 1j
            return x1, x2, x3
        elif(delta == 0):
            u = v = (-q / 2) ** (1 / 3)
            x1 = 2 * u - self.b / (3 * self.a)
            x2 = x3 = -u - self.b / (3 * self.a)
            return x1, x2, x3
        elif(delta < 0):
            t = math.acos(-q / 2 / math.sqrt(-p ** 3 / 27)) / 3
            u = 2 * math.sqrt(-p / 3) * math.cos(t)
            v = 2 * math.sqrt(-p / 3) * math.cos(t + 2 * math.pi / 3)
            w = 2 * math.sqrt(-p / 3) * math.cos(t + 4 * math.pi / 3)
            x1 = u - self.b / (3 * self.a)
            x2 = v - self.b / (3 *self. a)
            x3 = w - self.b / (3 * self.a)
            return x1, x2, x3
        
    def plot_cubic(self):
        """
        Plots the graph of the cubic equation ax^3 + bx^2 + cx + d using the matplotlib.pyplot library.

        Returns:
        None.
        """
            
        x = np.linspace(-10,10,num=100)
        fx = []
            
        for i in range(len(x)):
            fx.append((self.a)*(i**3) + (self.b)*(i**2) + (self.c * i) + (self.d))
                
        plt.plot(x,fx)
        plt.show()
            
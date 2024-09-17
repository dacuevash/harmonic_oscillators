import sympy as sy
import numpy as np # type: ignore
import matplotlib # type: ignore
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt # type: ignore
from sympy.utilities.lambdify import lambdify
from sympy.printing.latex import latex
from matplotlib.figure import Figure
import io
from PIL import Image, ImageTk # type: ignore

# Declare symbolic function variables
t = sy.symbols('t')
x = sy.Function('x')(t)

# UnDamped Harmonic Oscillator 
class UDHO:
    """
    This class models an Undamped Harmonic Oscillator, meaning that there's no viscous damping coefficient. 
    So the equation model is: mx'' + kx = f(t)
    """
    def __init__(self, mass, stiffness, x_0, v_0, right_hand_side) -> None:
        self.mass = sy.Rational(mass).limit_denominator()
        self.stiffness = sy.Rational(stiffness).limit_denominator()
        self.x_0 = x_0
        self.v_0 = v_0
        self.right_hand_side = sy.sympify(right_hand_side)
        self.natural_frequency = np.sqrt(stiffness/mass)
        self.equation = sy.Eq(self.mass * x.diff(t, 2) + self.stiffness * x, self.right_hand_side)
        self.initial_conditions = {x.subs(t, 0): self.x_0, x.diff(t).subs(t, 0): self.v_0}
        self.solution = sy.dsolve(self.equation, x, ics=self.initial_conditions)
        
    def _convert_rational_to_decimal(self, expression, precision=4):
        return expression.evalf(precision)
    
    def get_solution(self):
        rounded_rhs = self._convert_rational_to_decimal(self.solution.rhs)
        rounded_solution = self.solution.__class__(self.solution.lhs, rounded_rhs)
        latex_string = latex(rounded_solution)
        latex_fig, latex_ax = plt.subplots(figsize=(4, 1)) 
        latex_ax.text(0.5, 0.5, f"${latex_string}$", fontsize=12, ha='center', va='center')
        latex_ax.axis('off')
        
        image_buffer = io.BytesIO()
        plt.savefig(image_buffer, format='jpg', bbox_inches='tight', transparent=False)
        image_buffer.seek(0)
        plt.close(latex_fig)
        
        solution_image = ImageTk.PhotoImage(Image.open(image_buffer))
        return solution_image
    
    def get_x_at_t(self, time):
        x_solution = lambdify(t, self.solution.rhs, 'numpy')
        x_value = x_solution(time)
        return x_value
    
    def get_velocity_at_t(self, time):
        velocity_solution = lambdify(t, sy.diff(self.solution.rhs, t), 'numpy')
        velocity_value = velocity_solution(time)
        return velocity_value
        
    def get_t_at_x(self, x_value):
        inverse_solution = lambdify(x, sy.solve(self.solution.rhs, t), 'numpy')
        t_value = inverse_solution(x_value)
        return t_value
        
    def get_graph(self, t_0, t_f, samples):
        x_solution = lambdify(t, self.solution.rhs, 'numpy')
        t_values = np.linspace(t_0, t_f, samples)
        x_values = x_solution(t_values)
        
        fig, ax = plt.subplots()
        ax.plot(t_values, x_values)
        ax.set_xlabel('Time [s]')
        ax.set_ylabel('Displacement [m]')
        ax.set_title('Simple Harmonic Oscillator')
        ax.grid(True)
        return fig


#Damped Harmonic Oscillator 
class DHO:
    """
    This class models a damped harmonic oscillator, which means the damping coefficient isn't zero.
    The equation model is: mx'' + bx' + kx = f(t)
    """
    def __init__(self, mass, stiffness, damping_coefficient, x_0, v_0, right_hand_side) -> None:
        self.mass = sy.Rational(mass).limit_denominator()
        self.stiffness = sy.Rational(stiffness).limit_denominator()
        self.damping_coefficient = sy.Rational(damping_coefficient).limit_denominator()
        self.x_0 = x_0
        self.v_0 = v_0
        self.right_hand_side = sy.sympify(right_hand_side)
        self.natural_frequency = np.sqrt(stiffness/mass)
        self.equation = sy.Eq(self.mass * x.diff(t, 2) + self.damping_coefficient * x.diff(t, 1) + self.stiffness * x, self.right_hand_side)
        self.initial_conditions = {x.subs(t, 0): self.x_0, x.diff(t).subs(t, 0): self.v_0}
        self.solution = sy.dsolve(self.equation, x, ics=self.initial_conditions)
        self.damping_ratio = damping_coefficient / (2 * np.sqrt(mass * stiffness))
    
    def get_x_at_t(self, time):
        x_solution = lambdify(t, self.solution.rhs, 'numpy')
        x_value = x_solution(time)
        return x_value
    
    def get_velocity_at_t(self, time):
        velocity_solution = lambdify(t, sy.diff(self.solution.rhs, t), 'numpy')
        velocity_value = velocity_solution(time)
        return velocity_value
        
    def get_t_at_x(self, x_value):
        inverse_function = sy.solve(self.solution.rhs, t)
        print(inverse_function)
        inverse_solution = lambdify(x, inverse_function, 'numpy')
        t_value = inverse_solution(x_value)
        return t_value
        
    def get_behavior(self):
        d_ratio = self.damping_ratio
        match d_ratio:
            case _ if d_ratio > 1:
                return "Overdamped"
            case _ if d_ratio == 1:
                return "Critically damped"
            case _ if d_ratio < 1:
                return "Underdamped"
    
    def get_solution(self):
        rounded_solution = self.solution.evalf(4)
        latex_string = latex(rounded_solution)
        latex_fig, latex_ax = plt.subplots(figsize=(4, 1)) 
        latex_ax.text(0.5, 0.5, f"${latex_string}$", fontsize=12, ha='center', va='center')
        latex_ax.axis('off')
        
        image_buffer = io.BytesIO()
        plt.savefig(image_buffer, format='jpg', bbox_inches='tight', transparent=True)
        image_buffer.seek(0)
        plt.close(latex_fig)
        
        solution_image = ImageTk.PhotoImage(Image.open(image_buffer))
        return solution_image
    
    def get_graph(self, t_0, t_f, samples):
        simplification_part_1 = sy.nsimplify(self.solution.rhs)
        simplification_part_2 = simplification_part_1.evalf()
        x_solution = lambdify(t, simplification_part_2, 'numpy')
        t_values = np.linspace(t_0, t_f, samples)
        x_values = x_solution(t_values)
        fig, ax = plt.subplots()
        ax.plot(t_values, x_values)
        ax.set_xlabel('Time [s]')
        ax.set_ylabel('Displacement [m]')
        ax.set_title('Simple Harmonic Oscillator')
        ax.grid(True)
        return fig

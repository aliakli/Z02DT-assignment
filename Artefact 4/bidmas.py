import ast  # For parsing expressions into AST
import operator  # For basic arithmetic operations
import math  # For math functions and constants


class Calculator:
# ====== Simple calculator supporting arithmetic, trig, logs, and constants ======
    
    def __init__(self, angle_mode=True):
        self.angle_mode = angle_mode  # True for radians, False for degrees
        self.arithmetic_operators = {  # Mapping AST operators to functions
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow
        }
        self.functions = {  # Supported math functions with argument counts
            "sin": (self.sin, 1),
            "cos": (self.cos, 1),
            "tan": (self.tan, 1),
            "arcsin" : (self.arcsin, 1),
            "arccos" : (self.arccos, 1),
            "arctan" : (self.arctan, 1),
            "log": (self.log, 1),
            "ln": (self.ln, 1),
            "log_n": (self.log_n, 2),
            "sqrt": (self.sqrt, 1),
            "cbrt": (self.cbrt, 1),
            "n_rt": (self.n_rt, 2)
        }
        self.constants = {  # Predefined constants
            "pi": math.pi,
            "e": math.e,
            "help": """

====== Trig functions ======
*Default Radians*
sin(angle) 
cos(angle) 
tan(angle) 
====== Inverse Trig Functions ======
*Default Radians*
arcsin(ratio) must be 1>=ratio>=-1
arccos(ratio) must be 1>=ratio>=-1
arctan(ratio)

====== Logarithms ======
log(arg) -> log base 10
ln(arg) -> log base e
log_n(arg, base) -> log base {base}

====== Constants ======
pi = 3.141592653589793
e = 2.718281828459045

"""
        }

    def sin(self, angle):
        if self.angle_mode:
            return round(math.sin(angle), 2)  # Calculate sine in radians
        return round(math.sin(math.radians(angle)), 2)  # Convert degrees to radians
    
    def arcsin(self, ratio):
        if ratio > 1 or ratio < -1:
            return "Ratio must be between 1 and -1"
        if self.angle_mode:
            return round(math.asin(ratio), 3)
        return round(math.degrees(math.asin(ratio)), 3)
    
    def arccos(self, ratio):
        if ratio > 1 or ratio < -1:
            return "Ratio must be between 1 and -1"
        if self.angle_mode:
            return round(math.acos(ratio), 3)
        return round(math.degrees(math.acos(ratio)), 3)
    
    def arctan(self, ratio):
        if self.angle_mode:
            return round(math.atan(ratio), 3)
        return round(math.degrees(math.atan(ratio)), 3)


    def cos(self, angle):
        if self.angle_mode:
            return round(math.cos(angle), 2)  # Calculate cosine in radians
        return round(math.cos(math.radians(angle)), 2)  # Convert degrees to radians

    def tan(self, angle):
        if self.angle_mode:
            return round(math.tan(angle), 2)  # Calculate tangent in radians
        return round(math.tan(math.radians(angle)), 2)  # Convert degrees to radians
    
    def log(self, arg):
        return round(math.log(arg,10),3)  # Logarithm base 10
    
    def ln(self, arg):
        return round(math.log(arg),3)  # Natural logarithm
    
    def log_n(self, arg, base):
        return round(math.log(arg,base),3)  # Logarithm with custom base
    
    def sqrt(self, arg):
        if arg < 0: # Test for complex result
            return "Result cannot be complex" 
        return (round(arg**0.5,3)) # Using laws of indices to get square root
    
    def cbrt(self, arg):
        return (round(arg**(1/3),3)) # Using laws of indices to get cube root
    
    def n_rt(self, arg, root):
        if arg < 0 and root % 2 == 0: # Tessting if the root is even and the argument is negative to avoid complex roots
            return "Result cannot be complex"
        try:
            return (round(arg**(1/root),3)) # Using laws of indices to get the nth root
        except ZeroDivisionError: # Catch the 1/0 error
            return "Cannot take the 0th root"    

    def tokenise_expression(self, expression):
        tokens = ast.parse(expression, mode="eval")  # Parse expression into AST
        return self.evaluate_expression(tokens.body)  # Evaluate parsed AST

    def evaluate_function(self, expression):
        if not isinstance(expression.func, ast.Name):
            raise Exception  # Only named functions allowed

        function_name = expression.func.id  # Get function name
        if function_name not in self.functions:
            raise Exception  # Raise error if function not supported

        function, max_args = self.functions[function_name]  # Get function and arg count
        if len(expression.args) != max_args:
            raise Exception(
                f"Error: {function_name}() takes {max_args} arguments."
            )  # Validate number of arguments

        values = [
            self.evaluate_expression(arg) for arg in expression.args
        ]  # Evaluate all arguments
        return function(*values)  # Call function with evaluated args

    def evaluate_expression(self, expression):
        """Recursively evaluates AST nodes for numbers, constants, functions, and operations."""
        if isinstance(expression, ast.Call):
            return self.evaluate_function(expression)  # Evaluate function calls

        if isinstance(expression, ast.Name):
            if expression.id in self.constants:
                return self.constants[expression.id]  # Return constant value
            raise Exception("Error")  # Undefined variable

        if (
            isinstance(expression, ast.Constant)
            and isinstance(expression.value, (int, float))
        ):
            return expression.value  # Return numeric constant

        if isinstance(expression, ast.BinOp):
            left = self.evaluate_expression(expression.left)  # Evaluate left operand
            right = self.evaluate_expression(expression.right)  # Evaluate right operand
            operation_type = type(expression.op)

            if operation_type in self.arithmetic_operators:
                return self.arithmetic_operators[operation_type](left, right)  # Perform operation

        if isinstance(expression, ast.UnaryOp):
            value = self.evaluate_expression(expression.operand)  # Evaluate operand

            if isinstance(expression.op, ast.UAdd):
                return +value  # Unary plus
            if isinstance(expression.op, ast.USub):
                return -value  # Unary minus

import ast
import operator
import math


class Calculator:
    def __init__(self, angle_mode=True):
        self.angle_mode = angle_mode
        self.answer = 0
        self.arithmetic_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow
            
        }
        self.functions = {
            "sin": (self.sin, 1),
            "cos": (self.cos, 1),
            "tan": (self.tan, 1),
            "log": (self.log, 1),
            "ln": (self.ln, 1),
            "log_n": (self.log, 2),
        }
        self.constants = {
            "pi": math.pi,
            "e": math.e,
            
        }

    def sin(self, angle):
        if self.angle_mode:
            return round(math.sin(angle), 2)
        return round(math.sin(math.radians(angle)), 2)

    def cos(self, angle):
        if self.angle_mode:
            return round(math.cos(angle), 2)
        return round(math.cos(math.radians(angle)), 2)

    def tan(self, angle):
        if self.angle_mode:
            return round(math.tan(angle), 2)
        return round(math.tan(math.radians(angle)), 2)
    
    def log(self, arg):
        return round(math.log(arg,10))
    
    def ln(self, arg):
        return round(math.log(arg))
    
    def log_n(self, arg, base):
        
        return round(math.log(arg, base))

    def tokenise_expression(self, expression):
        tokens = ast.parse(expression, mode="eval")
        return self.evaluate_expression(tokens.body)

    def evaluate_function(self, expression):
        if not isinstance(expression.func, ast.Name):
            raise Exception

        function_name = expression.func.id
        if function_name not in self.functions:
            raise Exception

        function, max_args = self.functions[function_name]
        if len(expression.args) != max_args:
            raise Exception(
                f"Error: {function_name}() takes {max_args} arguments."
            )

        values = [
            self.evaluate_expression(arg) for arg in expression.args
        ]
        return function(values[0])

    def evaluate_expression(self, expression):
        if isinstance(expression, ast.Call):
            return self.evaluate_function(expression)

        if isinstance(expression, ast.Name):
            if expression.id in self.constants:
                return self.constants[expression.id]
            raise Exception("Error")

        if (
            isinstance(expression, ast.Constant)
            and isinstance(expression.value, (int, float))
        ):
            return expression.value

        if isinstance(expression, ast.BinOp):
            left = self.evaluate_expression(expression.left)
            right = self.evaluate_expression(expression.right)
            operation_type = type(expression.op)

            if operation_type in self.arithmetic_operators:
                return self.arithmetic_operators[operation_type](left, right)

        if isinstance(expression, ast.UnaryOp):
            value = self.evaluate_expression(expression.operand)

            if isinstance(expression.op, ast.UAdd):
                return +value
            if isinstance(expression.op, ast.USub):
                return -value

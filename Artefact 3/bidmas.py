import ast
import operator
import math

class Calculator:
    arithmetic_operators = {
        ast.Add : operator.add,
        ast.Sub : operator.sub,
        ast.Mult : operator.mul,
        ast.Div : operator.truediv
        }
    def tokenise_expression(self, expression):
        tokens = ast.parse(expression, mode="eval")
        return self.evaluate_expression(tokens.body)
    
    def evaluate_expression(self, expression):
        if isinstance(expression, ast.Constant) and isinstance(expression.value, (int,float)):
            return expression.value
        if isinstance(expression,ast.BinOp):
            left = self.evaluate_expression(expression.left)
            right = self.evaluate_expression(expression.right)
            operation_type = type(expression.op)
            if operation_type in self.arithmetic_operators:
                return self.arithmetic_operators[operation_type](left,right)

        if isinstance(expression, ast.UnaryOp):
                    val = self.evaluate_expression(expression.operand)
                    if isinstance(expression.op, ast.UAdd):
                        return +val
                    if isinstance(expression.op, ast.USub):
                        return -val

        

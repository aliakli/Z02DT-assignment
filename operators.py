import math
class Operators:
    def __init__(self):
        self.answer = 0

    def clear(self):
        self.answer = 0
        print(self.answer)
        return self.answer

    def memory(self):
        return self.answer

    def add(self, numbers):
        print(self.answer, "+", " + ".join(str(n) for n in numbers))
        self.answer += sum(numbers)
        return self.answer

    def subtract(self, numbers):
        print(self.answer, "-", " - ".join(str(n) for n in numbers))
        self.answer -= sum(numbers)
        return self.answer

    def multiplication(self, numbers):
        print(self.answer, "*", " * ".join(str(n) for n in numbers))
        for n in numbers:
            self.answer *= n
        return self.answer

    def division(self, numbers):
        try:
            print(self.answer, "/", " / ".join(str(n) for n in numbers))
            for n in numbers:
                self.answer /= n
            return self.answer
        except ZeroDivisionError:
            return "Division by zero"
        
    def exponentiation(self, numbers):
        print(self.answer, "^", " ^ ".join(str(n) for n in numbers))
        for n in numbers:
            self.answer **= n
        return self.answer
    
    def sine(self, numbers):
        for n in numbers:
            self.answer += n
        print(f"sin({self.answer})")
        self.answer = math.sin(math.radians(self.answer))
        return self.answer
    
    def cosine(self, numbers):
        for n in numbers:
            self.answer += n
        print(f"cos({self.answer})")
        self.answer = math.cos(math.radians(self.answer))
        return self.answer

    def tangent(self, numbers):
        for n in numbers:
            self.answer += n
        print(f"tan({self.answer})")
        self.answer = math.tan(math.radians(self.answer))
        return self.answer
    
    def log(self, numbers):
        for n in numbers:
            self.answer += n
        print(f"log_10({self.answer})")
        self.answer = math.log10(self.answer)
        return self.answer

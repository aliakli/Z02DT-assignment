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
    
    
        
            
        
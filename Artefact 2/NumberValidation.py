class NumberValidation:
    #Function to validate number 
    def validate_number(self,inp):
        if inp == "=":
            return "="
        else:
            try: 
                a = float(inp)
                return int(a) if a.is_integer() else a
            except ValueError: 
                #If a number given is not a valid number, this prevents the program from crashing 
                return "NaN"
    #Gets number from user input and validates     
    def get_valid_number(self):
        num = input("Enter a number and press '=' to compute: ")
        #Loops until valid number is given
        while self.validate_number(num) == "NaN":
            num = input("Not a valid number\nEnter a number: ")
        return self.validate_number(num)
    def get_numbers(self):
        numbers = []
        #Loops until the final input is '='
        while True:
            #Add the validated number to the end of the list
            numbers.append(self.get_valid_number())
            #Checks if the last value in the array is '='
            if numbers[-1] == "=":
                #Remove the '='
                numbers.pop()
                break
        #Return the array
        return numbers
    



tokens = []
current_num = ""
calculation = input().strip()

def get_numbers(inp):
    numbers = []
    for i in inp:
        if isinstance(i,float):
            numbers.append(i)
    return numbers

def get_operators(inp):
    numbers = []
    for i in inp:
        if not isinstance(i,float):
            numbers.append(i)
    return numbers
            
            

for i in calculation:
    if i.isdigit() or i == ".":
        current_num += i
    elif i in "+-*/()^":
            if current_num:
                current_num = float(current_num)
                
                tokens.append(current_num)
                tokens.append(i)
                current_num = ""
            else:
                tokens.append(i)

numbers = get_numbers(tokens)                
operations = get_operators(tokens)
subexpr = []
if current_num:
    tokens.append(float(current_num))
start = 0
end = 0
for i in (0,len(operations)-1):
    if operations[i] == ")":
        start = i
        for j in range(0,len(operations)-1,-1):
            if operations[j] == "(":
                end = j
                subexpr.append(operations[start:end])
print(subexpr)
                
                

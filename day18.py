def reduce1(stack):
    while len(stack) > 1:
        if stack[1] == "+":
            stack = [stack[0] + stack[2]] + stack[3:]
        elif stack[1] == "*":
            stack = [stack[0] * stack[2]] + stack[3:]
        else:
            assert False
    
    return stack
            
def reduce2(stack):
    while len(stack) > 1:
        while "+" in stack:
            k = stack.index("+")
            stack = stack[:k - 1] + [stack[k - 1] + stack[k + 1]] + stack[k + 2:]
        while "*" in stack:
            stack = [stack[0] * stack[2]] + stack[3:]

    return stack

def parse_line(line, reduce_function):
    stack = []
    for c in line:
        if c.isdigit():
            stack.append(int(c))
        elif c in "*+(":
            stack.append(c)
        elif c == ")":
            temp_stack = []
            while (a := stack.pop()) != "(":
                temp_stack.insert(0, a)
            stack += reduce_function(temp_stack)
    
    stack = reduce_function(stack)
    return stack.pop()

# Part 1

print(sum(parse_line(line, reduce1) for line in open("input")))

# Part 2

print(sum(parse_line(line, reduce2) for line in open("input")))

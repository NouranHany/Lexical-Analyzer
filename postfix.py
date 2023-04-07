import re

def validate_regex(pattern):
    try:
        re.compile(pattern)

    except re.error:
        print("Non valid regex pattern")
        exit()

def replace_range(match_obj):
    replaced=''
    start=None
    end=None
    flag=False
    for char in match_obj.group():
        if char=='[':
            replaced+='('
        elif char==']':
            if replaced[-1]=='|':
                replaced=replaced[:-1]+')'
            else: replaced+=')'
        elif char=='-':
            flag=True
        else:
            if flag:
                end=char
                flag=False
                for i in range(ord(start),ord(end)+1):
                    replaced+=chr(i)
                    replaced+='|'               
            else:
                start=char
    return replaced

def add_concat(pattern):
    literals='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    i=0
    while i != len(pattern)-1:
        a=pattern[i]
        b=pattern[i+1]
        # catches *(  or +( or ?( or )( or a(
        if (a=='*'or a=='+'or a=='?'or a==')' or  a in literals) and b=='(':
            pattern=pattern[:i+1]+'.'+pattern[i+1:]
            i+=2
            continue
        # catches ab or )a or *a or +a or ?a
        if (a in literals or a==')' or a=='*'or a=='+' or a=='?') and b in literals:
            pattern=pattern[:i+1]+'.'+pattern[i+1:]
            i+=2
            continue
        i+=1
    return pattern

def fix_pattern(pattern):
    pattern =re.sub(r'\[(?:.-.)+\]', replace_range,pattern)
    pattern=add_concat(pattern)
    return pattern

def infix_to_postfix(regex):
    output_queue = []
    operator_stack = []
    # the precedence of the operators is defined here
    # the higher the number, the higher the precedence
    operators={"|":1, ".":2, "*":3, "+":3, "?":3}

    for item in regex:
        if item == "(":
            operator_stack.append(item)
        elif item == ")":
            while operator_stack[-1] != "(":
                output_queue.append(operator_stack.pop())
            # remove the "(" from the stack
            operator_stack.pop()
        elif item in operators and len(operator_stack)!=0 and  operator_stack[-1]=='(':
            operator_stack.append(item)
        elif item in operators:
            while operator_stack and operator_stack[-1] != "(" and operators[item] <= operators[operator_stack[-1]]:
                output_queue.append(operator_stack.pop())
            operator_stack.append(item)
        else:
            # the input is a letter or literal
            output_queue.append(item)

    while operator_stack:
        output_queue.append(operator_stack.pop())

    return output_queue

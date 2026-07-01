# Prioritas Operator
precedence = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2
}


# VALIDASI
def validate_expression(expr):

    expr = expr.replace(" ", "")

    if expr == "":
        return False, "Ekspresi kosong."

    allowed = "0123456789+-*/()"

    for c in expr:
        if c not in allowed:
            return False, "Hanya boleh angka dan operator + - * / ( )"

    operators = "+-*/"

    if expr[0] in "+*/":
        return False, "Ekspresi tidak boleh diawali operator."

    if expr[-1] in operators:
        return False, "Ekspresi tidak boleh diakhiri operator."

    # Operator ganda
    for i in range(len(expr)-1):
        if expr[i] in operators and expr[i+1] in operators:
            return False, "Operator ganda tidak diperbolehkan."

    # Kurung seimbang
    stack = []

    for c in expr:

        if c == "(":
            stack.append(c)

        elif c == ")":

            if not stack:
                return False, "Kurung tidak seimbang."

            stack.pop()

    if stack:
        return False, "Kurung tidak seimbang."

    return True, ""

# INFIX -> POSTFIX
def infix_to_postfix_steps(expr):

    expr = expr.replace(" ", "")

    stack = []
    output = []
    steps = []

    number = ""

    for token in expr:

        if token.isdigit():

            number += token

        else:

            if number != "":
                output.append(number)

                steps.append({
                    "token": number,
                    "stack": stack.copy(),
                    "output": output.copy()
                })

                number = ""

            if token == "(":

                stack.append(token)

            elif token == ")":

                while stack and stack[-1] != "(":
                    output.append(stack.pop())

                stack.pop()

            else:

                while (
                    stack
                    and stack[-1] != "("
                    and precedence[token] <= precedence[stack[-1]]
                ):
                    output.append(stack.pop())

                stack.append(token)

            steps.append({
                "token": token,
                "stack": stack.copy(),
                "output": output.copy()
            })

    if number != "":

        output.append(number)

        steps.append({
            "token": number,
            "stack": stack.copy(),
            "output": output.copy()
        })

    while stack:

        output.append(stack.pop())

        steps.append({
            "token": "-",
            "stack": stack.copy(),
            "output": output.copy()
        })

    return output, steps


# EVALUASI POSTFIX
def evaluate_postfix_steps(postfix):

    stack = []

    steps = []

    for token in postfix:

        before = stack.copy()

        if token.isdigit():

            stack.append(int(token))

        else:

            b = stack.pop()

            a = stack.pop()

            if token == "+":
                stack.append(a+b)

            elif token == "-":
                stack.append(a-b)

            elif token == "*":
                stack.append(a*b)

            elif token == "/":

                if b == 0:
                    raise ZeroDivisionError

                hasil = a / b

                if hasil.is_integer():
                    hasil = int(hasil)

                stack.append(hasil)

        steps.append({

            "token": token,

            "before": before,

            "after": stack.copy()

        })

    return stack.pop(), steps
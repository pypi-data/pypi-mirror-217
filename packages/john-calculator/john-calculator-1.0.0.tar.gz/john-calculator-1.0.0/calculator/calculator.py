import re


def calculate(expression):
    # 移除空格
    expression = expression.replace(" ", "")

    # 检查输入表达式是否合法
    if not is_valid_expression(expression):
        raise ValueError("Invalid expression")

    # 使用正则表达式提取数字和操作符
    pattern = r"(\d+|\+|-|\*|/|\(|\))"
    tokens = re.findall(pattern, expression)

    # 转换为后缀表达式
    postfix = infix_to_postfix(tokens)

    # 计算后缀表达式的结果
    result = evaluate_postfix(postfix)

    return result


def is_valid_expression(expression):
    # 使用正则表达式验证表达式是否合法
    pattern = r"^(\d+|\+|-|\*|/|\(|\))*$"
    return re.match(pattern, expression) is not None


def infix_to_postfix(tokens):
    # 运算符的优先级
    precedence = {
        "+": 1,
        "-": 1,
        "*": 2,
        "/": 2,
    }

    postfix = []
    stack = []

    for token in tokens:
        if token.isdigit():
            postfix.append(token)
        elif token == "(":
            stack.append(token)
        elif token == ")":
            while stack and stack[-1] != "(":
                postfix.append(stack.pop())
            stack.pop()  # 移除左括号
        else:
            while stack and stack[-1] != "(" and precedence[token] <= precedence.get(stack[-1], 0):
                postfix.append(stack.pop())
            stack.append(token)

    while stack:
        postfix.append(stack.pop())

    return postfix


def evaluate_postfix(postfix):
    stack = []

    for token in postfix:
        if token.isdigit():
            stack.append(int(token))
        else:
            b = stack.pop()
            a = stack.pop()
            result = perform_operation(token, a, b)
            stack.append(result)

    return stack.pop()


def perform_operation(operator, a, b):
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        return a / b


# 示例用法
expression = input("请输入要计算的表达式: ")
result = calculate(expression)
print("结果:", result)

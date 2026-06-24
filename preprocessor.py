def preprocess_indentation(code):
    lines = code.splitlines()
    result = []
    stack = [0]

    for line in lines:
        if not line.strip():
            continue

        stripped = line.lstrip(' ')
        indent = len(line) - len(stripped)

        if indent > stack[-1]:
            stack.append(indent)
            result.append("<INDENT>")

        elif indent < stack[-1]:
            while indent < stack[-1]:
                stack.pop()
                result.append("<DEDENT>")
            if indent != stack[-1]:
                raise SyntaxError("Indentação inválida")
            
        result.append(stripped)

    while len(stack) > 1:
        stack.pop()
        result.append("<DEDENT>")

    return "\n".join(result)
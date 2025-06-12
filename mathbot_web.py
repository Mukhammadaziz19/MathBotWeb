import re

def clean_expr(expr):
    expr = expr.replace('^', '**')
    expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)  # 2x -> 2*x
    expr = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', expr)  # x2 -> x*2
    expr = expr.replace('=', ' = ')
    return expr

def process_input(user_input):
    try:
        task = guess_task(user_input)
        expr = clean_expr(user_input.lower())

        if task == 'derivative':
            expr = expr.replace('derivative of', '').replace('differentiate', '').strip()
            return f"📉 Derivative: {diff(sympify(expr))}"

        elif task == 'integral':
            expr = expr.replace('integral of', '').replace('integrate', '').strip()
            return f"📈 Integral: {integrate(sympify(expr))} + C"

        elif task == 'solve':
            expr = expr.replace('solve', '').strip()
            lhs, rhs = expr.split('=')
            equation = Eq(parse_expr(lhs), parse_expr(rhs))
            return f"🧠 Solution: {solve(equation)}"

        elif task == 'factor':
            expr = expr.replace('factor', '').strip()
            return f"🧩 Factored: {factor(sympify(expr))}"

        elif task == 'expand':
            expr = expr.replace('expand', '').strip()
            return f"📂 Expanded: {expand(sympify(expr))}"

        elif task == 'simplify':
            expr = expr.replace('simplify', '').strip()
            return f"🧹 Simplified: {simplify(sympify(expr))}"

        elif task == 'percentage':
            expr = expr.replace('%', ' percent').replace('percent', '').replace('of', '').strip()
            numbers = re.findall(r'\d+\.?\d*', expr)
            if len(numbers) == 2:
                percent, of_value = map(float, numbers)
                result = percent / 100 * of_value
                return f"📊 {percent}% of {of_value} = {result}"
            return "❓ Couldn't parse the percentage input."

        elif task == 'arithmetic':
            result = eval(expr)
            return f"🧮 Result: {expr} = {result}"

        else:
            return "❓ I couldn't understand that. Try again."

    except Exception as e:
        return f"⚠️ Error: {str(e)}"

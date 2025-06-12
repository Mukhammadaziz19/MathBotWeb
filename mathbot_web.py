import streamlit as st
from sympy import symbols, Eq, solve, simplify, factor, expand, integrate, diff, sympify
from sympy.parsing.sympy_parser import parse_expr

x, y = symbols('x y')

# Configure page
st.set_page_config(
    page_title="MathBot 🤖🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Auto task detection
def guess_task(expr):
    expr = expr.lower()
    if any(k in expr for k in ['derivative', 'differentiate']):
        return 'derivative'
    elif any(k in expr for k in ['integral', 'integrate']):
        return 'integral'
    elif 'solve' in expr:
        return 'solve'
    elif 'factor' in expr:
        return 'factor'
    elif 'expand' in expr:
        return 'expand'
    elif 'simplify' in expr:
        return 'simplify'
    elif '%' in expr or 'percent' in expr:
        return 'percentage'
    elif any(op in expr for op in ['+', '-', '*', '×', '÷', '/', '**', '^']):
        return 'arithmetic'
    else:
        return 'unknown'

# Process math logic
def process_input(user_input):
    try:
        task = guess_task(user_input)

        if task == 'derivative':
            expr = user_input.replace('derivative of', '').replace('differentiate', '').strip().replace('^', '**')
            return f"📉 Derivative: {diff(sympify(expr))}"

        elif task == 'integral':
            expr = user_input.replace('integral of', '').replace('integrate', '').strip().replace('^', '**')
            return f"📈 Integral: {integrate(sympify(expr))} + C"

        elif task == 'solve':
            expr = user_input.replace('solve', '').strip().replace('^', '**')
            lhs, rhs = expr.split('=')
            equation = Eq(parse_expr(lhs), parse_expr(rhs))
            return f"🧠 Solution: {solve(equation)}"

        elif task == 'factor':
            expr = user_input.replace('factor', '').strip().replace('^', '**')
            return f"🧩 Factored: {factor(sympify(expr))}"

        elif task == 'expand':
            expr = user_input.replace('expand', '').strip().replace('^', '**')
            return f"📂 Expanded: {expand(sympify(expr))}"

        elif task == 'simplify':
            expr = user_input.replace('simplify', '').strip().replace('^', '**')
            return f"🧹 Simplified: {simplify(sympify(expr))}"

        elif task == 'percentage':
            expr = user_input.replace('%', ' percent').replace('of', '').replace('percent', '').strip()
            percent, of_value = expr.split()
            result = float(percent) / 100 * float(of_value)
            return f"📊 {percent}% of {of_value} = {result}"

        elif task == 'arithmetic':
            expr = user_input.replace('×', '*').replace('÷', '/').replace('^', '**')
            result = eval(expr)
            return f"🧮 Result: {expr} = {result}"

        else:
            return "❓ I couldn't understand that. Try again."

    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ---------- UI ----------

st.markdown("<h1 style='text-align: center;'>🧠 MathBot Web App</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Type in a math problem and I’ll break it down for you 💪</p>", unsafe_allow_html=True)
st.markdown("---")

# Responsive form
with st.form(key="math_form"):
    user_input = st.text_area("📥 Enter your math problem below:", height=100, placeholder="E.g. solve 3x + 5 = 20")
    submit = st.form_submit_button("🧠 Solve", use_container_width=True)

# Show results
if submit:
    if user_input.strip():
        results = []
        for line in user_input.strip().splitlines():
            if line:
                results.append(f"🗣️ **Input**: `{line}`")
                results.append(process_input(line))
        st.markdown("---")
        st.markdown("\n\n".join(results))
    else:
        st.warning("Yo, type something first 🤨")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 0.9em;'>Created By: Mukhammadaziz Mamurjonov ⚙️</p>", unsafe_allow_html=True)

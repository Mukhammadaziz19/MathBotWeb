import streamlit as st
from sympy import symbols, Eq, solve, simplify, factor, expand, integrate, diff, sympify
from sympy.parsing.sympy_parser import parse_expr

# Define symbols (more generic)
x, y, z = symbols('x y z')

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="MathBot 🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- MODERN UI ---
st.markdown("""
    <style>
        .main { background-color: #1e1e1e; color: white; }
        .block-container { padding-top: 2rem; }
        textarea, .stTextInput>div>div>input { background-color: #333; color: white; }
        .stButton button { background-color: #4CAF50; color: white; font-weight: bold; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='text-align: center;'>📐 MathBot 2.0</h1>
<p style='text-align: center;'>Drop any math problem. I’ll handle the rest 🧠</p>
<hr style='border-top: 1px solid gray;'>
""", unsafe_allow_html=True)

# --- TASK DETECTION ---
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

# --- MATH ENGINE ---
def process_input(user_input):
    try:
        task = guess_task(user_input)
        expr = user_input.lower().replace('^', '**')

        if task == 'derivative':
            expr = expr.replace('derivative of', '').replace('differentiate', '').strip()
            return f"📉 Derivative: {diff(sympify(expr))}"

        elif task == 'integral':
            expr = expr.replace('integral of', '').replace('integrate', '').strip()
            return f"📈 Integral: {integrate(sympify(expr))} + C"

        elif task == 'solve':
            expr = expr.replace('solve', '').strip()
            if '=' in expr:
                lhs, rhs = expr.split('=')
                equation = Eq(parse_expr(lhs), parse_expr(rhs))
                return f"🧠 Solution: {solve(equation)}"
            else:
                return f"🧠 Roots: {solve(parse_expr(expr))}"

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
            expr = expr.replace('%', '').replace('percent of', '').replace('of', '').strip()
            parts = expr.split()
            if len(parts) >= 2:
                percent, value = float(parts[0]), float(parts[1])
                result = percent / 100 * value
                return f"📊 {percent}% of {value} = {result}"
            else:
                return "❌ Invalid percentage format. Use like: 20% of 50"

        elif task == 'arithmetic':
            expr = expr.replace('×', '*').replace('÷', '/').replace('^', '**')
            result = eval(expr)
            return f"🧮 Result: {expr} = {result}"

        else:
            return "🤷‍♂️ I couldn’t figure out what you meant. Try being clearer."

    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# --- INPUT FORM ---
with st.form("math_form"):
    user_input = st.text_area("📥 Enter a math problem:", height=100, placeholder="E.g. solve x^2 + 5x + 6 = 0")
    submitted = st.form_submit_button("🧠 Calculate")

if submitted:
    if user_input.strip():
        responses = []
        for line in user_input.strip().splitlines():
            responses.append(f"🔹 **Input:** `{line}`")
            responses.append(process_input(line))
        st.markdown("---")
        st.markdown("\n\n".join(responses))
    else:
        st.warning("Yo, type something first 😅")

# --- FOOTER ---
st.markdown("""
<hr style='border-top: 1px solid gray;'>
<p style='text-align: center; font-size: 0.9em;'>Built by Mukhammadaziz 💡 | More Improvements coming soon!💪</p>
""", unsafe_allow_html=True)

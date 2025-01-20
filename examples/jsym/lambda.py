import sympy as sp
import json


def handler(event, context):
    results = {}
    # Define symbols
    x, y, z = sp.symbols("x y z")

    # Define equations
    equation1 = 2 * x + 3 * y - 5
    equation2 = 3 * x - 4 * y + 6

    # Solve equations
    solution = sp.solve((equation1, equation2), (x, y))

    # Convert solution to string for JSON serialization
    results["solution"] = {str(k): str(v) for k, v in solution.items()}

    # Differentiation
    expression = x**3 + 2 * x**2 + 3 * x + 1
    derivative = sp.diff(expression, x)
    results["derivative"] = str(derivative)

    # Integration
    integral = sp.integrate(expression, x)
    results["integral"] = str(integral)

    # Simplification
    expression = (x**2 + 2 * x + 1) / (x + 1)
    simplified_expression = sp.simplify(expression)
    results["simplified"] = str(simplified_expression)

    # Evaluation
    value = expression.subs(x, 5)
    results["evaluate"] = str(value)

    return results

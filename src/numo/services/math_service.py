class MathService:
    """
    Service class for handling mathematical operations.
    """

    pattern = r"^[\d\s\+\-\*\/\(\)\^\%\.\,]+$"

    @staticmethod
    def safe_eval(expression: str) -> float:
        expression = expression.replace("^", "**")
        return eval(expression, {"__builtins__": {}}, {})

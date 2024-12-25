from typing import Optional
import ast
import operator
from src.numo.domain.interfaces.numo_runner import NumoRunner


class MathRunner(NumoRunner):
    """
    Runner for safely evaluating mathematical expressions.
    Uses AST-based evaluation instead of eval() for security.
    """

    # Supported operators and their implementations
    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
    }

    def __init__(self):
        """Initialize with validation settings."""
        self._max_length = 1000  # Maximum expression length
        self._max_depth = 20  # Maximum AST depth

    async def run(self, source: str) -> Optional[str]:
        """
        Safely evaluate a mathematical expression.

        Args:
            source: Mathematical expression to evaluate

        Returns:
            Result as string if successful, None if invalid

        Example:
            >>> runner = MathRunner()
            >>> await runner.run("2 + 2")  # Returns "4"
            >>> await runner.run("1 / 0")  # Returns None
        """
        try:
            # Basic validation
            if not source or not isinstance(source, str):
                return None

            if len(source) > self._max_length:
                return None

            # Parse and evaluate
            node = ast.parse(source, mode="eval")
            if not self._is_safe_ast(node):
                return None

            result = self._evaluate_node(node.body)

            # Validate result
            if not isinstance(result, (int, float)) or not self._is_valid_number(
                result
            ):
                return None

            return str(result)

        except (SyntaxError, ValueError, ZeroDivisionError, OverflowError):
            return None
        except Exception:
            # Catch all other exceptions but don't expose details
            return None

    def _is_safe_ast(self, node: ast.AST, depth: int = 0) -> bool:
        """
        Recursively validate the AST to ensure it only contains safe operations.

        Args:
            node: AST node to validate
            depth: Current recursion depth

        Returns:
            True if AST is safe, False otherwise
        """
        if depth > self._max_depth:
            return False

        # Only allow specific node types
        allowed = (
            ast.Expression,
            ast.Num,
            ast.Constant,
            ast.BinOp,
            ast.UnaryOp,
            ast.Add,
            ast.Sub,
            ast.Mult,
            ast.Div,
            ast.Pow,
            ast.Mod,
            ast.USub,
        )

        if not isinstance(node, allowed):
            return False

        return all(
            self._is_safe_ast(child, depth + 1) for child in ast.iter_child_nodes(node)
        )

    def _evaluate_node(self, node: ast.AST) -> float:
        """
        Recursively evaluate an AST node.

        Args:
            node: AST node to evaluate

        Returns:
            Calculated result

        Raises:
            ValueError: If node type is not supported
        """
        if isinstance(node, (ast.Num, ast.Constant)):
            return float(node.n)

        elif isinstance(node, ast.BinOp):
            left = self._evaluate_node(node.left)
            right = self._evaluate_node(node.right)

            if isinstance(node.op, ast.Pow) and (right > 100 or right < -100):
                raise ValueError("Exponent too large")

            op = self.OPERATORS.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported operation: {type(node.op)}")

            return op(left, right)

        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -self._evaluate_node(node.operand)

        raise ValueError(f"Unsupported node type: {type(node)}")

    def _is_valid_number(self, value: float) -> bool:
        """Check if number is within valid range."""
        return (
            isinstance(value, (int, float))
            and not (value != value)  # Check for NaN
            and abs(value) <= 1e308  # Max float value
            and (abs(value) >= 1e-308 or value == 0)  # Min float value or zero
        )

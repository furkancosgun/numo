import re
from typing import Optional
from src.domain.interfaces.numo_runner import NumoRunner

class MathRunner(NumoRunner):
    def __init__(self):
        # Regular expression pattern for valid mathematical expressions
        self._pattern = r'^[\d\s\+\-\*\/\(\)\^\%\.\,]+$'
    
    async def run(self, source: str) -> Optional[str]:
        try:
            result = eval(source)
            return str(result)
        except Exception:
            return None
    
    def _validate_mathematical_expression(self, expression: str) -> bool:
        """
        Validate if the expression contains only allowed mathematical characters.
        
        Args:
            expression: Mathematical expression to validate
            
        Returns:
            True if expression is valid, False otherwise
        """
        return bool(re.match(self._pattern, expression))
        
    def _prepare_expression(self, expression: str) -> str:
        """
        Prepare expression for evaluation by converting operators.
        
        Args:
            expression: Original mathematical expression
            
        Returns:
            Prepared expression ready for evaluation
        """
        return expression.replace('^', '**')
        
    def _evaluate_expression(self, expression: str) -> float:
        """
        Safely evaluate mathematical expression.
        
        Args:
            expression: Prepared mathematical expression
            
        Returns:
            Calculated result
            
        Raises:
            Various exceptions for invalid expressions
        """
        return eval(expression, {"__builtins__": {}}, {}) 
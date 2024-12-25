from abc import ABC, abstractmethod
from typing import Optional


class NumoRunner(ABC):
    """
    Abstract base class for all runners in the Numo system.

    Runners are responsible for executing specific types of operations such as:
    - Mathematical calculations
    - Unit conversions
    - Currency conversions
    - Language translations
    - Variable operations

    Each runner specializes in a specific domain and implements the run method
    to handle operations within that domain.
    """

    @abstractmethod
    async def run(self, source: str) -> Optional[str]:
        """
        Execute the runner's specific operation on the input string.

        Args:
            source: Preprocessed input string ready for execution

        Returns:
            Result of the operation if successful, None if operation failed

        Example:
            >>> runner = MathRunner()
            >>> await runner.run("1 + 2")  # Returns "3"
            >>> await runner.run("invalid")  # Returns None
        """
        pass

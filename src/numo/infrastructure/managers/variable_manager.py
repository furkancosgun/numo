from typing import Dict, Tuple, Optional
from src.numo.domain.interfaces.numo_manager import NumoManager


class VariableManager(NumoManager):
    """
    Manages variable definitions, operations, and substitutions in mathematical expressions.
    Provides secure variable storage and mathematical operator aliases.
    """

    # Mapping of operator symbols to their aliases
    OPERATOR_ALIASES = {
        "+": ["plus", "add"],
        "-": ["minus", "subtract"],
        "*": ["multiply", "times"],
        "/": ["divide", "division"],
        "%": ["mod", "modulus"],
        "^": ["power", "exponent"],
    }

    def __init__(self):
        """Initialize the VariableManager with default operators and empty variable store."""
        self._variables: Dict[str, str] = {}
        self._initialize_operators()

    def _initialize_operators(self) -> None:
        """Initialize mathematical operator aliases for improved expression readability."""
        for operator, aliases in self.OPERATOR_ALIASES.items():
            # Store the operator itself
            self._variables[operator] = operator
            # Store all its aliases
            for alias in aliases:
                self._variables[alias.lower()] = operator

    def build(self, source: str) -> str:
        """
        Process input string for variable definitions and references.

        Args:
            source: Input string containing variable definition or references

        Returns:
            Processed string with variable references replaced or original if it's a definition
        """
        if not source or not isinstance(source, str):
            return ""

        source = source.strip()
        source, is_definition = self._process_variable_definition(source)

        if not is_definition:
            source = self._replace_variable_references(source)

        return source

    def _validate_variable_name(self, name: str) -> bool:
        """
        Validate variable name according to naming rules.

        Args:
            name: Variable name to validate

        Returns:
            True if name is valid, False otherwise
        """
        if not name or not isinstance(name, str):
            return False

        # Variable names should be alphanumeric and start with a letter
        return name.isalnum() and name[0].isalpha()

    def _process_variable_definition(self, source: str) -> Tuple[str, bool]:
        """
        Process and store variable definition if present.

        Args:
            source: Input string potentially containing variable definition

        Returns:
            Tuple of (processed_source, is_definition)
        """
        # Match either ':' or '=' for assignment
        parts = source.split(":", 1) if ":" in source else source.split("=", 1)

        if len(parts) != 2:
            return source, False

        name = parts[0].strip()
        value = parts[1].strip()

        if not self._validate_variable_name(name):
            return source, False

        # Process the value before storing
        processed_value = self._replace_variable_references(value)
        self._variables[name.lower()] = processed_value

        return f"{name} = {processed_value}", True

    def _replace_variable_references(self, source: str) -> str:
        """
        Replace variable references with their values.

        Args:
            source: Input string containing variable references

        Returns:
            String with variable references replaced by their values
        """
        tokens = source.split()
        processed_tokens = []

        for token in tokens:
            lower_token = token.lower()
            if lower_token in self._variables:
                processed_tokens.append(self._variables[lower_token])
            else:
                processed_tokens.append(token)

        return " ".join(processed_tokens)

    def add_variable(self, name: str, value: str) -> bool:
        """
        Add a new variable to the store.

        Args:
            name: Variable name
            value: Variable value

        Returns:
            True if variable was added successfully, False otherwise
        """
        if not self._validate_variable_name(name):
            return False

        self._variables[name.lower()] = str(value)
        return True

    def get_variable(self, name: str) -> Optional[str]:
        """
        Get variable value by name.

        Args:
            name: Variable name

        Returns:
            Variable value if exists, None otherwise
        """
        return self._variables.get(name.lower())

    def clear_variables(self) -> None:
        """Clear all user-defined variables while preserving operator aliases."""
        stored_operators = {
            name: value
            for name, value in self._variables.items()
            if any(value == op for op in self.OPERATOR_ALIASES.keys())
        }
        self._variables = stored_operators

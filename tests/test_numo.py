import pytest
from src.numo import Numo


@pytest.fixture
def numo():
    """Create a Numo instance for testing."""
    return Numo()


@pytest.mark.asyncio
class TestNumo:
    """Test suite for Numo package."""

    async def test_basic_math(self, numo):
        """Test basic mathematical operations."""
        results = await numo.calculate(["2 + 2", "3 * 4", "10 / 2"])
        assert float(results[0]) == 4.0
        assert float(results[1]) == 12.0
        assert float(results[2]) == 5.0

    async def test_variables(self, numo):
        """Test variable operations."""
        results = await numo.calculate(["x = 5", "y = 3", "z = x + y", "z"])
        assert float(results[0]) == 5.0
        assert float(results[1]) == 3.0
        assert float(results[2]) == 8.0
        assert float(results[3]) == 8.0

    async def test_functions(self, numo):
        """Test mathematical functions."""
        results = await numo.calculate(["abs(-5)", "sqrt(16)", "pow(2, 3)"])
        assert float(results[0]) == 5.0
        assert float(results[1]) == 4.0
        assert float(results[2]) == 8.0

    async def test_unit_conversion(self, numo):
        """Test unit conversions."""
        results = await numo.calculate(["1 km to m", "100 cm to m"])
        assert float(results[0]) == 1000.0
        assert float(results[1]) == 1.0

    async def test_empty_and_invalid_input(self, numo):
        """Test handling of empty and invalid input."""
        results = await numo.calculate(
            ["", "invalid expression", "xyz + 123", "1 km to invalidunit"]
        )
        assert len(results) == 4
        assert all(result is None for result in results)

    async def test_error_handling(self, numo):
        """Test error handling in various scenarios."""
        results = await numo.calculate(
            [
                "1 / 0",  # Division by zero
                "sqrt(-1)",  # Invalid math operation
                "invalid in spanish",  # Invalid translation
                "abc to xyz",  # Invalid unit conversion
            ]
        )
        assert len(results) == 4
        assert all(result is None for result in results)

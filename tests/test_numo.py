import pytest
from src.numo import Numo


@pytest.fixture
def numo():
    """Create a Numo instance for testing."""
    return Numo()


@pytest.mark.asyncio
class TestOther:
    async def test_other(self, numo):
        result = await numo.calculate(["x = 5", "y = 3", "z = x + y", "z"])
        assert float(result[0]) == 5
        assert float(result[1]) == 3
        assert float(result[2]) == 8
        assert float(result[3]) == 8


@pytest.mark.asyncio
class TestNumo:
    async def test_math_operations(self, numo):
        """Test basic mathematical operations."""
        results = await numo.calculate(["2 + 2", "3 * 4", "10 / 2", "2 ^ 3", "10 % 3"])
        assert len(results) == 5
        assert float(results[0]) == 4.0
        assert float(results[1]) == 12.0
        assert float(results[2]) == 5.0
        assert float(results[3]) == 8.0
        assert float(results[4]) == 1.0

    async def test_unit_conversions(self, numo):
        """Test unit conversion functionality."""
        results = await numo.calculate(
            ["1 km to m", "100 cm to m", "1 kg to g", "1 hour to minutes", "1 gb to mb"]
        )
        assert len(results) == 5
        assert float(results[0].split()[0]) == 1000
        assert float(results[1].split()[0]) == 1.0
        assert float(results[2].split()[0]) == 1000
        assert float(results[3].split()[0]) == 60.0
        assert float(results[4].split()[0]) == 1000.0

    async def test_currency_conversion(self, numo):
        """Test currency conversion functionality."""
        results = await numo.calculate(["100 USD to EUR", "50 EUR to JPY"])
        assert len(results) == 2
        for result in results:
            assert result is not None
            amount, currency = result.split()
            assert float(amount) > 0
            assert currency in ["EUR", "JPY"]

    async def test_translation(self, numo):
        """Test translation functionality."""
        results = await numo.calculate(["hello in spanish", "goodbye in french"])
        assert len(results) == 2
        assert results[0].lower() == "hola"
        assert results[1].lower() == "au revoir"

    async def test_variable_management(self, numo):
        """Test variable management functionality."""
        results = await numo.calculate(
            ["x = 5", "y = 3", "x + y", "z = x * y", "z / 2"]
        )
        assert len(results) == 5
        assert float(results[2]) == 8.0
        assert float(results[4]) == 7.5

    async def test_function_calls(self, numo):
        """Test built-in function calls."""
        results = await numo.calculate(
            ["nsum(1,2,3,4)", "navg(2,4,6,8)", "nmax(1,5,3,7)", "nmin(4,2,6,1)"]
        )
        assert len(results) == 4
        assert float(results[0]) == 10.0
        assert float(results[1]) == 5.0
        assert float(results[2]) == 7.0
        assert float(results[3]) == 1.0

    async def test_operator_aliases(self, numo):
        """Test operator alias functionality."""
        results = await numo.calculate(
            ["5 plus 3", "10 minus 4", "3 times 4", "15 divide 3", "7 mod 2"]
        )
        assert len(results) == 5
        assert float(results[0]) == 8.0
        assert float(results[1]) == 6.0
        assert float(results[2]) == 12.0
        assert float(results[3]) == 5.0
        assert float(results[4]) == 1.0

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
        assert all(result is None or result == "" for result in results)

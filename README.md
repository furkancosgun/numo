
# Numo 🔢

Numo is a versatile Python package that combines mathematical operations, unit conversions, currency conversions, and translations in one powerful tool.

## Features ✨

- **Mathematical Operations** 🧮
  - Basic arithmetic (`+`, `-`, `*`, `/`, `^`, `%`)
  - Function support (`nsum`, `navg`, `nmax`, `nmin`)
  - Variable management (`x = 5`, `y = x + 3`)

- **Unit Conversions** 📏
  - Length (km, m, cm, mm, mile, etc.)
  - Weight (kg, g, mg, lb, etc.)
  - Volume (l, ml, gal, etc.)
  - Time (hour, minute, second)
  - Digital Storage (gb, mb, kb)
  - Speed (mph, kmph)
  - Area (m², km², etc.)
  - Angular (degree, radian)

- **Currency Conversions** 💱
  - Real-time exchange rates
  - Support for major currencies (USD, EUR, GBP, etc.)
  - Accurate and up-to-date conversions

- **Text Translation** 🌍
  - Support for multiple languages
  - Simple syntax: "hello in spanish" -> "hola"
  - Powered by Google Translate

## Installation 📦

```bash
pip install numo
```

## Usage 🚀

### Command Line Interface

```bash
# Interactive mode
numo

# Single expression
numo -e "2 + 2"

# Process file
numo -f expressions.txt
```

### Python Library

```python
from numo import Numo
import asyncio

async def main():
    numo = Numo()
    results = await numo.calculate([
        "2 + 2",                  # Math: 4
        "1 km to m",              # Units: 1000 m
        "hello in spanish",       # Translation: hola
        "100 usd to eur",        # Currency: ~85 EUR
        "x = 5",                 # Variables
        "x + 3",                 # Using variables: 8
        "nsum(1, 2, 3, 4, 5)"   # Functions: 15
    ])
    
    for expr, result in zip(expressions, results):
        print(f"{expr} = {result}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Examples 📝

```python
# Mathematical Operations
"2 + 2"              # -> 4
"3 * 4"              # -> 12
"2 ^ 3"              # -> 8

# Unit Conversions
"1 km to m"          # -> 1000 m
"100 cm to m"        # -> 1 m
"1 hour to minutes"  # -> 60 minutes

# Currency Conversions
"100 USD to EUR"     # -> 85.3 EUR
"50 EUR to JPY"      # -> 6150 JPY

# Translations
"hello in spanish"   # -> hola
"goodbye in french"  # -> au revoir

# Variables
"x = 5"              # Define variable
"y = x + 3"          # Use variable: 8

# Functions
"nsum(1,2,3,4)"      # -> 10
"navg(2,4,6,8)"      # -> 5
```

## Development 🛠️

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/furkancosgun/numo.git
cd numo

# Install test dependencies
pip install -e ".[test]"

# Run tests
pytest
```

### Project Structure

```
numo/
├── src/
│   ├── application/     # Core business logic
│   ├── domain/         # Business rules
│   ├── infrastructure/ # External interfaces
│   └── presentation/   # User interfaces
└── tests/             # Test suite
```

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author ✍️

**Furkan Coşgun**
- Email: furkan51cosgun@gmail.com
- GitHub: [@furkancosgun](https://github.com/furkancosgun)


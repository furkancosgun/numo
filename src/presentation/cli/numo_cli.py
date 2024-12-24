from typing import List, Optional
from src.application.numo import Numo

class NumoCLI:
    def __init__(self):
        self.numo = Numo()
        
    async def process_expression(self, expression: str) -> Optional[str]:
        """Process a single expression."""
        results = await self.numo.calculate([expression])
        return results[0] if results else None
        
    async def process_expressions(self, expressions: List[str]) -> None:
        """Process multiple expressions."""
        results = await self.numo.calculate(expressions)
        for expr, result in zip(expressions, results):
            if result:
                print(f"{expr:30} = {result}")
                
    async def interactive_mode(self) -> None:
        """Run in interactive mode."""
        print("Numo Interactive Shell (Press Ctrl+C to exit)")
        print("Examples:")
        print("  2 + 2")
        print("  1 km to m")
        print("  hello in spanish")
        print("  100 usd to eur")
        print("-" * 40)
        
        while True:
            try:
                expression = input(">>> ")
                if not expression:
                    continue
                    
                result = await self.process_expression(expression)
                if result:
                    print(f"{result}")
                else:
                    print("Could not process expression")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {str(e)}") 
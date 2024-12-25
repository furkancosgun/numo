import asyncio
from src.numo import Numo


async def main():
    numo = Numo()
    result = await numo.calculate(["x = 5", "y = 3", "z = x + y", "z"])
    print(result)


asyncio.run(main())

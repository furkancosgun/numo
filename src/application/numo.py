from typing import List, Optional
from src.domain.interfaces.numo_manager import NumoManager
from src.domain.interfaces.numo_runner import NumoRunner
from src.infrastructure.managers import VariableManager, FunctionManager
from src.infrastructure.runners import (
    TranslateRunner,
    UnitRunner,
    CurrencyRunner,
    MathRunner,
    VariableRunner
)

class Numo:
    def __init__(self):
        self._managers: List[NumoManager] = [
            VariableManager(),
            FunctionManager()
        ]
        
        self._runners: List[NumoRunner] = [
            TranslateRunner(),
            UnitRunner(),
            CurrencyRunner(),
            MathRunner(),
            VariableRunner()
        ]
    
    async def calculate(self, lines: List[str]) -> List[Optional[str]]:
        """
        Process multiple lines of input through the Numo engine.
        
        Args:
            lines: List of input strings to process
            
        Returns:
            List of results, None if processing failed
        """
        processed_sources = self._preprocess_input_lines(lines)
        return await self._execute_runners(processed_sources)
        
    async def _execute_runners(self, sources: List[str]) -> List[Optional[str]]:
        results = []
        
        for source in sources:
            if not source:
                results.append(None)
                continue
            
            result = None
            for runner in self._runners:
                runner_result = await runner.run(source)
                if runner_result:
                    result = runner_result
                    break
                    
            results.append(result)
            
        return results
    
    def _preprocess_input_lines(self, sources: List[str]) -> List[str]:
        """
        Preprocess input lines through all managers.
        
        Args:
            sources: List of raw input strings
            
        Returns:
            List of preprocessed strings
        """
        result = []
        
        for source in sources:
            processed_line = source.strip()
            for manager in self._managers:
                processed_line = manager.build(processed_line)
            result.append(processed_line)
            
        return result 
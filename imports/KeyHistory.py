from typing import override 

from .utils.Stack import Stack

class KeyHistory(Stack):
    CURRENT_KEY_IND : int = 0 
    MAX_KEYS        : int = 3

    @override
    def insert(self, value : any) -> None:
        # if self size is more or like max item count, remove last
        if self.get_size() >= self.MAX_KEYS:
            super()._shift_items_left()
        
        super().insert(value)
        
        self.CURRENT_KEY_IND = self.get_size()
    
    def _get_items_string(self) -> str:
        hist_str = "" 

        for i in range(self.get_size()):
            hist_str += self.items[i]
        
        return hist_str
    

    def is_combination_executed(self, combination : str) -> bool:
        if not combination in self._get_items_string():
            return False
        
        # TODO slicker version needed !
        for i in range(1, len(combination) + 1):
            if self.items[-i] != combination[-i]:
                return False

        return True 


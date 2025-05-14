class Stack:

    def __init__(self):
        self.items = []
        self.size = 0

    # TODO for time being its not secure
    def get_size(self) -> int:
        return len(self.items)

    # Count of values inserted
    def insert(self, value : any) -> int:
        self.items.append(value)

        return len(self.items)

    def remove(self) -> any:
        return self.items.pop()
    
    def clean(self) -> None:
        while self.get_size():
            self.remove()

    def _set_items(self, items : list[any]) -> None:
        self.items = items

    def _shift_items_left(self, shift_by:int = 1) -> list:
        new_items = self.items[shift_by:]
        self._set_items(new_items) 
         
    def _shift_items_right(self, shift_by:int = 1) -> list:
        for _ in range(shift_by):
            self.remove()
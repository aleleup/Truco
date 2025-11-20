
class TestUsersWithFastApi:
    def __init__(self) -> None:
        self._items: list[int] = [1,2,3,4,5,6,7]
        self._iterator: int = 0
    def show_item(self, i: int) -> int:
        return self._items[i]

    def show_items_with_method(self) -> list[int]:
        return self._items
    
    def show_items_changing_iterator(self) -> int:
        res: int = self._items[self._iterator]
        self._iterator += 1 if self._iterator < len(self._items) else -self._iterator
        return res
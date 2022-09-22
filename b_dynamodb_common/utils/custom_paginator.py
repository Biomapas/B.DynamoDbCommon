from operator import attrgetter
from typing import List, Optional


class CustomPaginator:
    def __init__(self, objects: List[object], key: str) -> None:
        self.__key = key
        self.__objects = objects
        self.__objects.sort(key=attrgetter(key), reverse=False)
        self.__object_index_map = {_object.__getattribute__(key): index for index, _object in enumerate(self.__objects)}
        self.__next_page_id = None

    @property
    def count(self) -> int:
        return len(self.__objects)

    @property
    def next_page_id(self) -> Optional[str]:
        return self.__next_page_id

    def page(self, limit: Optional[int] = None, page_id: Optional[str] = None) -> List[object]:
        if limit and (not isinstance(limit, int) or limit < 0):
            raise ValueError('Limit must be a positive integer.')

        limit = len(self.__objects) if limit is None else limit

        page_start_idx = 0 if page_id is None else self.__object_index_map.get(page_id)

        if page_start_idx is None:
            return []

        page_end_idx = page_start_idx + limit
        page_end_idx = self.count if page_end_idx >= self.count else page_end_idx

        if page_end_idx == self.count:
            self.__next_page_id = None
        else:
            self.__next_page_id = self.__objects[page_end_idx].__getattribute__(self.__key)

        return self.__objects[page_start_idx:page_end_idx]

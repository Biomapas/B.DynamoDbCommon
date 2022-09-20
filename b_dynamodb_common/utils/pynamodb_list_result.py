from __future__ import annotations

from typing import Any, Dict, TypeVar, List, Optional

from b_dynamodb_common.utils.pynamodb_list_function import PynamoDBListFunction

T = TypeVar('T')


class PynamoDBListResult(List[T]):
    def __init__(
            self,
            list_function: PynamoDBListFunction[T],
    ) -> None:
        super().__init__([])
        self.__list_function = list_function
        # Last evaluated key is set if not all results have been fetched from dynamodb table.
        self.__last_evaluated_key: Optional[Dict[str, Any]] = None
        # A flag that determines whether all results have been fetched from the database.
        self.__finished = False

    @property
    def last_evaluated_key(self) -> Optional[Dict[str, Any]]:
        return self.__last_evaluated_key

    @property
    def finished(self) -> bool:
        return self.__finished

    def fetch(self, recursive: bool = False) -> PynamoDBListResult[T]:
        if self.finished:
            raise RecursionError('All items have already been fetched.')

        while True:
            self.__fetch_single_result()

            if (recursive is False) or (self.__last_evaluated_key is None):
                break

        return self

    def __fetch_single_result(self) -> None:
        kwargs = dict(last_evaluated_key=self.last_evaluated_key) if self.last_evaluated_key else dict()
        items, last_evaluated_key = self.__list_function(**kwargs)

        self.extend(items)
        self.__last_evaluated_key = last_evaluated_key

        if self.__last_evaluated_key is None:
            self.__finished = True

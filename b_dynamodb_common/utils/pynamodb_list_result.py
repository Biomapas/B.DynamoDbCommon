from __future__ import annotations

from typing import TypeVar, List, Optional

from pynamodb.pagination import ResultIterator

from b_dynamodb_common.utils.pynamodb_list_function import PynamoDBListFunction

T = TypeVar('T')


class PynamoDBListResult(List[T]):
    def __init__(
            self,
            list_function: PynamoDBListFunction[T],
    ) -> None:
        super().__init__([])
        self.__list_function: PynamoDBListFunction[T] = list_function
        self.__last_evaluated_key: Optional[str] = None

    @property
    def last_evaluated_key(self) -> Optional[str]:
        return self.__last_evaluated_key

    def fetch(self, recursive: bool = False) -> PynamoDBListResult[T]:
        # TODO do not allow to call this function after completely all results are fetched.
        while True:
            self.__fetch_single_result()

            if (recursive is False) or (self.__last_evaluated_key is None):
                break

        return self

    def __fetch_single_result(self) -> PynamoDBListResult[T]:
        result_iterator: ResultIterator[T] = self.__list_function(last_evaluated_key=self.__last_evaluated_key)

        self.extend(list(result_iterator))
        self.__last_evaluated_key: Optional[str] = result_iterator.last_evaluated_key

        return self

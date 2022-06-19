from __future__ import annotations

from typing import TypeVar, Callable, Generic, List, Optional, Tuple, Any

from pynamodb.pagination import ResultIterator

T = TypeVar('T')


class PynamoDBListFunction(Generic[T]):
    def __init__(
            self,
            function: Callable[[...], ResultIterator[Any]],
            *function_args,
            transformer: Optional[Callable[[Any], T]] = None,
            **function_kwargs,
    ) -> None:
        self.__function = function
        self.__transformer = transformer
        self.__args = function_args
        self.__kwargs = function_kwargs

    def __call__(self, *additional_args, **additional_kwargs) -> Tuple[List[T], Optional[str]]:
        iterator = self.__function(
            *(self.__args + additional_args),
            **{**self.__kwargs, **additional_kwargs}
        )

        items = list(iterator)

        if self.__transformer:
            items = [self.__transformer(item) for item in items]

        return items, iterator.last_evaluated_key

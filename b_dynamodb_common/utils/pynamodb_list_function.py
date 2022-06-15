from __future__ import annotations

from typing import TypeVar, Callable, Generic

from pynamodb.pagination import ResultIterator

T = TypeVar('T')


class PynamoDBListFunction(Generic[T]):
    def __init__(
            self,
            function: Callable[..., ResultIterator[T]],
            *function_args,
            **function_kwargs
    ) -> None:
        self.__function = function
        self.__args = function_args
        self.__kwargs = function_kwargs

    def __call__(self, *additional_args, **additional_kwargs) -> ResultIterator[T]:
        return self.__function(
            *(self.__args + additional_args),
            **{**self.__kwargs, **additional_kwargs}
        )

from typing import TypeVar, Generic, Type

from pynamodb.indexes import Index
from pynamodb.models import Model

T = TypeVar('T')


class ModelTypeFactory(Generic[T]):
    """
    Class that allows to specify "table_name" and "region" meta attributes in pynamodb.Model
    classes dynamically. This class creates subtypes from given model types for dynamic use.

    For example:
    If you have a Model class "User" and have multiple DynamoDB tables that hold users, you can use this
    factory to dynamically specify a table against which you want to perform your actions.

    Example usage:
    >>> from pynamodb.models import Model
    # Create your own model. Example, User model.
    >>> class User(Model): pass
    # Specify table 1 against which an example user will be saved.
    >>> user_model_table_1 = ModelTypeFactory(User).create('user_table_1', 'eu-west-1')
    >>> user_model_table_1(hash_key='hash', range_key='range').save()
    # Specify another table and save user in different table.
    >>> user_model_table_2 = ModelTypeFactory(User).create('user_table_2', 'eu-east-1')
    >>> user_model_table_2(hash_key='hash', range_key='range').save()
    """

    def __init__(self, model_type: Type[T]):
        self.__model_type = model_type

        # Ensure that given generic belongs to pynamodb.Model class.
        if not issubclass(model_type, Model):
            raise TypeError('Given model type must inherit from pynamodb.Model class!')

    def create(self, custom_table_name: str, custom_region: str) -> Type[T]:
        parent_class = self.__model_type

        class InnerModel(parent_class):
            class Meta:
                table_name = custom_table_name
                region = custom_region

        # All initialized indexes will not have model Meta attribute, hence, any operation
        # against the index is going to fail. In order to fix that, for each index
        # set inner model's meta attribute.
        for attribute_name in dir(parent_class):
            attribute = getattr(parent_class, attribute_name)
            if isinstance(attribute, Index):
                # Reverse engineering magic at its finest.
                attribute.Meta.model.Meta = InnerModel.Meta

        return InnerModel

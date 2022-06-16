import uuid
from typing import Callable, List

from pynamodb.attributes import UnicodeAttribute
from pynamodb.models import Model
from pytest import fixture

from b_dynamodb_common_test.integration.infrastructure import Infrastructure


class DummyEntity(Model):
    class Meta:
        table_name = Infrastructure.DYNAMODB_TABLE_NAME
        region = Infrastructure.DYNAMODB_TABLE_REGION

    pk = UnicodeAttribute(hash_key=True)
    data = UnicodeAttribute()


@fixture(scope='function')
def dummy_entity_function() -> Callable[[], DummyEntity]:
    """
    Fixture that returns a function.
    The function saves a dummy entity object in database and returns dummy entity object.

    This fixture does automatic cleanup (deletes created dummy entities in the database) after test run.

    :return: Returns a function that saves dummy entity object in database and returns dummy entity object.
    """
    entities: List[DummyEntity] = []

    def __create() -> DummyEntity:
        entity = DummyEntity()
        entity.pk = str(uuid.uuid4())
        entity.data = str(uuid.uuid4())
        entity.save()

        entities.append(entity)

        return entity

    yield __create

    for entity in entities:
        entity.delete()


@fixture(scope='function')
def dummy_entity(dummy_entity_function) -> DummyEntity:
    """
    Fixture that creates a dummy entity in the database
    and returns newly created dummy entity object.

    This fixture does automatic cleanup (deletes created dummy entities in the database) after test run.

    :return: Returns a newly created and saved dummy entity.
    """
    return dummy_entity_function()

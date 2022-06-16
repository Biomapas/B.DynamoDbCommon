from b_dynamodb_common.utils.pynamodb_list_function import PynamoDBListFunction
from b_dynamodb_common_test.integration.fixtures.dummy_entity import DummyEntity


def test_FUNC_call_WITH_pynamodb_query_function_EXPECT_iterator_returned(dummy_entity_function):
    dummy = dummy_entity_function()

    # Create more dummy data.
    [dummy_entity_function() for _ in range(10)]

    list_function: PynamoDBListFunction[DummyEntity] = PynamoDBListFunction(DummyEntity.query, dummy.pk)
    items = list(list_function())

    # Ensure only single entity was found.
    assert len(items) == 1

    # Ensure that it is the same entity with same data.
    assert items[0].pk == dummy.pk
    assert items[0].data == dummy.data

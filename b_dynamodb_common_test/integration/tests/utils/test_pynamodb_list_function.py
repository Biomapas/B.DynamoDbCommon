from b_dynamodb_common.utils.pynamodb_list_function import PynamoDBListFunction
from b_dynamodb_common_test.integration.fixtures.dummy_entity import DummyEntity


def test_FUNC_call_WITH_pynamodb_query_function_EXPECT_entity_returned(dummy_entity_function):
    dummy = dummy_entity_function()

    # Create more dummy data.
    [dummy_entity_function() for _ in range(10)]

    list_function: PynamoDBListFunction[DummyEntity] = PynamoDBListFunction(DummyEntity.query, dummy.pk)
    items, last_evaluated_key = list_function()

    # Ensure only single entity was found.
    assert len(items) == 1

    # Ensure that it is the same entity with same data.
    assert items[0].pk == dummy.pk
    assert items[0].data == dummy.data

    # Ensure that last evaluated key is not set.
    assert last_evaluated_key is None


def test_FUNC_call_WITH_pynamodb_scan_function_and_transformer_EXPECT_only_pks_returned(dummy_entity_function):
    entities = [dummy_entity_function() for _ in range(10)]
    entities_pk = [entity.pk for entity in entities]

    # Create more dummy data.
    [dummy_entity_function() for _ in range(10)]

    list_function: PynamoDBListFunction[str] = PynamoDBListFunction(
        DummyEntity.scan,
        limit=5,
        filter_condition=DummyEntity.pk.is_in(*[entity.pk for entity in entities]),
        transformer=lambda x: x.pk
    )

    items, last_evaluated_key = list_function()

    # Ensure limited entities returned.
    assert len(items) == 5

    # And that they are transformed to pk (str).
    assert all([isinstance(item, str) for item in items])

    # And returned entities are relevant.
    assert set(items).issubset(set(entities_pk))

    # And that last evaluated key is set.
    assert last_evaluated_key is not None

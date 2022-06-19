import pytest

from b_dynamodb_common.utils.pynamodb_list_function import PynamoDBListFunction
from b_dynamodb_common.utils.pynamodb_list_result import PynamoDBListResult
from b_dynamodb_common_test.integration.fixtures.dummy_entity import DummyEntity


def test_FUNC_fetch_WITH_pynamodb_scan_function_EXPECT_results_returned(dummy_entity_function):
    entities = [dummy_entity_function() for _ in range(50)]

    # Create more dummy data.
    [dummy_entity_function() for _ in range(50)]

    list_function: PynamoDBListFunction[DummyEntity] = PynamoDBListFunction(
        DummyEntity.scan,
        limit=10,
        filter_condition=DummyEntity.pk.is_in(*[entity.pk for entity in entities])
    )

    result = PynamoDBListResult(list_function)

    # We haven't fetched any data, hence total amount should be 0 with an empty last evaluated key.
    assert len(result) == 0
    assert result.last_evaluated_key is None
    assert result.finished is False

    # Do a single fetch operation.
    result.fetch(recursive=False)

    # Since scan limit was 10, we should have a total of 10 entities and a set last evaluated key.
    assert len(result) == 10
    assert result.last_evaluated_key is not None
    assert result.finished is False

    # Lets fetch it one more time.
    result.fetch(recursive=False)

    # Results should be the same i.e. +10 fetched entities, hence 20 in total.
    assert len(result) == 20
    assert result.last_evaluated_key is not None
    assert result.finished is False

    # Now lets use the recursive flag which will finish to fetch absolutely all items from the database.
    result.fetch(recursive=True)

    # Assert that the total amount of entities is 50 and the last evaluated key is empty again.
    assert len(result) == 50
    assert result.last_evaluated_key is None
    assert result.finished is True

    # Now since all items have been fetched, we would expect an exception if we call fetch again.
    with pytest.raises(RecursionError):
        result.fetch()

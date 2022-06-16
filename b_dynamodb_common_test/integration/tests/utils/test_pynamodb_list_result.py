import uuid

from b_dynamodb_common.utils.pynamodb_list_function import PynamoDBListFunction
from b_dynamodb_common.utils.pynamodb_list_result import PynamoDBListResult
from b_dynamodb_common_test.integration.util.dummy_model import Dummy


def test_FUNC_fetch_WITH_pynamodb_scan_function_EXPECT_results_returned():
    seed_data1 = [(str(uuid.uuid4()), str(uuid.uuid4())) for _ in range(50)]
    seed_data2 = [(str(uuid.uuid4()), str(uuid.uuid4())) for _ in range(50)]

    for item in seed_data1 + seed_data2:
        dum = Dummy()
        dum.pk = item[0]
        dum.data = item[1]
        dum.save()

    list_function: PynamoDBListFunction[Dummy] = PynamoDBListFunction(
        Dummy.scan,
        limit=10,
        filter_condition=Dummy.pk.is_in(*[d[0] for d in seed_data1])
    )

    result = PynamoDBListResult(list_function)

    assert len(result) == 0
    assert result.last_evaluated_key is None

    result.fetch(recursive=False)

    assert len(result) == 10
    assert result.last_evaluated_key is not None

    result.fetch(recursive=False)

    assert len(result) == 20
    assert result.last_evaluated_key is not None

    result.fetch(recursive=True)

    assert len(result) == 50
    assert result.last_evaluated_key is None

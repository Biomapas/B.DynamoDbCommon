import uuid

from b_dynamodb_common.utils.pynamodb_list_function import PynamoDBListFunction
from b_dynamodb_common_test.integration.util.dummy_model import Dummy


def test_FUNC_call_WITH_pynamodb_query_function_EXPECT_iterator_returned():
    pk = str(uuid.uuid4())
    data = str(uuid.uuid4())

    seed_data = [(str(uuid.uuid4()), str(uuid.uuid4())) for _ in range(10)]
    seed_data.append((pk, data))

    for item in seed_data:
        dum = Dummy()
        dum.pk = item[0]
        dum.data = item[1]
        dum.save()

    list_function: PynamoDBListFunction[Dummy] = PynamoDBListFunction(Dummy.query, pk)
    items = list(list_function())

    assert len(items) == 1

    assert items[0].pk == pk
    assert items[0].data == data

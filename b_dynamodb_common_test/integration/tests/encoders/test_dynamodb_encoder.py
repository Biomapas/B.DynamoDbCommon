import json
from decimal import Decimal

import pytest

from b_dynamodb_common.encoders.dynamodb_encoder import DynamoDbEncoder
from ordered_set import OrderedSet


def test_FUNC_dumps_WITH_json_dynamodb_encoder_EXPECT_data_serialized():
    data = {
        'key1': 'RandomData',
        'key2': OrderedSet([1, 2, 3]),
        'key3': Decimal(1.1)
    }

    # Make sure that without default serializer, we would get an error.
    with pytest.raises(TypeError):
        json.dumps(data)

    # With custom serializer we should not get an error.
    serialized_data = json.dumps(data, cls=DynamoDbEncoder)
    assert serialized_data == '{"key1": "RandomData", "key2": [1, 2, 3], "key3": 1.1}'

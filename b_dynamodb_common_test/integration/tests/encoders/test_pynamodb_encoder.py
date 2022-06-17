import json

import pytest
from pynamodb.attributes import MapAttribute

from b_dynamodb_common.encoders.pynamodb_encoder import PynamoDbEncoder


def test_FUNC_dumps_WITH_json_dynamodb_encoder_EXPECT_data_serialized():
    data = {
        'key1': MapAttribute(map_key_1='RandomData')
    }

    # Make sure that without default serializer, we would get an error.
    with pytest.raises(TypeError):
        json.dumps(data)

    # With custom serializer we should not get an error.
    serialized_data = json.dumps(data, cls=PynamoDbEncoder)
    assert serialized_data == '{"key1": {"map_key_1": "RandomData"}}'

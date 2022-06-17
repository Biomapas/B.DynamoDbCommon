from typing import Any

from pynamodb.attributes import MapAttribute

from b_dynamodb_common.encoders.dynamodb_encoder import DynamoDbEncoder


class PynamoDbEncoder(DynamoDbEncoder):
    def default(self, o: Any):

        if isinstance(o, MapAttribute):
            return o.as_dict()

        return super(PynamoDbEncoder, self).default(o)

from decimal import Decimal
from json import JSONEncoder
from typing import Any

from ordered_set import OrderedSet


class DynamoDbEncoder(JSONEncoder):
    def default(self, o: Any):

        if isinstance(o, (set, OrderedSet)):
            return list(o)

        if isinstance(o, Decimal):
            return float(o)

        return super(DynamoDbEncoder, self).default(o)

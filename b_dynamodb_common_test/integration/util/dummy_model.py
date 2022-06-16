from pynamodb.attributes import UnicodeAttribute
from pynamodb.models import Model

from b_dynamodb_common_test.integration.infrastructure import Infrastructure


class Dummy(Model):
    class Meta:
        table_name = Infrastructure.get_output(Infrastructure.DYNAMODB_TABLE_NAME_KEY)
        region = Infrastructure.get_output(Infrastructure.DYNAMODB_TABLE_REGION_KEY)

    pk = UnicodeAttribute(hash_key=True)
    data = UnicodeAttribute()

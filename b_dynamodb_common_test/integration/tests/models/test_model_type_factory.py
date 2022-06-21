import uuid

import pytest
from pynamodb.attributes import UnicodeAttribute
from pynamodb.exceptions import DoesNotExist
from pynamodb.models import Model

from b_dynamodb_common.models.model_type_factory import ModelTypeFactory
from b_dynamodb_common_test.integration.infrastructure import Infrastructure


class SampleEntity(Model):
    pk = UnicodeAttribute(hash_key=True)


def test_CLASS_model_type_factory_WITH_multiple_databases_EXPECT_multiple_databases_supported():
    """
    Test whether using ModelTypeFactory multiple databases can be supported.
    """
    factory = ModelTypeFactory(SampleEntity)

    # Create model against 1st database.
    sample_entity_db_1 = factory.create(
        custom_table_name=Infrastructure.get_output(Infrastructure.DYNAMODB_TABLE_A_NAME_KEY),
        custom_region=Infrastructure.get_output(Infrastructure.DYNAMODB_TABLE_A_REGION_KEY)
    )

    # Create model against 2nd database.
    sample_entity_db_2 = factory.create(
        custom_table_name=Infrastructure.get_output(Infrastructure.DYNAMODB_TABLE_B_NAME_KEY),
        custom_region=Infrastructure.get_output(Infrastructure.DYNAMODB_TABLE_B_REGION_KEY)
    )

    pk = str(uuid.uuid4())

    # Save entity in the first database.
    sample_entity_db_1(pk).save()
    # Ensure that it was saved and exists.
    sample_entity_db_1.get(pk)

    # Ensure that it does not exist in the second table.
    with pytest.raises(DoesNotExist):
        sample_entity_db_2.get(pk)

    # VICE VERSA.

    pk = str(uuid.uuid4())

    # Save entity in the second database.
    sample_entity_db_2(pk).save()
    # Ensure that it was saved and exists in the second database.
    sample_entity_db_2.get(pk)

    # Ensure that it does not exist in the first database.
    with pytest.raises(DoesNotExist):
        sample_entity_db_1.get(pk)

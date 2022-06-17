import uuid

import pytest
from pynamodb.attributes import UnicodeAttribute, ListAttribute

from b_dynamodb_common.models.permission_model import PermissionModel
from b_dynamodb_common_test.integration.infrastructure import Infrastructure


class PermissionsEntity(PermissionModel):
    class Meta:
        table_name = Infrastructure.DYNAMODB_TABLE_NAME
        region = Infrastructure.DYNAMODB_TABLE_REGION

    pk = UnicodeAttribute(hash_key=True)

    # Override permissions attribute to e.g. have custom column naming.
    _permissions = ListAttribute(attr_name='direct_permissions', of=UnicodeAttribute, null=True)


@pytest.mark.parametrize(
    'permissions',
    [
        '',
        'ADMIN',
        None,
        True,
        False,
        [1, 2, 3],
        [[], [], {}, {}],
        {'permission': 'ADMIN'},
    ],
)
def test_MODEL_permission_model_WITH_invalid_permissions_EXPECT_exception_raised(permissions):
    with pytest.raises(ValueError):
        PermissionsEntity().permissions = permissions


def test_MODEL_permission_model_WITH_correct_permissions_EXPECT_model_works_as_expected():
    permissions = ['CREATE', 'READ', 'UPDATE']
    pk = str(uuid.uuid4())

    entity = PermissionsEntity()
    entity.pk = pk
    entity.permissions = permissions
    entity.save()

    # Add more permissions and save.
    entity.add_permission('DELETE')
    entity.save()

    refreshed_permissions = PermissionsEntity.get(pk).permissions

    # Make sure all added permissions are present.
    assert sorted(refreshed_permissions) == sorted(permissions + ['DELETE'])

from typing import List, Union

from pynamodb.attributes import ListAttribute, UnicodeAttribute
from pynamodb.models import Model


class PermissionModel(Model):
    """
    PynamoDB model class that contains a "permission" attribute.
    """
    _permissions = ListAttribute(attr_name='permissions', of=UnicodeAttribute, null=True)

    """
    Permissions.
    """

    @property
    def permissions(self) -> List[str]:
        return self._permissions or []

    @permissions.setter
    def permissions(self, value: List[str]) -> None:
        # Make sure list of permissions is actually a list.
        if not isinstance(value, list):
            raise ValueError('Permissions attribute must be a list.')

        self.validate_permissions(*value)
        self._permissions = list(set(value))

    def add_permission(self, permission: str) -> None:
        self.validate_permissions(permission)
        self._permissions.append(permission)

    @staticmethod
    def validate_permissions(*permissions: Union[str, List[str]]) -> None:
        # Ensure values in the list are valid permissions.
        for permission in permissions:
            PermissionModel.__validate_permission(permission)

    @staticmethod
    def __validate_permission(permission: str) -> None:
        # Do not allow any type of falsy values.
        if not permission:
            raise ValueError('Permission is falsy i.e. an empty string, null, etc.')

        # Must be string.
        if not isinstance(permission, str):
            raise ValueError('Permission must be string.')

        # Can not be longer than 250 characters.
        if len(permission) > 250:
            raise ValueError('Permission string is too long.')

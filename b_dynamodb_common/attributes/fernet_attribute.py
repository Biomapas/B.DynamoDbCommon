from typing import Optional

from cryptography.fernet import Fernet
from pynamodb.attributes import UnicodeAttribute


class FernetAttribute(UnicodeAttribute):
    def __init__(self, secret_key: bytes, *args, **kwargs):
        self.__fernet = Fernet(secret_key)
        super().__init__(*args, **kwargs)

    def serialize(self, value: Optional[str] = None) -> Optional[str]:
        if value:
            encrypted_value: bytes = self.__fernet.encrypt(value.encode())
            return super().serialize(encrypted_value.decode())

    def deserialize(self, value: Optional[str] = None) -> Optional[str]:
        if value:
            decrypted_value = self.__fernet.decrypt(value.encode())
            return super().deserialize(decrypted_value).decode()

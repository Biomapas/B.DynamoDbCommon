import base64
from typing import Optional, Any

from pynamodb.attributes import UnicodeAttribute


class KmsAttribute(UnicodeAttribute):
    def __init__(self, kms_boto_client: Any, kms_arn: str, *args, **kwargs):
        self.__kms_arn = kms_arn
        self.__kms_boto_client = kms_boto_client

        super().__init__(*args, **kwargs)

    def serialize(self, value: Optional[str] = None) -> Optional[str]:
        if value:
            encrypted: bytes = self.__encrypt(value)
            encrypted_base64: str = base64.b64encode(encrypted).decode()
            return super().serialize(encrypted_base64)

    def deserialize(self, value: Optional[str] = None) -> Optional[str]:
        if value:
            base64_decoded_value = base64.b64decode(value)
            decrypted = self.__decrypt(base64_decoded_value)
            return super().deserialize(decrypted)

    def __encrypt(self, sensitive_data: str) -> bytes:
        return self.__kms_boto_client.encrypt(
            KeyId=self.__kms_arn,
            Plaintext=sensitive_data.encode()
        )['CiphertextBlob']

    def __decrypt(self, sensitive_data: bytes) -> str:
        return self.__kms_boto_client.decrypt(
            KeyId=self.__kms_arn,
            CiphertextBlob=sensitive_data
        )['Plaintext'].decode()

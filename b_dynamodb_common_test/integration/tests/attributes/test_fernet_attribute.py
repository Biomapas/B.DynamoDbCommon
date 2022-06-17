from cryptography.fernet import Fernet

from b_dynamodb_common.attributes.fernet_attribute import FernetAttribute


def test_FUNC_serialize_deserialize_WITH_non_null_value_EXPECT_serialzied_deserialized() -> None:
    """
    Test whether the serialization/deserialization works.

    :return: No return.
    """
    secret = Fernet.generate_key()
    message = 'hello'

    att = FernetAttribute(secret)

    # Check whether the same instance can encrypt and decrypt and message is the same.
    assert att.deserialize(att.serialize(message)) == message

    # Check if different Fernet instances can work with previously encrypted string.
    assert FernetAttribute(secret).deserialize(att.serialize(message)) == message

# B.DynamoDbCommon

![Pipeline](https://github.com/Biomapas/B.DynamoDbCommon/workflows/Pipeline/badge.svg?branch=master)

A python library that makes it easier to interact with AWS DynamoDB tables.

### Description

This library extends functionality of `pynamodb`, `boto3`, `json`, etc. modules
to make it easier to interact with AWS DynamoDB tables. It contains various 
useful functionalities:

- Attributes (PynamoDB custom attributes);
- Encoders (JSON encoders to work with pynamo/dynamo data types);
- Models (PynamoDB custom models);
- Seeds (Various data seeding functions);
- Utils (Other cool functions);

### Remarks

[Biomapas](https://www.biomapas.com/) aims to modernise life-science industry by sharing its IT knowledge with other companies and the community. 
This is an open source library intended to be used by anyone. 
Improvements and pull requests are welcome. 

### Related technology

- Python3
- Boto3
- AWS DynamoDB
- PynamoDB

### Assumptions

This project assumes you know about DynamoDB service, and you prefer 
using PynamoDB ORM to interact with DynamoDB tables.

- Good Python skills and basis of OOP.
- Good PynamoDB/DynamoDB skills.

### Useful sources

- DynamoDB API reference:<br>https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.API.html
- DynamoDB boto3:<br>https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html
- PynamoDB ORM documentation:<br>https://pynamodb.readthedocs.io/en/latest/
- PynamoDB ORM PyPi:<br>https://pypi.org/project/pynamodb/

### Install

Before installing this library, ensure you have these tools setup:

- Python / Pip

To install this project from source run:

```
pip install .
```

Or you can install it from a PyPi repository:

```
pip install b-dynamodb-common
```

### Usage & Examples

This section shows various examples on how to use this library.

#### Attributes

Attributes module. Contains various custom PynamoDB ORM attribtues.

- **Fernet attribute**

Custom PynamoDB attribute that encrypts data in the database. 
Using Fernet algorithm

```python
class User(Model):
    SECRET_ENCRYPTION_KEY = b'123456'

    first_name = FernetAttribute(SECRET_ENCRYPTION_KEY)
    last_name = FernetAttribute(SECRET_ENCRYPTION_KEY)
```

- **KMS attribute**

Custom PynamoDB attribute that encrypts data in the database. 
Using AWS KMS key to encrypt/decrypt data.

```python
boto_client = boto3.client('kms')
kms_key_arn = 'arn:of:the:custom:kms:key'
    
class User(Model):
    first_name = KmsAttribute(boto_client, kms_key_arn)
    last_name = KmsAttribute(boto_client, kms_key_arn)
```

#### Encoders

Encoders module. Contains various encoding functionality.

- **DynamoDbEncoder**

Custom JSON encoder to handle DynamoDB data types.

```python
data = {
    'key1': 'RandomData',
    'key2': OrderedSet([1, 2, 3]),
    'key3': Decimal(1.1)
}

json.dumps(data, cls=DynamoDbEncoder)
```

- **PynamoDbEncoder**

Custom JSON encoder to handle PynamoDB ORM and DynamoDB data types.

```python
data = {
    'key1': MapAttribute(map_key_1='RandomData'),
    'key2': OrderedSet([1, 2, 3]),
    'key3': Decimal(1.1)
}

json.dumps(data, cls=PynamoDbEncoder)
```

#### Models

Models module. Contains various PynamoDB-based custom models.

- **Permission model**

Model that contains permissions attribute.

```python
entity = PermissionsModel()
entity.pk = 'PK'
entity.permissions = ['list', 'of', 'permissions']
entity.save()

# Add more permissions and save.
entity.add_permission('permission')
entity.save()
```

#### Seeds

Currently this module is empty.

#### Utils

Utilities module. Contains lots of cool functions.

- **List function**

Wraps PynamoDB `query` and `scan` functions for better management.

```python
list_function: PynamoDBListFunction[DummyEntity] = PynamoDBListFunction(DummyEntity.query, 'PK')
items = list(list_function())
```
- **List results**

Wraps PynamoDB `query` and `scan` functions to handle recursive `last_evaluated_key` tokens.

```python
list_function: PynamoDBListFunction[DummyEntity] = PynamoDBListFunction(
    DummyEntity.scan,
    limit=10,
    filter_condition=DummyEntity.pk.is_in([...])
)

result = PynamoDBListResult(list_function)

# Fetch one time.
result.fetch(recursive=False)

# Check whether all results have been fetched.
result.finished

# If not, feel free to call it one more time and not worry about last_evaluated_key.
result.fetch(recursive=False)

# If you want to retrieve absolutely all results in one call:
result.fetch(recursive=True) # Simple!
```

### Testing

This package has integration tests based on **pytest**.
To run tests simply run:

```
pytest b_dynamodb_common_test/integration/tests
```

### Contribution

Found a bug? Want to add or suggest a new feature? 
Contributions of any kind are gladly welcome. 
You may contact us directly, create a pull-request or an issue in github platform. 
Lets modernize the world together.

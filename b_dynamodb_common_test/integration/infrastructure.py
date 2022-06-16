import boto3
from aws_cdk.core import Construct
from b_aws_testing_framework.tools.cdk_testing.testing_stack import TestingStack
from aws_cdk.aws_dynamodb import Table, Attribute, AttributeType


class Infrastructure(TestingStack):
    # Statically set table name.
    DYNAMODB_TABLE_NAME = TestingStack.global_prefix() + 'Table'
    # Dynamically resolve current region.
    DYNAMODB_TABLE_REGION = boto3.session.Session().region_name

    def __init__(self, scope: Construct):
        super().__init__(scope=scope)

        self.table = Table(
            scope=self,
            id='TestingDynamoDbTable',
            partition_key=Attribute(name='pk', type=AttributeType.STRING),
            table_name=self.DYNAMODB_TABLE_NAME
        )

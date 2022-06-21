import boto3
from aws_cdk.core import Construct
from b_aws_testing_framework.tools.cdk_testing.testing_stack import TestingStack
from aws_cdk.aws_dynamodb import Table, Attribute, AttributeType


class Infrastructure(TestingStack):
    # Statically set table name.
    DYNAMODB_TABLE_NAME = TestingStack.global_prefix() + 'Table'
    # Dynamically resolve current region.
    DYNAMODB_TABLE_REGION = boto3.session.Session().region_name

    DYNAMODB_TABLE_A_NAME_KEY = 'TableNameAKey'
    DYNAMODB_TABLE_A_REGION_KEY = 'TableRegionAKey'
    DYNAMODB_TABLE_B_NAME_KEY = 'TableNameBKey'
    DYNAMODB_TABLE_B_REGION_KEY = 'TableRegionBKey'

    def __init__(self, scope: Construct):
        super().__init__(scope=scope)

        self.table = Table(
            scope=self,
            id='TestingDynamoDbTable',
            partition_key=Attribute(name='pk', type=AttributeType.STRING),
            table_name=self.DYNAMODB_TABLE_NAME
        )

        self.dynamic_table_a = Table(
            scope=self,
            id='TestingDynamicDynamoDbTableA',
            partition_key=Attribute(name='pk', type=AttributeType.STRING),
        )

        self.add_output(self.DYNAMODB_TABLE_A_NAME_KEY, self.dynamic_table_a.table_name)
        self.add_output(self.DYNAMODB_TABLE_A_REGION_KEY, self.dynamic_table_a.stack.region)

        self.dynamic_table_b = Table(
            scope=self,
            id='TestingDynamicDynamoDbTableB',
            partition_key=Attribute(name='pk', type=AttributeType.STRING),
        )

        self.add_output(self.DYNAMODB_TABLE_B_NAME_KEY, self.dynamic_table_b.table_name)
        self.add_output(self.DYNAMODB_TABLE_B_REGION_KEY, self.dynamic_table_b.stack.region)

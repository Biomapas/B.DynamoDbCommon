from aws_cdk.core import Construct
from b_aws_testing_framework.tools.cdk_testing.testing_stack import TestingStack
from aws_cdk.aws_dynamodb import Table, Attribute, AttributeType


class Infrastructure(TestingStack):
    DYNAMODB_TABLE_NAME_KEY = 'DynamoDbTableNameKey'
    DYNAMODB_TABLE_REGION_KEY = 'DynamoDbTableRegionKey'
    DYNAMODB_TABLE_ARN_KEY = 'DynamoDbTableArnKey'

    def __init__(self, scope: Construct):
        super().__init__(scope=scope)

        self.table = Table(
            scope=self,
            id='TestingDynamoDbTable',
            partition_key=Attribute(name='pk', type=AttributeType.STRING)
        )

        self.add_output(self.DYNAMODB_TABLE_NAME_KEY, self.table.table_name)
        self.add_output(self.DYNAMODB_TABLE_REGION_KEY, self.table.stack.region)
        self.add_output(self.DYNAMODB_TABLE_ARN_KEY, self.table.table_arn)

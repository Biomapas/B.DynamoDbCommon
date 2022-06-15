from aws_cdk.core import Construct
from b_aws_testing_framework.tools.cdk_testing.testing_stack import TestingStack


class Infrastructure(TestingStack):
    def __init__(self, scope: Construct):
        super().__init__(scope=scope)

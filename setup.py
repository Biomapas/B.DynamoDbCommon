from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

with open('VERSION') as file:
    VERSION = file.read()
    VERSION = ''.join(VERSION.split())

setup(
    name='b_dynamodb_common',
    version=VERSION,
    license='Apache License 2.0',
    packages=find_packages(exclude=[
        # Exclude virtual environment.
        'venv',
        # Exclude test b_dynamodb_common files.
        'b_dynamodb_common_test'
    ]),
    description=(
        'Common functionality for interacting with dynamodb easier. '
        'Most of the functionality is based on PynamoDB ORM library.'
    ),
    long_description=README + '\n\n' + HISTORY,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[
        # This library includes nice ORM for dynamodb.
        "pynamodb>=5.0.3,<6.0.0",
        # Cryptography utilities. Used for various encryption methods.
        # NOTE! This library is extremely python-version-specific.
        # Therefore please take a close look on which python version it was built/installed.
        # Cryptography might not work if build environment python version is not the same as
        # your Lambda functions python version. For safety, use Python 3.8.
        "cryptography>=35.0.0,<38.0.0"
    ],
    keywords='AWS DynamoDB PynamoDB Database ORM Python',
    url='https://github.com/biomapas/B.DynamoDbCommon.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)

'''
    You must replace <FoodProducts> with the table name
'''


import boto3

def create_table():

    # configures the SDK for Python resource 
    DDB = boto3.resource('dynamodb', region_name='us-east-1')

    params = {
        'TableName': 'FoodProducts', 
        'KeySchema': [
            {'AttributeName': 'product_name', 'KeyType': 'HASH'}
        ],
        'AttributeDefinitions': [
            {'AttributeName': 'product_name', 'AttributeType': 'S'}
        ],
        'ProvisionedThroughput': {
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    }
    # Boto requires key values arguments rather than the object literal format, so here we use **params to pass the parameters to the create_table operation.
    table = DDB.create_table(**params)
    table.wait_until_exists()
    print ("Done")
    

if __name__ == '__main__':
    create_table()


"""
Copyright @2021 [Amazon Web Services] [AWS]
    
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

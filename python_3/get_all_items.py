'''
    You must replace <FMI_1> with the table name
'''

import boto3


def get_all_items():
    import boto3

    DDB = boto3.resource('dynamodb', region_name='us-east-1')

    table = DDB.Table('FoodProducts')

    response = table.scan()
    data = response['Items']
    
    # If the result of the scan operation is large, DynamoDB splits the results into 1 MB chunks of information (or the first 25 items if their total is less than 1 MB). These chunks of returned data are called pages. 
    # When the while loop runs, the code processes each page, which is also known as pagination. The loop then appends records to the end of the result set until all data has been received:
    
    while response.get('LastEvaluatedKey'):
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    print (data)
    
if __name__ == '__main__':
    get_all_items()


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

         ___        ______     ____ _                 _  ___  
        / \ \      / / ___|   / ___| | ___  _   _  __| |/ _ \ 
       / _ \ \ /\ / /\___ \  | |   | |/ _ \| | | |/ _` | (_) |
      / ___ \ V  V /  ___) | | |___| | (_) | |_| | (_| |\__, |
     /_/   \_\_/\_/  |____/   \____|_|\___/ \__,_|\__,_|  /_/ 
 ----------------------------------------------------------------- 


Hi there! Welcome to AWS Cloud9!

To get started, create some files, play with the terminal,
or visit https://docs.aws.amazon.com/console/cloud9/ for our documentation.

Happy coding!


----

## Preparing the lab

Download and extract the files that you need for this lab. Run the following command in the same terminal:

```
wget https://aws-tc-largeobjects.s3.us-west-2.amazonaws.com/CUR-TF-200-ACCDEV-2/lab-03-dynamo/code.zip -P /home/ec2-user/environment
```

You should see that the `code.zip` file was downloaded to the AWS Cloud9 instance and is now in the left navigation pane.

Extract the file by running the following command: 

```
unzip code.zip
```

Run a script that upgraded the version of Python installed on the Cloud9 instance. It will also upgrade the version of the AWS CLI installed.

To set permissions on the script and then run it, run the following commands:

```
chmod +x ./resources/setup.sh && ./resources/setup.sh
```

Verify the AWS CLI version and also verify that the SDK for Python is installed.

Confirm that the AWS CLI is now at version 2 by running the `aws --version` command.

In the AWS Cloud9 Bash terminal (at the bottom of the IDE), run the following command:

`pip show boto3`

## Creating a DynamoDB table by using the SDK for Python

To Create table

Go to the directory > 

`python_3/create_table.py`


```cli
cd python_3
python3 create_table.py
```


Listing tables in dynamodb
```cli
 aws dynamodb list-tables --region us-east-1
```

The output should be similar to the following example:

```json
{
  "TableNames": [
      "FoodProducts"
  ]
}
```

## Working with DynamoDB data – Understanding DynamoDB condition expressions


Review the JavaScript Object Notation (JSON) data that defines the new record.

Expand the `resources` folder.
Open the `not_an_existing_product.json` file by double-clicking it.

**Analysis:** This file contains one item with two attributes: product_name and product_id. 
Both of these attributes are strings. The primary key (product_name) was defined when the DynamoDB table was created. 
Because DynamoDB tables are schemaless (to be exact, not bound by a fixed schema), we can add new attributes to the table when items are inserted or updated. 
With DynamoDB, we don't need to change the table definition before we add records that contain additional attributes.

To insert the new record, run the following command. Ensure that you are still in the python_3 folder.

```
aws dynamodb put-item \
--table-name FoodProducts \
--item file://../resources/not_an_existing_product.json \
--region us-east-1

```

If we update the product_name, keeping the product_id same in the `not_an_existing_product.json` file, and rerunning above command. It inserts the new data. However, if we re-run the above command without any changes, it doesn't insert any new records.

When a primary key doesn't exist in the table, the DynamoDb `put-item` command inserts a new item. 
However, if the primary key already exists, this command replaces the existing record with the new record, removing any previous attributes. 
This behavior is why you don't see a new item in the table: the record was overwritten with identical information. The primary key prevents the same product_name values from being added multiple times.

However, we don't want this behavior. We want separate operations for adding new products and for updating product attributes. 

To implement this feature, we can refine the behavior of the `put-item` command with condition expressions. We can use condition expressions to determine which item should be modified. 
In this case, we must prevent records from being overwritten if they already exist in the table. The `attribute_not_exists()`` function provides this capability.

Next, we test the condition expression. We try to insert another version of the record for best pie. 

Run the following AWS CLI `put-item` command:

```
aws dynamodb put-item \
--table-name FoodProducts \
--item file://../resources/an_existing_product.json \
--condition-expression "attribute_not_exists(product_name)" \
--region us-east-1
```

The command should return this output: 

`An error occurred (ConditionalCheckFailedException) when calling the     PutItem operation: The conditional request failed`

This behavior is expected because the condition expression prevented an overwrite of the existing item.


## Adding and modifying a single item by using the SDK

In the AWS Cloud9 IDE, go to the python_3 directory.

Open the `conditional_put.py` script.

Make necessary changes as below:

```python3
'''
    You must replace <FMI_1> with the table name FoodProducts
    You must replace <FMI_2> with a product name. apple pie
    You must replace <FMI_3> with a444
    You must replace <FMI_4> with 595
    You must replace <FMI_5> with the description: It is amazing!
    You must replace <FMI_6> with a tag: whole pie
    You must replace <FMI_7> with a tag: apple
'''

import boto3
from botocore.exceptions import ClientError

def conditional_put():
    
    DDB = boto3.client('dynamodb', region_name='us-east-1')
    
    try:
        response = DDB.put_item(
            TableName='FoodProducts',
            Item={
                'product_name': {
                    'S': 'apple pie'
                },
                'product_id': {
                    'S': 'a555'
                },
                'price_in_cents':{
                    'N': '595' #number passed in as a string (ie in quotes)
                },
                'description':{
                    'S': "It is amazing!"
                },
                'tags':{
                    'L': [{
                            'S': 'whole pie'
                        },{
                            'S': 'apple'
                        }]
                }
            },
            ConditionExpression='attribute_not_exists(product_name)'
        )

```

Run the script

```cli
python3 conditional_put.py
#Done
```


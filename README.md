# Working with Amazon DynamoDB

         ___        ______     ____ _                 _  ___  
        / \ \      / / ___|   / ___| | ___  _   _  __| |/ _ \ 
       / _ \ \ /\ / /\___ \  | |   | |/ _ \| | | |/ _` | (_) |
      / ___ \ V  V /  ___) | | |___| | (_) | |_| | (_| |\__, |
     /_/   \_\_/\_/  |____/   \____|_|\___/ \__,_|\__,_|  /_/ 
 -----------------------------------------------------------------

Hi there! Welcome to AWS Cloud9!

To get started, create some files, play with the terminal,
or visit <https://docs.aws.amazon.com/console/cloud9/> for the documentation.

Happy coding!

---

## Preparing the lab

Download and extract the files that we need for this lab. Run the following command in the same terminal:

```cli
wget https://aws-tc-largeobjects.s3.us-west-2.amazonaws.com/CUR-TF-200-ACCDEV-2/lab-03-dynamo/code.zip -P /home/ec2-user/environment
```

You should see that the `code.zip` file was downloaded to the AWS Cloud9 instance and is now in the left navigation pane.

Extract the file by running the following command:

```cli
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

To Create table: Go to the directory > `python_3/create_table.py`

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

---

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

---

## Adding multiple items by using the SDK and batch processing

In the AWS Cloud9 IDE, open the `resources` > test.json file, and review the data.

This file contains six records that you use to test the batch-load script. Notice that this file contains multiple entries for `apple pie` on purpose.

Update the `test_batch_put.py` script:

In the AWS Cloud9 IDE, open the `python_3` > `test_batch_put.py` script.

Update the <FMI_1> placeholder with the FoodProducts table name.

Replace the <FMI_2> with the product_name primary key name.

In the upper left, choose File > Save to save your changes.

To understand the script, the table that will be written to by the script is defined in the `table` variable.

The with statement that begins on line 12 calls `batch_writer()``, which opens the connection to the database.

Then, the code loops through each record and inserts the new data into the FoodProducts table:

```python3
table = DDB.Table('FoodProducts')
with table.batch_writer(overwrite_by_pkeys=['product_name']) as batch:
   for food in food_list:
       price_in_cents = food['price_in_cents']
       product_name = food['product_name']
```

Run the script:

```cmd
python3 test_batch_put.py
```

Instead of keeping the first value of `price_in_cents`, for `apple_pie`, the most recent value in the data file was applied. Why did this behavior happen?

With single-item PUT requests (put_item), we can avoid overwriting duplicate records by including a condition.
However, with batch inserts, we have two options for handling duplicate keys. We can either allow the overwrite, or we can cause the entire batch process to fail.

In the `test_batch_put.py` script on line 12, `overwrite_by_pkeys=['product_name']` parameter is included in the `batch_writer` method. This parameter tells DynamoDB to use last write wins if the key already exists.
Last write wins is why the `price_in_cents` attribute was updated for `apple pie`.

For this dataset, it's better for the load to fail when duplicate `product_name` values are found instead of allowing the update to add incorrect values.

We must change the script so that it fails when duplicates are included in the batch. We can then review and clean up the data.
To implement this feature, we remove the `overwrite_by_pkeys` parameter from the `batch_writer` method.

We can fix the overwrite behavior by updating the `test_batch_put.py` script and preparing to load the production data.

In the AWS Cloud9 IDE, open python_3 > test_batch_put.py.
Update line 12 by changing <with table.batch_writer(overwrite_by_pkeys=['product_name']) as batch> to the following and saving the file:

```
with table.batch_writer() as batch:
```

Run the script:

```
python3 test_batch_put.py
```

We will get an error:
The important feedback in this output is the
`ClientError: An error occurred (ValidationException) when calling the BatchWriteItem operation: Provided list of item keys contains duplicates.`

This is good; you wish to fail hard and fast if there is a problem. You don't want some items being added and some not. You can leverage this error to catch issues in your JSON data and weed out any duplicate items.

Using this fail-fast approach, you can now try to load the actual data that the website will use.

In AWS Cloud9, review the contents of the `resources/website/all_products.json` file. You will find many items. These items have several attributes, and some include an optional integer attribute called `specials`.

In order to load the raw JSON used in the website, you use a new script called `batch_put.py`.

It is very similar to the `test_batch_put.py` script. This script allows for the optional integer special attribute and also maps the names of more fields to the correct DynamoDB attribute types.

We need to modify the `python_3/batch_put.py` script.

Replace <FMI> with FoodProducts and save the changes.

Run the script:

```
python batch_put.py
```

---

## Querying the table by using the SDK

The SDK has two operations for retrieving data from a DynamoDB table: `scan()` and `query()`.

The `scan` operation reads all records in the table, and unwanted data can then be filtered out.
If only a subset of the table data is needed, the query operation often provides better performance because it reads only a subset of the records in the table or index.

We will show all the menu items on the café website, so let us use the `scan()`` operation to retrieve all records from the table.

In AWS Cloud9 IDE, open `python_3 > get_all_items.py`.

Notice the while loop that begins on line 18.

If the result of the scan operation is large, DynamoDB splits the results into 1 MB chunks of information (or the first 25 items if their total is less than 1 MB). These chunks of returned data are called pages.
When the while loop runs, the code processes each page, which is also known as pagination. The loop then appends records to the end of the result set until all data has been received:

```python3
 response = table.scan()
 data = response['Items']
 while response.get('LastEvaluatedKey'):
    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
     data.extend(response['Items'])
     
```

Query that returns a single product instead of returning all products.

Update the `get_one_item.py` script.

Focus on lines 13 and 14, which define the response variable. The get_item operation requires a TableName and a Key. The Key parameter is used to compare the table's primary key, product_name, with the value that is passed in from the main module of the script.

On line 24, note the value that's assigned to the product variable. Also observe that this value is passed to the get_one_item function.

```python3
response = DDB.get_item(TableName='FoodProducts',
  Key={
   'product_name': {'S': product}
   }
  )
data = response['Item']
print (data)
if __name__ == '__main__':
  product = "chocolate cake"
  get_one_item(product)
```

**Note:** The get_item operation is a higher level abstraction of the query operation. It is designed to return a single item.

Run the script:

```
python3 get_one_item.py
```

---

## Adding a global secondary index to the table

Update the `add_gsi.py` script.

The index `special_GSI` is created which consist of one attribute, `special`, which is a number. The index is created with the `Create` action.
Similarly to the table creation, the line that defines the `table` variable also updates the table.

```python
params = {
        'TableName': 'FoodProducts',
        'AttributeDefinitions': [
            {'AttributeName': 'special', 'AttributeType': 'N'}
        ],
        'GlobalSecondaryIndexUpdates': [
            {
                'Create': {
                    'IndexName': 'special_GSI',
                    'KeySchema': [
                        {
                            'AttributeName': 'special',
                            'KeyType': 'HASH'
                        }
                    ],
                        'Projection': {
                        'ProjectionType': 'ALL'
                    },
                        'ProvisionedThroughput': {
                        'ReadCapacityUnits': 1,
                        'WriteCapacityUnits': 1
                    }
                }
            }
        ]
    }

    table = DDB.update_table(**params)
```

```
python3 add_gsi.py
```

Note:  It can take up to 5 minutes for the index to populate.

The `special_GSI` index is a sparse index, meaning it does not have as many items as the main table. It is a subset of the data and is more efficient to scan when you want to find only the items that are part of the specials menu.

Update the `scan_with_filter.py` script.

On line 18, including the `IndexName` option lets the `scan` operator know that it will be going to the index and not the main table to read the data.

On line 19, the filter expression processes the records that have been read and shows only records that meet the comparison criteria. In this case, it shows records only if they don't have `out of stock` in the `tags` attribute. This ensures that only items that are available or "on offer" are shown to customers.

```python
response = table.scan(
  IndexName='special_GSI',
  FilterExpression=Not(Attr('tags').contains('out of stock')))
```

Run the script:

```python
python3 scan_with_filter.py
```

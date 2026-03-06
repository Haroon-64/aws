# DynamoDB

## setup

- trigger lambda using http, and use dynamoDB for persistence

- create table:

    ```sh
        aws dynamodb create-table \
        --table-name users \
        --attribute-definitions AttributeName=userId,AttributeType=S \
        --key-schema AttributeName=userId,KeyType=HASH \
        --billing-mode PAY_PER_REQUEST \
    ```

- create http api:

    ```sh
    aws apigatewayv2 create-api \
    --name users-api \
    --protocol-type HTTP \
    --target arn:aws:lambda:us-east-1:000000000000:function:createUser \
    --output json \
    ```

- invoke:

    ```sh
        aws lambda invoke --function-name createUser --cli-binary-format raw-in-base64-out --payload file://event.json out.json
    ```

    or curl:

    ```sh
        curl -X POST \
        -H "Content-Type: application/json" \
        -d "{\"userId\":\"u1\",\"name\":\"alex\",\"email\":\"alex@mail.com\"}" \
        http://localhost:4566/users  // or http://host.docker.internal:4566/users
    ```

- dynamoDb ops:

  ```py
  table.put_item(
            Item={
                "userId": "u1",
                "name": "alex",
                "email": "<alex@mail.com>"
            }
        )```

  - ```py
  response = table.get_item(
            Key={"userId": "u1"}
        )```

  - ```py
  table.update_item(
            Key={"userId":"u1"},
            UpdateExpression="SET email=:e",
            ExpressionAttributeValues={
                ":e": "<new@mail.com>"
            }
        )```

  - ```py
  table.delete_item(
            Key={"userId": "u1"}
        )```

  - ```py
  response = table.query(
            KeyConditionExpression=Key("userId").eq("u1")
        )```

  - ```py
  response = table.scan()
  ```

## notes

options:
    - local/global Secondary Index - for sorting and filtering
    - stream spec - for event-driven architecture
    - Time to Live (TTL) - for automatic item deletion
    - Table class - STANDARD and STANDARD_INFREQUENT_ACCESS. - for cost optimization
    - Tags - for cost allocation and management
    - SSE spec - encryption

attribute types: S - string, N - number, B - binary

DynamoDB requires only the primary key to be defined in the table schema. All other attributes are schemaless.

to create logs/streams:
    policy:

```json
        {
        "Effect": "Allow",
        "Action": [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
        ],
        "Resource": "*"
        }
```

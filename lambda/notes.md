# lambda

## setup

1. create role:  aws iam create-role --role-name lambda-role --assume-role-policy-document file://role.json
2. attach policy: aws iam attach-role-policy --role-name lambda-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
   or file: aws iam attach-role-policy --role-name lambda-role --policy-document file://policy.json

    - > lambda does not have a identitiy like a user, so we use role to grant permissions to lambda by telling it to assume the role ex "Action": "sts:AssumeRole"

3. setup lambda:
    `pip install -r requirements.txt -t .`   : install dependencies in current directory (or create a shared dependencies layer if small)
    `zip -r function.zip .`

4. create lambda function:

    ```sh
        aws lambda create-function \
        --function-name test-function \
        --runtime python3.10 \
        --handler lambda_function.handler \
        --zip-file fileb://function.zip \
        --role arn:aws:iam::000000000000:role/lambda-role
    ```

5. trigger on push to s3
    - create config.json
    - attach to lambda

        ```sh
        aws lambda update-function-configuration \
        --function-name test-function \
        --configuration-parameters file://configuration.json
        ```

        or

        ```sh
        aws s3api put-bucket-notification-configuration \
        --bucket my-bucket \
        --notification-configuration file://notification.json
        ```

## notes

execution time max 15 minutes
ephemeral filesystem - i.e. no persistent storage
stateless execution - i.e. no persistent state
memory 128 MB to 10 GB

## create and attach layeres

```sh
    aws lambda publish-layer-version \
    --layer-name python-deps \
    --zip-file fileb://layer.zip
```

attach layer to function:

```sh
    aws lambda update-function-configuration \
    --function-name test-function \
    --layers arn:aws:lambda:us-east-1:000000000000:layer:python-deps:1
```

## output

```json
{
    "FunctionName": "s3-listener",
    "FunctionArn": "arn:aws:lambda:us-east-1:000000000000:function:s3-listener",
    "Runtime": "python3.10",
    "Role": "arn:aws:iam::000000000000:role/lambda-role",
    "Handler": "lambda_function.handler",
    "CodeSize": 324,
    "Description": "",
    "Timeout": 3,
    "MemorySize": 128,
    "LastModified": "2026-03-05T10:43:01.565836+0000",
    "CodeSha256": "aiN4sk4ElaFlaHETDrkSdgnArzAEe4e8KVLCQrGQ/Vg=",
    "Version": "$LATEST",
    "TracingConfig": {
        "Mode": "PassThrough"
    },
    "RevisionId": "36abb50c-6a35-453f-9a0d-687a1202e994",
    "State": "Pending",
    "StateReason": "The function is being created.",
    "StateReasonCode": "Creating",
    "PackageType": "Zip",
    "Architectures": [
        "x86_64"
    ],
    "EphemeralStorage": {
        "Size": 512
    },
    "SnapStart": {
        "ApplyOn": "None",
        "OptimizationStatus": "Off"
    },
    "RuntimeVersionConfig": {
        "RuntimeVersionArn": "arn:aws:lambda:us-east-1::runtime:8eeff65f6809a3ce81507fe733fe09b835899b99481ba22fd75b5a7338290ec1"
    },
    "LoggingConfig": {
        "LogFormat": "Text",
        "LogGroup": "/aws/lambda/s3-listener"
    }
}
```

## config options

LambdaFunctionConfigurations

arn: aws:lambda:us-east-1:000000000000:function:s3-listener
events: ["s3:ObjectCreated:*", "s3:ObjectRemoved:*", "s3:ObjectAccessed:*"]

## role configs

- Action: sts:AssumeRole
- Resource: arn:aws:iam::000000000000:role/lambda-role

## STS

security token service

- actions:
    sts:AssumeRole
    sts:GetCallerIdentity
    sts:DecodeAuthorizationMessage
    sts:GetFederationToken
etc

- AWS services such as Lambda, ECS, and EC2 do not store credentials. They assume roles using STS to obtain temporary credentials.

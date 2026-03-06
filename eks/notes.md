# EKS/SNS/SQS

## setup - sns/sqs

- create sns/sqs:
    `aws sns create-topic --name test-topic`
    `{
        "TopicArn": "arn:aws:sns:us-east-1:000000000000:test-topic"
    }`

- create sqs:
    `aws sqs create-queue --queue-name test-queue`
    `{
        "QueueUrl": "https://sqs.us-east-1.amazonaws.com/000000000000/test-queue"
    }`

  - get url
        `aws sqs get-queue-url --queue-name test-queue`
    `{
        "QueueUrl": "<http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/test-queue>"
    }`

  - get arn:
    `aws sqs get-queue-attributes --queue-url <http://localhost:4566/000000000000/test-queue> --attribute-names QueueArn`
        {
            "Attributes": {
                "QueueArn": "arn:aws:sqs:us-east-1:000000000000:test-queue"
            }
        }

- subscribe sqs to sns:
    `aws sns subscribe --topic-arn arn:aws:sns:us-east-1:000000000000:test-topic --protocol sqs --notification-endpoint https://sqs.us-east-1.amazonaws.com/000000000000/test-queue`
    `{
        "SubscriptionArn": "arn:aws:sns:us-east-1:000000000000:test-topic:411b0d19-3aae-4cc3-9de5-c2da45b6b2c1"
    }`

- add sqs policy to allow sns to send
    `aws sqs set-queue-attributes --queue-url <http://localhost:4566/000000000000/test-queue> --attributes Policy="$(Get-Content policy.json -Raw)"`

## setup eks

control plane is mana
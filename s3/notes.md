# S3

## setup

- create: aws s3 mb s3://data
- commands: aws s3 <operation> <source> <destination>
  - cp: copy
  - mv: move
  - rm: remove
  - ls: list
  - sync: sync

## policy

"s3:GetObject"
"s3:PutObject"
"s3:DeleteObject"
"s3:ListBucket"
"s3:*"

- specific entties

arn:aws:s3:::bucket-name
arn:aws:s3:::bucket-name/*

## Evaluation Order

1 Explicit Deny
2 Explicit Allow
3 Default Deny

## Conditions

aws:SourceIp : IP address
aws:SecureTransport : whether the request was made using HTTPS
s3:prefix : prefix of the object key
s3:ExistingObjectTag : tag of the existing object
s3:x-amz-server-side-encryption : server-side encryption

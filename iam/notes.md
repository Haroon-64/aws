# IAM

## setup users

- > endpoint-url is not required if AWS CLI is configured with the correct endpoint
- aws --endpoint-url=<http://localhost:4566> iam create-user --user-name test

create policy

- aws iam create-policy --policy-name test-policy --policy-document file://policy.json

```json
    {
  "Version": "2012-10-17",  // general version for IAM policies
  "Statement": [
    {
      "Effect": "Allow" | "Deny",
      "Action": "service:action" or ["service:action", ...],  // Specific AWS API actions (like s3:GetObject or dynamodb:PutItem)
      "Resource": "arn-of-resource" or ["arn1", "arn2"],  // ARN(s) of the resource(s) the policy applies to
      "Condition": { ... }  // optional, restricts when the action is allowed (like IP address, time, MFA).
    }
  ]
}
```

attach to user

- aws iam attach-user-policy --user-name test --policy-arn arn:aws:iam::000000000000:policy/test-policy

list policies

- aws iam list-policies

## definitions

- ARN - Amazon Resource Name
- Policy - JSON document that defines permissions of a user, group, or roleW
- permission boundary - maximum permissions that can be granted to a user, group, or role
  - A user policy allows s3:*, but boundary allows only s3:GetObject → user can only read objects
-

## changes in actual aws

- Persistence: Users, policies, and roles exist across regions/accounts.
- Security enforcement: MFA, temporary credentials, session expiration, and cross-account roles are enforced.
- Limits: AWS imposes account/user limits and rate throttling.
- Organization: Paths and roles are used to structure large team.
- Monitoring: CloudTrail logs all IAM actions.
- Permissions boundaries: Real AWS enforces boundaries; LocalStack only mocks them.


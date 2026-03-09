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

## EKS

control plane is managed by aws
    - provision and matain master nodes
    - install  api server, schedular,controll manager, etcd
    - scale and backups

user controls only
    - worker nodes
    - install applications
    - scaling

Woker nodes:

- self managed  -> provision EC2 instances as workers
  - install kubelet, proxy, container runtime, and register to control plane
  - manage scaling and updates
- managed node groups -> aws manages worker nodes
  - uses eks optimized images
  - manage lifecycle using aws api
  - part of auto scaling groups
  - updates
- fargate -> serverless
  - no config of workers/ec2
  - create on demand optimaly
  - better scale with price per use

## creation

- > EKS

- name and k8s version
- IAM role with policies such as manage nodes, secrets, storage
- select VPC and subnet
- define secuirity group for managing traffic

- > Nodes

- create node group
- select instance type
- min/max/desired count
- cluster to connect to

- > connect to cluster

- `kubectl config set-cluster <cluster-name> --server=<api-server-url> --certificate-authority=<ca-cert-path>`

- > create cluster

- console
- eksctl
- IaC

`eksctl.exe create cluster -n test-cluster --nodegroup-name test-group --node-type t2.micro --nodes 2`

for localstack

```sh
    $env:AWS_EKS_ENDPOINT="http://localhost.localstack.cloud:4566"
    $env:AWS_EC2_ENDPOINT="http://localhost.localstack.cloud:4566"
    $env:AWS_IAM_ENDPOINT="http://localhost.localstack.cloud:4566"
    $env:AWS_STS_ENDPOINT="http://localhost.localstack.cloud:4566"
    $env:AWS_CLOUDFORMATION_ENDPOINT="http://localhost.localstack.cloud:4566"
    $env:AWS_ELB_ENDPOINT="http://localhost.localstack.cloud:4566"
    $env:AWS_ELBV2_ENDPOINT="http://localhost.localstack.cloud:4566"
```

- > without eksctl

- create role
- attach policy (control plane management)
    `aws iam attach-role-policy  --role-name EKSClusterRole  --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy`

- VPC and networking

- create eks cluster
`aws eks create-cluster --name <> --role-arn <> --resource-vpc-config <>`

- node IAM

AmazonEKSWorkerNodePolicy
AmazonEC2ContainerRegistryReadOnly
AmazonEKS_CNI_Policy

- create node group

 ```sh
     aws eks create-nodegroup --cluster-name <> --nodegroup-name <> --node-role <arn:aws:iam::<account-id>:role/EKSWorkerNodeRole> --subnets <> --scaling-config minSize=1 maxSize=3 desiredSize=2
```

- config kubectl
    `aws eks update-kubeconfig --name test-cluster`

## deployment

- create and push image to ecr
  - `docker build -t fastapi-sns .`
  - `aws ecr create-repository --repository-name fastapi-sns`
- auth docker
  - `aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 000000000000.dkr.ecr.us-east-1.localhost.localstack.cloud:4566`
- tag       `docker tag fastapi-sns:1.0 123456789012.dkr.ecr.us-east-1.amazonaws.com/fastapi-sns:1.0`
- push `docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/fastapi-sns:1.0`

- create deployment.yml, and apply `kubectl apply -f deployment.yaml`
- expose app via service.yml, and apply `kubectl apply -f service.yaml`

- update the image: `kubectl set image deployment/fastapi-publisher fastapi=ECR_URI:2.0`

## notes

deployement `automountServiceAccountToken: false`
not needed unless:
    list pods
    detect failures
    create replacement pods

if needed:
    create service account with role and bindings

def handler(event, context):
    record = event["Records"][0]

    bucket = record["s3"]["bucket"]["name"]
    key = record["s3"]["object"]["key"]

    print("bucket:", bucket)
    print("file:", key)

    return {"statusCode": 200}

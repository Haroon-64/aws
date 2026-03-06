from fastapi import FastAPI
import boto3
import logging

app = FastAPI()
logger = logging.getLogger(__name__)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/message")
def post_message(message: str):

    try:
        sns = boto3.resource(
            "sns",
            endpoint_url="http://host.docker.internal:4566",
            aws_access_key_id="test",
            aws_secret_access_key="test",
            region_name="us-east-1",
        )
        sns.Topic("arn:aws:sns:us-east-1:000000000000:test-topic").publish(
            Message=message
        )
    except Exception as e:
        logger.error(e)
        return {"error": str(e)}

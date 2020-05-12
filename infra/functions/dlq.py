import os
import boto3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('dlq')

sqs = boto3.client('sqs')

QUEUE_URL = os.environ['QUEUE_URL']

def handler(event, context):
    for record in event['Records']:
        logger.info(record)
        sqs.delete_message(
            QueueUrl=QUEUE_URL,
            ReceiptHandle=record['receiptHandle'],
        )
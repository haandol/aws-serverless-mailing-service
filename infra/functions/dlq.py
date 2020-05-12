import os
import boto3
import logging

logger = logging.getLogger('dead-letter-queue')
logger.setLevel(logging.INFO)

sqs = boto3.client('sqs')

QUEUE_URL = os.environ['QUEUE_URL']


def handler(event, context):
    for record in event['Records']:
        logger.info(record)
        sqs.delete_message(
            QueueUrl=QUEUE_URL,
            ReceiptHandle=record['receiptHandle'],
        )
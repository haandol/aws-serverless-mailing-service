import os
import boto3
import logging

logger = logging.getLogger('dead-letter-queue')

sqs = boto3.client('sqs')

QUEUE_URL = os.environ['QUEUE_URL']


def handler(event, context):
    logger.setLevel(logging.INFO)
    for record in event['Records']:
        logger.info(record)
        sqs.delete_message(
            QueueUrl=QUEUE_URL,
            ReceiptHandle=record['receiptHandle'],
        )
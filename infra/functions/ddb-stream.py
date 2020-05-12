import os
import boto3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('ddb-stream')

sqs = boto3.client('sqs')

QUEUE_URL = os.environ['QUEUE_URL']


def handler(event, context):
    entries = []
    for record in event['Records']:
        if 'INSERT' != record['eventName']:
            continue
        
        logger.info(record)
        new_id = record['dynamodb']['NewImage']['id']['S']
        email = record['dynamodb']['NewImage']['email']['S']
        first_name = record['dynamodb']['NewImage']['first_name']['S']
        last_name = record['dynamodb']['NewImage']['last_name']['S']
        entries.append({
            'Id': new_id,
            'MessageBody': email,
            'MessageAttributes': {
                'FirstName': {
                    'StringValue': first_name,
                    'DataType': 'String',
                },
                'LastName': {
                    'StringValue': last_name,
                    'DataType': 'String',
                },
            },
        })

    if entries:
        logger.info(f'send {len(entries)} messages to SQS...')
        response = sqs.send_message_batch(
            QueueUrl=QUEUE_URL,
            Entries=entries
        )
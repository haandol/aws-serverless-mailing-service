import os
import boto3
import logging

logger = logging.getLogger('ddb-stream')
logger.setLevel(logging.INFO)

sqs = boto3.client('sqs')

MAIL_QUEUE_URL = os.environ['MAIL_QUEUE_URL']


def handler(event, context):
    mail_entries = []
    sns_entries = []
    for record in event['Records']:
        if 'INSERT' != record['eventName']:
            continue
        
        logger.info(record)
        new_id = record['dynamodb']['NewImage']['id']['S']
        event_type = record['dynamodb']['NewImage']['event_type']['S']
        email = record['dynamodb']['NewImage']['email']['S']
        first_name = record['dynamodb']['NewImage']['first_name']['S']
        last_name = record['dynamodb']['NewImage']['last_name']['S']

        entry = {
            'Id': new_id,
            'MessageBody': email,
            'MessageAttributes': {
                'EventType': {
                    'StringValue': event_type,
                    'DataType': 'String',
                },
                'FirstName': {
                    'StringValue': first_name,
                    'DataType': 'String',
                },
                'LastName': {
                    'StringValue': last_name,
                    'DataType': 'String',
                },
            },
        }

        if event_type == 'mail':
            mail_entries.append(entry)
        elif event_type == 'sns':
            sns_entries.append(entry)

    if mail_entries:
        logger.info(f'send {len(mail_entries)} messages to SQS...')
        response = sqs.send_message_batch(
            QueueUrl=MAIL_QUEUE_URL,
            Entries=mail_entries
        )
        logger.info(response)

    if sns_entries:
        logger.info(f'send {len(sns_entries)} messages to SNS...')
        # TODO: implement for push queue 
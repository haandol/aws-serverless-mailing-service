import os
import boto3
import logging
from datetime import datetime
from botocore.exceptions import ClientError

logger = logging.getLogger('mail')
logger.setLevel(logging.INFO)

DDB_NAME = 'mailbox'

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DDB_NAME)


def handler(records):
    with table.batch_writer() as batch:
        for record in records:
            batch.put_item(Item=record)
            logger.info(record)


if __name__ == '__main__':
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    records = [
        {
            'id': now + 'dongkly',
            'email': 'dongkyl@amazon.com',
            'event_type': 'mail',
            'first_name': 'DongGyun',
            'last_name': 'Lee',
        },
        {
            'id': now + 'ldg55d',
            'email': 'ldg55d@gmail.com',
            'event_type': 'mail',
            'first_name': 'Vincent',
            'last_name': 'Lee',
        },
        {
            'id': now + 'kwonyul',
            'email': 'kwonyul@amazon.com',
            'event_type': 'mail',
            'first_name': 'KwonYul',
            'last_name': 'Choi',
        },
    ]
    handler(records)

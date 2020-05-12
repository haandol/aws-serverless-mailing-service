import os
import boto3
import logging
from datetime import date
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('mail')

DDB_NAME = 'mailList'

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DDB_NAME)


def handler(records):
    with table.batch_writer() as batch:
        for record in records:
            batch.put_item(Item=record)
            logger.info(record)


if __name__ == '__main__':
    today = date.today().strftime('%Y%m%d')
    records = [
        {
            'id': today + 'dongkly',
            'email': 'dongkyl@amazon.com',
            'first_name': 'DongGyun',
            'last_name': 'Lee',
        },
        {
            'id': today + 'ldg55d',
            'email': 'ldg55d@gmail.com',
            'first_name': 'Vincent',
            'last_name': 'Lee',
        },
    ]
    handler(records)
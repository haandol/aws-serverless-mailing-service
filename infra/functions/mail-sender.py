import os
import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger('mail-sender')
logger.setLevel(logging.INFO)

sqs = boto3.client('sqs')
ses = boto3.client('ses', region_name='us-east-1')

QUEUE_URL = os.environ['QUEUE_URL']

CHARSET = 'UTF-8'
BODY_HTML = '''<html>
<head></head>
<body>
  <h1>For {} {} Test</h1>
  <p>This email was sent with
    <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
    <a href='https://aws.amazon.com/sdk-for-python/'>
      AWS SDK for Python (Boto)</a>.</p>
</body>
</html>
'''

SENDER = "DongGyun Lee <dongkyl@amazon.com>"

SUBJECT = "Amazon SES Test (SDK for Python)"

BODY_TEXT = ("For {} {} Test\r\n"
             "This email was sent with Amazon SES using the "
             "AWS SDK for Python (Boto)."
             )


def handler(event, context):
    failed_records = []
    for record in event['Records']:
        logger.info(record)
        email = record['body']
        msg_attr = record['messageAttributes']
        first_name = msg_attr['FirstName']['stringValue']
        last_name = msg_attr['LastName']['stringValue']
        try:
            response = ses.send_email(
                Destination={
                    'ToAddresses': [email],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': BODY_HTML.format(first_name, last_name),
                        },
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT.format(first_name, last_name),
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': SUBJECT,
                    },
                },
                Source=SENDER,
            )
        except ClientError as e:
            logger.error(e.response['Error']['Message'])
            failed_records.append(record)
        else:
            logger.info("Email sent! Message ID:"),
            logger.info(response['MessageId'])
            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=record['receiptHandle'],
            )

    if failed_records:
        logger.error(failed_records)
        raise RuntimeError(f'{len(failed_records)} of records are failed to send.')
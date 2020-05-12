import os
import boto3
from botocore.exceptions import ClientError

sqs = boto3.client('sqs')
ses = boto3.client('ses', region_name='us-east-1')

QUEUE_URL = os.environ['QUEUE_URL']

CHARSET = 'UTF-8'
BODY_HTML = '''<html>
<head></head>
<body>
  <h1>Amazon SES Test (SDK for Python)</h1>
  <p>This email was sent with
    <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
    <a href='https://aws.amazon.com/sdk-for-python/'>
      AWS SDK for Python (Boto)</a>.</p>
</body>
</html>
'''

SENDER = "DongGyun Lee <dongkyl@amazon.com>"

SUBJECT = "Amazon SES Test (SDK for Python)"

BODY_TEXT = ("Amazon SES Test (Python)\r\n"
             "This email was sent with Amazon SES using the "
             "AWS SDK for Python (Boto)."
             )


def handler(event, context):
    for record in event['Records']:
        email = record['body']
        try:
            response = ses.send_email(
                Destination={
                    'ToAddresses': [email],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': BODY_HTML,
                        },
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT,
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
            print(e.response['Error']['Message'])
            raise e
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])
            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=record['receiptHandle'],
            )
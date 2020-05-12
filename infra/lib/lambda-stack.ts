import * as path from 'path';
import * as cdk from '@aws-cdk/core';
import * as iam from '@aws-cdk/aws-iam';
import * as sqs from '@aws-cdk/aws-sqs';
import * as lambda from '@aws-cdk/aws-lambda';
import * as dynamodb from '@aws-cdk/aws-dynamodb';
import { DynamoEventSource, SqsEventSource } from '@aws-cdk/aws-lambda-event-sources'

interface Props extends cdk.StackProps {
  queue: sqs.Queue;
  dlq: sqs.Queue;
  table: dynamodb.Table;
}

export class LambdaStack extends cdk.Stack {
  public readonly ddbStreamFunction: lambda.Function;
  public readonly mailSenderFunction: lambda.Function;
  public readonly dlqFunction: lambda.Function;

  constructor(scope: cdk.Construct, id: string, props: Props) {
    super(scope, id, props);

    const ns = scope.node.tryGetContext('ns') || '';

    this.ddbStreamFunction = this.getDdbStreamFunction(ns, props);
    this.mailSenderFunction = this.getMailSenderFunction(ns, props);
    this.dlqFunction = this.getDlqFunction(ns, props);
  }

  getDdbStreamFunction(ns: string, props: Props): lambda.Function {
    const role = new iam.Role(this, `DdbStreamFnExecutionRole${ns}`, {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
      managedPolicies: [
        { managedPolicyArn: 'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole' },
        { managedPolicyArn: 'arn:aws:iam::aws:policy/service-role/AWSLambdaDynamoDBExecutionRole' },
        { managedPolicyArn: 'arn:aws:iam::aws:policy/AmazonSQSFullAccess' },
        { managedPolicyArn: 'arn:aws:iam::aws:policy/AmazonS3FullAccess' },
      ]
    });
    const fn = new lambda.Function(this, `DdbStreamFunction${ns}`, {
      runtime: lambda.Runtime.PYTHON_3_7,
      code: lambda.Code.fromAsset(path.resolve(__dirname, '.././functions')),
      description: `ddbStreamFunction`,
      handler: 'ddb-stream.handler',
      role,
      memorySize: 512,
      timeout: cdk.Duration.seconds(30),
      deadLetterQueue: props.dlq,
      deadLetterQueueEnabled: true,
      environment: {
        QUEUE_URL: props.queue.queueUrl,
      },
    });
    fn.addEventSource(new DynamoEventSource(props.table, {
      batchSize: 100,
      startingPosition: lambda.StartingPosition.LATEST,
      maxBatchingWindow: cdk.Duration.seconds(5),
    }));
    return fn;
  }

  getMailSenderFunction(ns: string, props: Props): lambda.Function {
    const role = new iam.Role(this, `SenderFnExecutionRole${ns}`, {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
      managedPolicies: [
        { managedPolicyArn: 'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole' },
        { managedPolicyArn: 'arn:aws:iam::aws:policy/service-role/AWSLambdaSQSQueueExecutionRole' },
        { managedPolicyArn: 'arn:aws:iam::aws:policy/AmazonSESFullAccess' },
      ]
    });
    const fn = new lambda.Function(this, `MailSenderFunction${ns}`, {
      runtime: lambda.Runtime.PYTHON_3_7,
      code: lambda.Code.fromAsset(path.resolve(__dirname, '.././functions')),
      description: `mailSenderFunction`,
      handler: 'mail-sender.handler',
      role,
      timeout: cdk.Duration.seconds(30),
      deadLetterQueue: props.dlq,
      deadLetterQueueEnabled: true,
      environment: {
        QUEUE_URL: props.queue.queueUrl,
      },
    });
    fn.addEventSource(new SqsEventSource(props.queue, { batchSize: 10 }));
    return fn;
  }

  getDlqFunction(ns: string, props: Props): lambda.Function {
    const role = new iam.Role(this, `DlqFnExecutionRole${ns}`, {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
      managedPolicies: [
        { managedPolicyArn: 'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole' },
        { managedPolicyArn: 'arn:aws:iam::aws:policy/service-role/AWSLambdaSQSQueueExecutionRole' },
      ],
    });
    const fn = new lambda.Function(this, `DlqFunction${ns}`, {
      runtime: lambda.Runtime.PYTHON_3_7,
      code: lambda.Code.fromAsset(path.resolve(__dirname, '.././functions')),
      description: `dlqFunction`,
      handler: 'dlq.handler',
      role,
      timeout: cdk.Duration.seconds(30),
      environment: {
        QUEUE_URL: props.dlq.queueUrl,
      },
    });
    fn.addEventSource(new SqsEventSource(props.dlq, { batchSize: 10 }));
    return fn;
  }

}

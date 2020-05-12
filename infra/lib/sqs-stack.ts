import * as cdk from '@aws-cdk/core';
import * as sqs from '@aws-cdk/aws-sqs';

export class SqsStack extends cdk.Stack {
  public readonly queue: sqs.Queue;
  public readonly dlq: sqs.Queue;
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    this.queue = new sqs.Queue(this, `MailingQueue`);
    this.dlq = new sqs.Queue(this, `DeadLetterQueue`, {
      retentionPeriod: cdk.Duration.days(1),
    });
  }
}
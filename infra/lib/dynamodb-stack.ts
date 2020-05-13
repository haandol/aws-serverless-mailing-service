import * as cdk from '@aws-cdk/core';
import * as dynamodb from '@aws-cdk/aws-dynamodb';

export class DynamodbStack extends cdk.Stack {
  public readonly table: dynamodb.Table;
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const ns = scope.node.tryGetContext('ns') || '';
    const tableName = scope.node.tryGetContext('tableName') || '';

    this.table = new dynamodb.Table(this, `${tableName}Table${ns}`, {
      tableName,
      partitionKey: {
        name: 'id',
        type: dynamodb.AttributeType.STRING
      },
      sortKey: {
        name: 'event_type',
        type: dynamodb.AttributeType.STRING,
      },
      stream: dynamodb.StreamViewType.NEW_IMAGE,
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });
  }
}

#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { DynamodbStack } from '../lib/dynamodb-stack';
import { LambdaStack } from '../lib/lambda-stack';
import { SqsStack } from '../lib/sqs-stack';

const ns = 'Beta';
const app = new cdk.App({
  context: {
    ns,
    tableName: 'mailList',
  },
});

const dynamodbStack = new DynamodbStack(app, `DynamodbStack${ns}`);

const sqsStack = new SqsStack(app, `SqsStack${ns}`);

const lambdaStack = new LambdaStack(app, `LambdaStack${ns}`, {
  queue: sqsStack.queue,
  dlq: sqsStack.dlq,
  table: dynamodbStack.table,
});
lambdaStack.addDependency(sqsStack);
lambdaStack.addDependency(dynamodbStack);

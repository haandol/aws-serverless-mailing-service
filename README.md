# Mailing Service on AWS

This repository is for tutorial of Custom Mailing Service on AWS

**Running this repository may cost you to provision AWS resources**

# Prerequisites

- awscli
- Nodejs 10.20+
- AWS Account and Locally configured AWS credential

# Installation

Install project dependencies

```bash
$ cd infra
$ npm i
```

Install cdk in global context and run `cdk init` if you did not initailize cdk yet.

```bash
$ npm i -g cdk
$ cdk init
$ cdk bootstrap
```

Deploy CDK Stacks on AWS

```bash
$ cdk deploy "*" --require-approval never
```
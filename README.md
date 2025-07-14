# 🚀 AcmeLabs Image Analyzer

Welcome to the AcmeLabs Image Analyzer project!

This project leverages GitHub Actions with AWS services to analyze images & labels them using AWS Rekognition saving the results to DynamoDB. Below are the steps to set up your environment and deploy the resources.

AWS Services Used:
- AWS CloudFormation
- AWS CloudWatch
- AWS DynamoDB
- AWS IAM
- AWS Lambda
- AWS Rekognition
- AWS S3
- AWS

GitHub Services:
- GitHub Actions
- GitHub Repositories
- GitHub Secrets
- GitHub Workflows

Languages Used:
- Bash (Inline Shell Scripts)
- YAML
- Python

## Table of Contents
1. [🌐 Setup AWS Credentials](#-setup-aws-credentials)
2. [👤 Create IAM User with Programmatic Access](#-create-iam-user-with-programmatic-access)
3. [🔑 Create IAM Policy for GitHub Actions CI/CD](#-create-iam-policy-for-github-actions-cicd)
4. [🔐 Configure GitHub Secrets](#-configure-github-secrets)
5. [🔐 Configure GitHub Secrets](#-configure-github-secrets)
6. [🔧 Modify Configuration Files](#-modify-configuration-files)
7. [🎉 Trigger the Workflow](#-trigger-the-workflow)
8. [🏁 Conclusion](#-conclusion)

## 🌐 Setup AWS Credentials

To set up AWS credentials follow these steps:

1. **AWS Account**: Ensure you have an AWS account. If not, create one at [AWS](https://aws.amazon.com/).
   
## 👤 Create IAM User
- Create an IAM user in the AWS Management Console with programmatic access.
- Example IAM username: `acmelabs_image_analyzer_github_actions_cicd_user`

1. Sign in to the [AWS Management Console](https://aws.amazon.com/console/).
2. Navigate to the IAM service.
3. Click on "Users" in the sidebar, then click on "Create user".
4. Enter a username for the new user and click on "Next" to proceed to the **Set permissions** section.
5. Click on "Next" to proceed to the "Review and create" section.
6. Click "Create user" to proceed.

## 🔑 Create Access Keys
1. Navigate to the "Security credentials" tab of your user new IAM user. 
2. Click on "Create access key" tab. 
3. Click on "Other" for the "Use case". 
4. Click on "Next" and fill out the "Description tag value" (name the secret). 
5. Click on "Create access key". 
6. Make sure to copy the Access Key ID and Secret Access Key. 
   - You will need these for your GitHub Actions Workflows.
   - Store these credentials securely, as you will not be able to view the Secret Access Key again. 🔒
   - You can also download the credentials as a CSV file for safekeeping.
7. Click "Done" to finish. 🎉


## ⚙️ Create IAM Policy for GitHub Actions CI/CD
1. Create the `acmelabs_image_analyzer_github_actions_cicd_policy` Policy:
- In the IAM console, go to "Policies" and click "Create policy".
- Switch to the "JSON" tab and paste the following policy:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AcmeLabsImageAnalyzer",
            "Effect": "Allow",
            "Action": [
                "lambda:AddPermission",
                "lambda:CreateFunction",
                "lambda:DeleteFunction",
                "lambda:GetFunction",
                "lambda:InvokeFunction",
                "lambda:ListFunctions",
                "lambda:TagResource",
                "lambda:UntagResource",
                "dynamodb:CreateTable",
                "dynamodb:GetItem",
                "dynamodb:DeleteTable",
                "dynamodb:DescribeTable",
                "dynamodb:PutItem",
                "dynamodb:Scan",
                "dynamodb:TagResource",
                "dynamodb:UntagResource",
                "s3:CreateBucket",
                "s3:GetBucketNotification",
                "s3:GetBucketTagging",
                "s3:GetObject",
                "s3:ListBucket",
                "s3:PutBucketNotification",
                "s3:PutBucketTagging",
                "s3:PutObject",
                "cloudformation:CreateChangeSet",
                "cloudformation:DeleteChangeSet",
                "cloudformation:CreateStack",
                "cloudformation:DescribeChangeSet",
                "cloudformation:DescribeStacks",
                "cloudformation:DescribeStackResources",
                "cloudformation:ExecuteChangeSet",
                "cloudformation:GetTemplate",
                "cloudformation:GetTemplateSummary",
                "cloudformation:ListStacks",
                "cloudformation:UpdateStack",
                "cloudformation:TagResource",
                "cloudformation:UntagResource",
                "iam:CreateRole",
                "iam:DeleteRole",
                "iam:DeleteRolePolicy",
                "iam:GetRole",
                "iam:GetRolePolicy",
                "iam:PassRole",
                "iam:PutRolePolicy",
                "iam:TagPolicy",
                "iam:TagRole",
                "iam:UntagPolicy",
                "iam:UntagRole"
            ],
            "Resource": [
                "arn:aws:lambda:us-east-1:047719623795:function:acmelabs_imageanalyzer_beta",
                "arn:aws:lambda:us-east-1:047719623795:function:acmelabs_imageanalyzer_prod",
                "arn:aws:dynamodb:us-east-1:047719623795:table/acmelabs_imageanalyzer_beta_results",
                "arn:aws:dynamodb:us-east-1:047719623795:table/acmelabs_imageanalyzer_prod_results",
                "arn:aws:s3:::acmelabs-lambdas",
                "arn:aws:s3:::acmelabs-lambdas/*",
                "arn:aws:s3:::acmelabs-image-analyzer",
                "arn:aws:s3:::acmelabs-image-analyzer/*",
                "arn:aws:cloudformation:us-east-1:047719623795:stack/AcmeLabsImageAnalyzerStack/*",
                "arn:aws:iam::047719623795:role/AcmeLabsImageAnalyzerLambdaExecutionRole"
            ]
        }
    ]
}
```
- Set the `AWSAccountId` to your actual AWS account ID.
- Change the function names and table names to match your project requirements.
- Change the S3 ARNs to your values.
- Change the CloudFormation stack name to your value.
- Change the IAM role name to your value.
- Click "Next" and give it a name `acmelabs_image_analyzer_github_actions_cicd_policy`.
- Click on "Create policy" to save it. 📝

2. Attach the Policy to the User:
- Go back to the IAM user you created earlier.
- Click on the "Permissions" tab, then click "Add permissions".
- Choose "Attach existing policies directly", search for `acmelabs_image_analyzer_github_actions_cicd_policy`, select it.
- Click "Next" and then "Add permissions" to attach the policy to the user. ➕

## 🔐 Configure GitHub Secrets
1. Go to your GitHub repository.
2. Navigate to `Settings` > `Secrets and variables` > `Actions`.
3. Add the following secrets:
   1. Click on the "Secrets" tab.
   2. Click on "New repository secret".
   3. Name the secrets as follows:
      - AWS_ACCESS_KEY_ID 
      - AWS_ACCOUNT_ID 
      - AWS_REGION 
      - AWS_SECRET_ACCESS_KEY 
      - BETA_DYNAMODB_TABLE_NAME 
      - BETA_LAMBDA_FUNCTION_NAME 
      - PROD_DYNAMODB_TABLE_NAME 
      - PROD_LAMBDA_FUNCTION_NAME 
      - S3_IMAGE_ANALYZER_BUCKET 
      - S3_LAMBDA_BUCKET
   4. Enter the corresponding values for each secret:
      - For example:
         - AWS_ACCESS_KEY_ID: Your IAM user's Access Key ID.
         - AWS_ACCOUNT_ID: Your AWS account ID (found in the AWS Management Console).
         - AWS_REGION: The AWS region where you want to deploy resources (e.g., us-east-1).
         - AWS_SECRET_ACCESS_KEY: Your IAM user's Secret Access Key.
         - BETA_DYNAMODB_TABLE_NAME:  acmelabs_image_analyzer_beta_results
         - BETA_LAMBDA_FUNCTION_NAME: acmelabs_image_analyzer_beta
         - PROD_DYNAMODB_TABLE_NAME: acmelabs_image_analyzer_prod_results
         - PROD_LAMBDA_FUNCTION_NAME: acmelabs_image_analyzer_prod
         - S3_IMAGE_ANALYZER_BUCKET: acmelabs-image-analyzer
         - S3_LAMBDA_BUCKET: acmelabs-lambdas
   5. Click "Add secret" to save each secret. 💾

## 🔧 Modify Configuration Files
1. Update *on_merge.yaml*
   - Set **DEPLOY_RESOURCES** flag:
     - true = Deploys resources, this needs to be true only once to deploy the resources. Should be first commit to your repository.
     - false = Uploads & processes images only. This will be the default value for subsequent commits.
     - Keep in mind, if you need to update the resources:
       1. Set this flag to true again
       2. Change the command `aws cloudformation deploy` to `aws cloudformation update-stack`
       3. Make the changes in *template.yaml* file as needed.
       4. Commit the changes to your repository.

2. Update *template.yaml*
- Modify the following parameters to your values:
```yaml
    Region:
     Type: String
     Default: us-east-1
     Description: The AWS Region where the resources will be created.

    S3LambdaBucket:
     Type: String
     Default: acmelabs-lambdas
     Description: The S3 bucket where the Lambda function packages are stored.
    
    S3ImageAnalyzerBucket:
     Type: String
     Default: acmelabs-image-analyzer
     Description: The S3 bucket for storing images to be analyzed.
    
    BetaDynamoDBTableName:
     Type: String
     Default: acmelabs_imageanalyzer_beta_results
     Description: The name of the DynamoDB table for Beta results.
    
    ProdDynamoDBTableName:
     Type: String
     Default: acmelabs_imageanalyzer_prod_results
     Description: The name of the DynamoDB table for Prod results.
    
    BetaLambdaFunctionName:
     Type: String
     Default: acmelabs_imageanalyzer_beta
     Description: The name of the Lambda function for Beta processing.
    
    ProdLambdaFunctionName:
     Type: String
     Default: acmelabs_imageanalyzer_prod
     Description: The name of the Lambda function for Prod processing.
``` 

## GitHub Repository Structure
```angular2html
├── .github
│   ├── pull_request_template.md
│   └── workflows
│       ├── on_merge.yaml
│       └── on_pull_request.yaml
├── cloudformation
│   └── template.yaml
├── images
│   ├── image1.jpg
│   └── image2.jpg
├── lambda
│   ├── beta.py
│   └── prod.py
├── .gitignore
├── LICENSE
└── README.md
```
   
## 🔄 Trigger the Workflows
To trigger the workflows, upload images to the images directory in your repository.
1. Pull requests to the main branch will trigger the workflow which will store the images to s3 under the prefix rekognition-input/beta/ 
   - This will trigger the Lambda function to analyze the images and store the results in the DynamoDB table for beta results. 
2. Merge the pull request to the main branch to trigger the workflow which will store the images to s3 under the prefix rekognition-input/prod/
  - This will trigger the Lambda function to analyze the images and store the results in the DynamoDB table for prod results.

## 🏁 Conclusion
This project is designed to help you analyze images using AWS services efficiently. If you have any questions or need further assistance, feel free to reach out.

Ensure that your AWS credentials are kept secure and not shared publicly. 🔒
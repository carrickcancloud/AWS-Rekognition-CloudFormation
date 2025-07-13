import boto3
import os
import json
import logging
from datetime import datetime, timezone
from botocore.exceptions import ClientError, BotoCoreError
from typing import Dict, Any, List

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda function to process S3 events and detect labels in images using AWS Rekognition.

    Args:
        event (Dict[str, Any]): The event data containing S3 bucket and object key.
        context (Any): The context object for the Lambda function.

    Returns:
        Dict[str, Any]: Response object containing status code and message.
    """
    logger.info("Lambda function has started.")
    logger.info(f"Received event: {json.dumps(event)}")

    # Initialize AWS clients
    rekognition = boto3.client('rekognition')
    dynamodb = boto3.resource('dynamodb')
    table_name = os.environ.get('DYNAMODB_TABLE_BETA', 'UnknownTable')
    logger.info(f"Using DynamoDB table: {table_name}")
    table = dynamodb.Table(table_name)

    for record in event.get('Records', []):
        logger.info("Processing record: %s", json.dumps(record))

        try:
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']
            logger.info(f"Extracted bucket: {bucket}, key: {key}")

            # Attempt to detect labels in the image using AWS Rekognition
            response = rekognition.detect_labels(
                Image={'S3Object': {'Bucket': bucket, 'Name': key}}
            )
            logger.info(f"Rekognition response for {key}: {json.dumps(response)}")

            # Extract labels and their confidence scores
            labels: List[Dict[str, Any]] = [{'Name': label['Name'], 'Confidence': label['Confidence']} for label in
                                            response.get('Labels', [])]
            logger.info(f"Detected labels for {key}: {labels}")

            # Prepare the item to be stored in DynamoDB
            item = {
                'filename': key,
                'labels': labels,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'branch': 'beta'
            }
            logger.info(f"Prepared DynamoDB item: {item}")

            # Attempt to store the item in DynamoDB
            table.put_item(Item=item)
            logger.info(f"Successfully stored item in DynamoDB for {key}")

        except (ClientError, BotoCoreError) as e:
            logger.error(f"Error processing {key} in bucket {bucket}: {str(e)}")
            return {
                'statusCode': 500,
                'body': json.dumps(f"Error processing {key}: {str(e)}")
            }
        except Exception as e:
            logger.error(f"Unexpected error processing {key}: {str(e)}")
            return {
                'statusCode': 500,
                'body': json.dumps(f"Unexpected error processing {key}: {str(e)}")
            }

    logger.info("Processing completed successfully.")
    return {
        'statusCode': 200,
        'body': json.dumps('Labels processed successfully')
    }

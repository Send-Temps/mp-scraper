import boto3
import json

class Util:

    #s3 config
    s3_client = boto3.client('s3')
    s3_bucket_name = None

    #DyanmoDB config
    dynamodb_resource = boto3.resource("dynamodb", region_name="us-east-1")
    dynamodb_table = None

    def __init__(self, bucket, dynamodb_table):
        self.s3_bucket_name = bucket
        self.dynamodb_table = self.dynamodb_resource.Table(dynamodb_table)

    # Reads from the given path and returns decoded text
    def read_from_s3(self, path):
        response = self.s3_client.get_object(
            Bucket=self.s3_bucket_name,
            Key=path)
        return response['Body'].read().decode('utf-8')

    #writes a dictionary (body) to S3 at the given key
    def write_to_s3(self, key, body):
        response = self.s3_client.put_object(
            Bucket=self.s3_bucket_name,
            Key=key,
            Body=bytes(json.dumps(body).encode('UTF-8')))
        return response

    def read_from_dynamodb(self, table, key):
        pass

    def write_to_dynamodb(self, table, data):
        pass

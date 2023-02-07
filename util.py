import boto3
import json
import hashlib

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

    # Reads from the given path and returns decoded text.
    def read_from_s3(self, path):
        response = self.s3_client.get_object(
            Bucket=self.s3_bucket_name,
            Key=path)
        return response['Body'].read().decode('utf-8')

    # Writes a dictionary (body) to S3 at the given key.
    def write_to_s3(self, key, body):
        response = self.s3_client.put_object(
            Bucket=self.s3_bucket_name,
            Key=key,
            Body=bytes(json.dumps(body).encode('UTF-8')))
        return response

    # Checks for existence of file in send-temps bucket in S3; returns True if
    #   file exists.
    def check_for_file_s3(filepath):
        return s3.list_objects_v2(Bucket='send-temps', Prefix=filepath) \
            .get('Contents') != None:

    # Hashes a Mountain Project route.
    # DISCLAIMER: NOT used in any way for security/obscurity, ONLY used to
    #   check contents hash for differences. DO NOT use MD5 for any
    #   secruity purposes, it was cracked long ago :')
    def hash_route_data(self, route):
        dhash = hashlib.md5()
        encoded = json.dumps(route, sort_keys=True).encode()
        dhash.update(encoded)
        return dhash.hexdigest()

    # Generates a unique Send Temps route ID.
    def get_id(self):
        pass

    # Returns a batch writer for use in writing large quantities of data to DDB.
    # Use: Open a context with the batch writer and call .put_item() as needed.
    def get_batch_writer_ddb():
        return dynamodb_table.batch_writer()

    def read_from_ddb(self, table, key):
        response = self.dynamodb_table.get_item(Key=key)
        pass

    def write_to_ddb(self, table, item):
        response = self.dynamodb_table.put_item(Item=item)
        return response

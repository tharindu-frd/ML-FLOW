import yaml
import subprocess
import os
from from_root import from_root
import json
import mlflow.sagemaker as mfs


def read_config(config_path):
       with open(config_path) as config_file:
              content = yaml.safe_load(config_file)
       return content


def upload(s3_bucket_name=None,mlruns_dir=None):
       try:
              output = subprocess.run(["aws","s3","sync","{}".format(mlruns_dir),
                                       "s3://{}".format(s3_bucket_name)],
                                       stdout= subprocess.PIPE,
                                       encoding='utf-8'
                                       )
              
              print('\nSaved to bucket: ', s3_bucket_name)
              return f"Done Uploading :{output.stdout}"
       except Exception as e:
              return f"Error occured while uploading: {e.__str__()}"
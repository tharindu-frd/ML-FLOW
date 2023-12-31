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



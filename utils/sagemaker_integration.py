import boto3
import mlflow.sagemaker as mfs
import json
import subprocess



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
       


def deploy_model_aws_sagemaker(config=None):
       try:
              app_name = config['params']['app_name']
              execution_role_arn = config['params']['execution_role_arn']
              image_ecr_url = config['params']['image_ecr_url']
              region = config['params']['region']
              s3_bucket_name = config['params']['s3_bucket_name']
              experiment_id = config['params']['experiment_id']
              run_id = config['params']['run_id']
              model_name = config['params']['model_name']


              model_uri = "s3://{}/{}/{}/artifacts/{}/".format(s3_bucket_name,experiment_id,run_id,model_name)
              mfs.deploy(app_name=app_name,
                         model_name=model_uri,
                         execution_role_arn=execution_role_arn,
                         region_name = region,
                         image_url=image_ecr_url,
                         mode = mfs.DEPLOYMENT_MODE_CREATE
                         )
              
              return "Deployment Successfully"
       
       except Exception as e:
              print(f"Error occured while uploading :{e}")




def query(input_json,config=None):

       try:
              app_name = config['params']['app_name']
              region = config['params']['region']
              client = boto3.session.Session().client("sagemaker-runtime",region)
              response = client.invoke_endpoints(
                     EndpointName = app_name,
                     Body = input_json,
                     ContentTyps='applications/json; format=pandas-split',
              )

              preds = response['Body'].read().decode("ascii")
              preds = json.loads(preds)
              return preds
       except Exception as e:
              return f"Error occurred while prediction: {e.__str__}"
       



def switching_models(config=None):
       try:

              app_name = config['params']['app_name']
              execution_role_arn = config['params']['execution_role_arn']
              image_ecr_url = config['params']['image_ecr_url']
              region = config['params']['region']
              s3_bucket_name = config['params']['s3_bucket_name']
              experiment_id = config['params']['experiment_id']
              new_run_id = config['params']['run_id']
              model_name = config['params']['model_name']
              '''
    Inside this we can make a modification:
       Go through the db  get all the run ids  , and pick the  best one based on evaluation matrices and update the config.yaml file . So whenever we execute 
              python switch_models.py   :  The best model will be deployed 

       so based on that our new_run_id wil be changed .

       To do that we have store the credentials of our data base in the config.yaml
    
    
    '''


              new_model_uri = "s3://{}/{}/{}/artifacts/{}/".format(s3_bucket_name,experiment_id,new_run_id,model_name)

              response =  mfs.deploy(app_name=app_name,
                         model_name=new_model_uri,
                         execution_role_arn=execution_role_arn,
                         region_name = region,
                         image_url=image_ecr_url,
                         mode = mfs.DEPLOYMENT_MODE_REPLACE
                         )
              

              return f"Model Successfully Changed:{new_run_id}"
       
       except Exception as e:
              print(f"Error occured during changing the model: {e.__str__()}")

       


def remove_deployed_model(config=None):
       try:
              app_name= config['params']['app_name']
              region = config['params']['region']

              mfs.delete(app_name=app_name,region_name=region)
              return f"Endpoint Successfully Deleted: {app_name}"
       
       except Exception as e:
              print(f"Error occured while deleting the model: {e.__str__()}")








'''

##### For testing 

if __name__ == "__main__":
       runs = os.path.join(from_root(),'mlruns/')
       print('Path to ml runs exists')
       status=upload(s3_bucket_name='mlops-sagemaker-35687',mlruns_dir=runs)
       print(status)

'''
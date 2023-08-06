import json
import tarfile
import datetime
import uuid

import boto3
import pymongo
import panel as pn
from IPython.core.display import HTML
import pandas as pd

# from ipyfilechooser import FileChooser
pn.extension('tabulator')
pn.extension(notifications=True)

class mlops():
    

    G_DEPLOY_TARGET = ['DATALAB', 'SF', 'SB']
    G_MANAGER_ID_DIST = {}
    G_EVALUATE_DF = None
    
   
    P_DEPLOY_TARGET = None
    P_MANGER_ID = None
    
    P_EVALUATE = None
    P_EVALUATE_DTL = None
    P_CHK = None
    P_DEPLOY_BUTTON = None
    
    
    G_STAT_MACHINE = None
    
    
    
    def __init__(self, aws_access_key_id = None, aws_secret_access_key = None): 
        pn.extension()
        
        self.G_AWS_ACCESS_KEY = aws_access_key_id
        self.G_AWS_SECRET_KEY = aws_secret_access_key
        
            
                
        self.G_SSM_MONGO_PATH = '/mlops/dev/database/mongo'
        
        
        deploy_collection = self.mongodb_connection('dev', 'depoly', self.G_AWS_ACCESS_KEY, self.G_AWS_SECRET_KEY, self.G_SSM_MONGO_PATH, '' )
        for row in deploy_collection.find({'target' : 'labcut_autogluon'}) : 
            self.G_STAT_MACHINE = row['step_function']

        model_list = self.mongodb_connection('dev', 'log', self.G_AWS_ACCESS_KEY, self.G_AWS_SECRET_KEY, self.G_SSM_MONGO_PATH, '' )


        mongo_filter  =  {'acc' : {'$ne' : None} }
        select_filter = {    '_id' : 0, 
                             'latest' : 1,
                             'train_time' : 1,
                             'script_ver' :1, 
                             'model_name' : 1,  
                             'acc' : 1, 
                             'model' : 1,
                             'root_mean_squared_error' : 1, 
                             'mean_squared_error' : 1, 
                             'mean_absolute_error' : 1,
                             'median_absolute_error' : 1, 
                             'r2' :1 
                        }
            
            
        
        
        tmp_model_list = []
        for row in model_list.find(mongo_filter, select_filter).sort([("_id", pymongo.DESCENDING)]):
            tmp_model_list.append( row )
        
        self.G_EVALUATE_DF = pd.DataFrame( tmp_model_list )
        
        
        model_user = self.mongodb_connection('dev', 'user', self.G_AWS_ACCESS_KEY, self.G_AWS_SECRET_KEY, self.G_SSM_MONGO_PATH, '' )
        for row in model_user.find({}, {'_id' : 0}):
            self.G_MANAGER_ID_DIST = row
            
        
    
    
    # aws 통합 접속 정보이다. 
    def aws_connection(self, service_name, aws_access_key_id, aws_secret_access_key, region_name = "ap-northeast-2", endpoint_url = ""):
        if service_name == 's3' : 
            if aws_access_key_id == '' or aws_secret_access_key == '': 
                cli = boto3.client('s3', region_name=region_name)
            else :
                cli = boto3.client('s3', aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key, region_name=region_name)

        if service_name == 'ssm' : 
            if aws_access_key_id == '' or aws_secret_access_key == '': 
                cli = boto3.client('ssm', endpoint_url= endpoint_url, region_name=region_name)
            else :
                cli = boto3.client('ssm', aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key, region_name=region_name)


        if service_name == 'stepfunctions' : 
            if aws_access_key_id == '' or aws_secret_access_key == '': 
                cli = boto3.client('stepfunctions', region_name=region_name)
            else :
                cli = boto3.client('stepfunctions', aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key, region_name=region_name)

        return cli   
    
    
    
    
    # ssm에서 데이터를 가지고 온다. 
    def get_ssm(self, parameter_store_path, aws_access_key_id, aws_secret_access_key, endpoint_url, region_name ):
        client =  self.aws_connection('ssm', aws_access_key_id, aws_secret_access_key, region_name, endpoint_url  )

        if type(parameter_store_path) != list :
            parameter_store_path = [parameter_store_path]

        parameter = client.get_parameters(Names = parameter_store_path, WithDecryption=True)


        # 값을 뽑아온다. 
        parameter_result = []
        if len(parameter['Parameters']) == 0:
            pass
        elif len(parameter['Parameters']) != 0:
            for token_parameter in parameter['Parameters']:
                token_data = token_parameter['Value'].replace("'", '"') 
                parameter_value = json.loads( token_data )
                parameter_result.append(parameter_value)

        if len(parameter_result) == 1:
            return parameter_result[0]
        else :
            return parameter_result
        
        
    
    
    # 몽고디비를 접속해주는 함수이다. 
    def mongodb_connection( self, environment, collection_div, aws_access_key_id, aws_secret_access_key, ssm_path, endpoint_url, region_name = 'ap-northeast-2' ) : 
        
        SSM_PATH = ssm_path.format(environment)
        CONN_INFO = self.get_ssm( SSM_PATH,  aws_access_key_id, aws_secret_access_key, endpoint_url, region_name )
        MONGODB_HOST = CONN_INFO['host']
        MONGODB_PORT = CONN_INFO['port']
        DATABASE     = CONN_INFO['db_name']
        COLLECTION   = CONN_INFO['collection'][collection_div]
        conn = pymongo.MongoClient(MONGODB_HOST)
        db = conn[DATABASE]
        collection = db[COLLECTION]


        return collection
    
    
    
    

    
    
    
    

    
    # 패널 선언 부분
    def main_display_config(self) : 
#         df = pd.DataFrame(np.random.randn(10, 4), columns=['A','B','C','D'])
        
        self.P_DEPLOY_TARGET       = pn.widgets.Select(name='배포 목적지', options = self.G_DEPLOY_TARGET ) 

        self.P_MANGER_ID           = pn.widgets.Select(name='매니저 사번', options = list(self.G_MANAGER_ID_DIST.keys()) ) 
        
        self.P_EVALUATE                 = pn.widgets.Tabulator(self.G_EVALUATE_DF,  selectable=True,hidden_columns  = ['index'],  disabled = True,  pagination='remote', page_size=10, header_filters=True)

        
        self.P_CHK                      =  pn.widgets.input.TextAreaInput( disabled = True, placeholder='배포 모델을 선택해주세요..')
        self.P_DEPLOY_BUTTON            =  pn.widgets.Button(name='배포', button_type='primary', min_height =40)
        
        
        
    

    
    G_DEPLOY_MODEL_INFO = {}

    # mlops 메인 화면이다. 
    # 해당 화면의 역할은 show_config의 들어갈 데이터를 만들어 낸다. 
    def main_display(self) :
        
        def selected_callback(obj,event):
            
            if len(self.P_EVALUATE.selection) != 0 :
#                 model_name = self.P_EVALUATE.selected_dataframe.to_dict('recode')[0]['model_name']
#                 script_ver = self.P_EVALUATE.selected_dataframe.to_dict('recode')[0]['script_ver']
                
                row_idx = self.P_EVALUATE.selection[0]
                model_name = self.G_EVALUATE_DF.loc[row_idx]['model_name']
                script_ver = self.G_EVALUATE_DF.loc[row_idx]['script_ver']
                

                self.P_CHK.value = "{0}의 {1}버전을 배포하시겠습니까?".format( model_name, str( script_ver ) )
                self.G_DEPLOY_MODEL_INFO['model_name'] = model_name
                self.G_DEPLOY_MODEL_INFO['model_version'] = int(script_ver)
                self.G_DEPLOY_MODEL_INFO['manager_id'] = self.P_MANGER_ID.value
           
           

            
        def delpoly_endpoint(event):
            client = boto3.client('stepfunctions')   
            excute_id = str(uuid.uuid1())
            

            cli = boto3.client('stepfunctions', aws_access_key_id = self.G_AWS_ACCESS_KEY, aws_secret_access_key = self.G_AWS_SECRET_KEY, region_name='ap-northeast-2')

            response = cli.start_execution(  
                                                    stateMachineArn=self.G_STAT_MACHINE,
                                                    name=excute_id, 
                                                    input= json.dumps(self.G_DEPLOY_MODEL_INFO)
                                                  )
 
            pn.state.notifications.success( '배포가 시작됩니다.')
                
            
            
    


        
        
        self.main_display_config()
        
        display(HTML('<h1>1. 배포 타겟 선택</h1>'))
        display( self.P_DEPLOY_TARGET ) 
  
        display(HTML('<h1>1. 배포자 입력 </h1>'))
        display( self.P_MANGER_ID ) 
        
        display(HTML('<h1>2. 모델 버전 선택 </h1>'))
        
        self.P_EVALUATE.link(self.P_CHK, callbacks={'selection': selected_callback})    
        display( self.P_EVALUATE )
        
        display(HTML('<h1>3. 배포버전 선택 </h1>'))
        deploy_button = pn.Row( self.P_CHK, self.P_DEPLOY_BUTTON )
        display( deploy_button )
        
        self.P_DEPLOY_BUTTON.on_click( delpoly_endpoint )
        
        

        
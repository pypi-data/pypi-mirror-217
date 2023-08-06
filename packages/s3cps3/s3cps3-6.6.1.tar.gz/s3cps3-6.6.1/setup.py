from setuptools import setup
setup(name='s3cps3',
      version='6.6.1',
      packages=['s3cps3'],
      package_data={'s3cps3':['*.xsh','*.sh']},
      install_requires=['awscli==1.16.6','boto3==1.8.6','botocore==1.11.6','urllib3==1.23','pyasn1==0.5.0','six==1.16.0','rsa==3.4.2','click==8.1.3','xonsh==0.12.2','loguru==0.5.3','awscli_plugin_endpoint==0.4'],
      scripts=['s3cps3/s32s3', 's3cps3/main.xsh', 's3cps3/commons.py', 's3cps3/listbucket.py', 's3cps3/s3bigcp.sh', 's3cps3/s3cps3.py',],
      # entry_points={
      #     'console_scripts':[
      #         's3cps3 = s3cps3.transfer:run_xsh_script',
      #     ]
      # },

      )
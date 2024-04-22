import azure.functions as func
import logging
import subprocess
import json
import re

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route='dotnetversion', methods=['GET'])
def dotnetversion(req: func.HttpRequest) -> func.HttpResponse:
   logging.info('dotnetinfo function processed a request.')

   command_to_run = ['dotnet', '--version']
   result = subprocess.run(command_to_run, capture_output=True, text=True).stdout
   response_data = {
      'result': 'success',
      'version': f'{result.rstrip()}'
   }
   response_json = json.dumps(response_data)

   return func.HttpResponse(response_json, status_code=200, mimetype='application/json')

@app.route(route='pacversion', methods=['GET'])
def pacversion(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('pacversion function processed a request.')

    command_to_run = ['pac']
    result = subprocess.run(command_to_run, capture_output=True, text=True).stdout
    match = re.search(r'Version: (.*)', result)
    response_data = {
      'result': 'success',
      'version': f'{match.group(1)}'
    }
    response_json = json.dumps(response_data)

    return func.HttpResponse(response_json, status_code=200, mimetype='application/json')

@app.route(route='pacauth', methods=['POST'])
def pacauth(req: func.HttpRequest) -> func.HttpResponse:
   logging.info('pacauth function processed a request.')

   req_body = req.get_json()
   applicationId = req_body.get('applicationId')
   clientSecret  = req_body.get('clientSecret')
   tenant = req_body.get('tenant')
   
   command_to_run = ['pac', 'auth', 'create', '--name', 'MyOrg-SPN', '--applicationId', applicationId, '--clientSecret', clientSecret, '--tenant', tenant]
   result = subprocess.run(command_to_run, capture_output=True, text=True)
   if result.returncode == 0:
      response_data = {
         'result': 'success'
      }
      response_json = json.dumps(response_data)

      return func.HttpResponse(response_json, status_code=200, mimetype='application/json')

   else:
      response_data = {
         'result': 'failed'
      }
      response_json = json.dumps(response_data)

      return func.HttpResponse(response_json, status_code=500, mimetype='application/json')
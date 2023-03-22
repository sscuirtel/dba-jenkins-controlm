import urllib3
import json
import time


### Function to call Control-M
def calling_controlm(folder):
    print("FOLDER RECEIVED INTO THE FUNCTION LAUNCHING: ", folder)
    print(urllib3.__version__)
    urllib3.disable_warnings() # disable warnings when creating unverified requests
    endpoint='https://<CTLM_ENDPOINT>/automation-api'
    token='<TOKEN>'
    ctm='IN01'
    ipAddress = "192.168.38.1"

    order_encoded_body = json.dumps({
                  "ctm": ctm,
                  "folder": folder, 
                  "variables": [
                        {
                            "varIP": ipAddress,
                        }
                    ] 
                })
    print(order_encoded_body)
    url_order = endpoint + '/run/order'
    print("Calling EndPoint: " + url_order + " to run folder")
    http_order = urllib3.PoolManager(cert_reqs='CERT_NONE')  
    #response_order = http_order.request("POST", url, headers=headers, body=order_encoded_body)
    response_order = http_order.request('POST', url_order, headers={
        'x-api-key': token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
        }, body=order_encoded_body)
    print("Respuesta Data: ", response_order.data)
    respuesta = response_order.data 
    json_respuesta = json.loads(respuesta)
    print("Respuesta Status: ", response_order.status)
   
        
    if response_order.status == 200: #Give Control-M Enterprise Manager authorization token back if folder order is successful
        print("Folder " + folder + " succesfully ordered")
        ejecucionRunID = json_respuesta['runId']
        print("RunID del proceso es :",ejecucionRunID)
        finEjecucion, wayToChoose = checkRunFolder(ejecucionRunID)
        print ("El Resultado de la ejecucion del folder ha sido: ",finEjecucion," evento a generar: ", wayToChoose)
        ### Base on wayToChoose we will generate and Event in Control-M
        getEventResult = runEventElection(wayToChoose)
        print(getEventResult)
    
    resultado = "Process finished for folder " + folder
    return (resultado)

### Function to Check Folder Execution
def checkRunFolder(ejecucionRunID):
    wayToChoose = 0
    print("RUNID TO VERIFY FOLDER EXECUTION: ", ejecucionRunID)
    urllib3.disable_warnings() # disable warnings when creating unverified requests
    endpoint='https://<CTLM_ENDPOINT>/automation-api'
    token='<TOKEN>'
    ctm='IN01'
    url_order = endpoint + '/run/status/' + ejecucionRunID
    #
    http_order = urllib3.PoolManager(cert_reqs='CERT_NONE')  
    response_getorder = http_order.request('GET', url_order, headers={
        'x-api-key': token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
        }
    )
    respuesta = response_getorder.data 
    json_respuesta = json.loads(respuesta)
    print ("Status de la ejecucion: ",json_respuesta['statuses'][0]['status'])
    folderExecution = json_respuesta['statuses'][0]['status']
    while (folderExecution == "Executing"):
        time.sleep(10)
        http_order = urllib3.PoolManager(cert_reqs='CERT_NONE')  
        response_loop_getorder = http_order.request('GET', url_order, headers={
            'x-api-key': token,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
            }
        )
        respuesta = response_loop_getorder.data 
        json_respuesta = json.loads(respuesta)
        json_takeinfo = json.loads(respuesta)
        print ("Status de la ejecucion: ",json_respuesta['statuses'][0]['status'])
        folderExecution = json_respuesta['statuses'][0]['status']

    ## Proceed to take the jobsID, JobTypes, JobNames

    if folderExecution == "Ended OK":
        jobid = []
        jobname = []
        jobtype = []
        for jobs in json_takeinfo['statuses']:
            #print(jobs['jobId'])
            jobid.append(jobs['jobId'])
            #print(jobs['name'])
            jobname.append(jobs['name'])
            #print(jobs['type'])
            jobtype.append(jobs['type'])
        ### Proceed to check the output of the executions in order to how proceed into next steps. 
        wayToChoose = checkOutputJobs(jobid,jobname,jobtype)
        print ("El resultado de la ejecucion ha sido", wayToChoose)
        return (folderExecution,wayToChoose)
    else:
        print("La ejecucion del folder ha sido fallida, resulado: ",folderExecution)
        wayToChoose = 3
        return (folderExecution,wayToChoose)


### Check Job Output order to how proceed into next steps. 
def checkOutputJobs(jobid,jobname,jobtype):
    print("Proceed to verify the output executions")
    idjob = jobid.copy()
    namejob = jobname.copy()
    typejob = jobtype.copy()
    print(idjob)
    print(namejob) 
    for myidjob in idjob:
        for myjob in typejob:
            for mynamejob in namejob:
                #print(myjob)
                #print(mynamejob)
                if mynamejob == 'dav-first-process':
                    #takenamejob = mynamejob
                    takeidjob = myidjob
                    break


    ### Taking the output. 
    urllib3.disable_warnings() # disable warnings when creating unverified requests
    endpoint='https://<CTLM_ENDPOINT>/automation-api'
    token='<TOKEN>'
    ctm='IN01'
    url_output = endpoint + '/run/job/' + takeidjob + '/output'
    #
    http_order = urllib3.PoolManager(cert_reqs='CERT_NONE')  
    #response_order = http_order.request("POST", url, headers=headers, body=order_encoded_body)
    response_getoutput = http_order.request('GET', url_output, headers={
        'x-api-key': token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
        }
    )
    output = response_getoutput.data
    output_text = output.decode('utf-8')
    print("El contenido del output ha sido: ", output_text)
    if "0% packet loss" in output_text:
        print("No hemos tenido perdida de paquetes")
        resultado = 1
    else:
        print("Habido perdida de paquetes")
        resultado = 2
    
    return(resultado)


### Run an Event in Helix in order to take "Way 1" or "Way 2" 
#### Into this script we could have two ways based on the output of the job dav-first-process.
#####    - value 1. We will generate an event called run dav-value-1.
#####    - value 2. We will generate an event called run dav-value-2.

def runEventElection(wayToChoose):
    print ("El camino que se debe de elegir es: ", wayToChoose)
    # Defining which event we are gonna to generate
    if wayToChoose == 1:
        # code to execute if x equals 1
        event = 'dav-event-for-OK'
    elif wayToChoose == 2:
        # code to execute if x equals 2
        event = 'dav-event-for-not-OK'
    elif wayToChoose == 3:
        # code to execute if x equals 3
        event = 'dav-event-for-fail-folder'
    else:
        # code to execute if x is not equal to any of the above
        event = 'dav-event-NOT-VALUE'
    print(urllib3.__version__)
    urllib3.disable_warnings() # disable warnings when creating unverified requests
    endpoint='https://<CTLM_ENDPOINT>/automation-api'
    token='<TOKEN>'
    ctm='IN01'
    
    
    addEvent_encoded_body = json.dumps({
                "name": event,
                "date": "ODAT"
                })
    url_event = endpoint + '/run/event/' + ctm
    print("Calling EndPoint: " + url_event + " to generate event: " + event)
    http_event = urllib3.PoolManager(cert_reqs='CERT_NONE')  
    response_event = http_event.request('POST', url_event, headers={
        'x-api-key': token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
        }, body=addEvent_encoded_body)
    print(response_event.data)
    print(response_event.status)
    if response_event.status == 200: #Give Control-M Enterprise Manager authorization token back if folder order is successful
        #print("Event " + event + " succesfully created")
        return("Event " + event + " succesfully created")
    else: 
        return("Event " + event + " FAILED could not be generated")


### Main process
print("Starting the script")
print("This script will interact with Helix Control-M in order to launch processes and folders")
result = calling_controlm("dav-python-jenkins")
print (result)
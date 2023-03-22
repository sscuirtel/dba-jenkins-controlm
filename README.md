# Jenkins vs Helix Control-M / OnPrem Control-M 

This is an example to see how we can directly interact with Control-M/Helix Control-M in CI/CD processes from tools like `Jenkins`, `GitLab` or `AWS CodePipeline`. \

![CTLM Swagger](https://github.com/sscuirtel/jenkins-controlm/blob/development/images/Use_Case.png "Use Case")

For this scenario we have used Jenkins as a CI/CD tool. \
For this we have a pipeline with several branches: \
	- Development. *Master \
	- Control-M

As a branch source we have used the following GitHub project (https://github.com/sscuirtel/jenkins-controlm). \
Into this repository we will find the main files of interest. 
### Jenkinsfile
	- This is where we define the phases of our CI/CD process. 
### ./jenkins/scripts/deliver-in-development.py
	- This is the script developed in python to interact with Control-M/Helix Control-M. 

The use case is as follows: 

![Use Case](https://github.com/sscuirtel/jenkins-controlm/blob/development/images/scenario.png "Scenario")

The other flow that is waiting for these events is a workflow that is scheduled on a daily basis, but will not go into execution until jenkins sends one of the events listed above.

![Event Election](https://github.com/sscuirtel/jenkins-controlm/blob/development/images/Event_election.png "Event Election")


### To use this tutorial you will need: 
[Access to a Control-M or Helix Control-M environemnt](https://se-sanb0x.us1.controlm.com/ControlM/)

The `jenkins` directory contains an example or copy of the `Jenkinsfile` and `Jenkinsfile_react` (i.e. Pipeline)
you'll be free to create yourself your examples into the `scripts` subdirectory
contains shell scripts with commands that are executed when Jenkins processes
either the "Deliver for development" or "Deploy for production" stages of your
Pipeline (depending on the branch that Jenkins builds from).

# All the pipelines will be running under docker container agent so keep in mind you will need your images deployed 

This project mainly uses the image python:3.10.7-alpine, modify your `Jenkinsfile` if it could be needed

# How to play with Helix Control-M or with your Control-M environment. 

1. Update the folder name that you would like to order from Jenkins. 
    
    result = calling_controlm("<NAME_OF_THE_FOLDER>")

2. `Endpoint of HCTLM/CTLM` 
Into the script folder edit the script deliver-in-development.py modify the following lines. 
    
    endpoint="https://<END_POINT>/automation-api" \
    token="<ENTER_YOUR_TOKEN_ID>" \
    ctm="<ENTER_NAME_OF_YOUR_HCTLM_CTLM_SERVER>" 

3. The use case of this scenario will proceed base on the result of a ping in Helix-Controlm. \
   Update the variable ipAddress \
      ipAddress = "<ENTER_AN_ACCESSIBLE_IP_ADDRES_FROM_YOUR_ENVIRONEMT>" 

## Available Scripts

In the project directory, you can run:

### `python3 ./jenkins/scripts/deliver-in-development.py`

Runs the script in development branch. 
It will interact with Helix Control-M in order to show how you can interact with HCTLM into your CI/CD process, 
ordering folder, check the execution of a folder/jobs control the output of an execution and add events in HCTLM.


# Learn

In order to get more knowledge about which actions you could perform to interact with Control-M/Helix Control-M via REST API, the Enterprise Manager exposes a swagger where you will be able to see all the actions that you can perform. 

![CTLM Swagger](https://github.com/sscuirtel/jenkins-controlm/blob/development/images/CTLM_API_Swagger.png "CTLM Swagger")

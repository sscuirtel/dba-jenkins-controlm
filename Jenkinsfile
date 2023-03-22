pipeline {
    agent {
        docker {
            image 'python:3.10.7-alpine'
            args '-u root'
        }
    }
    environment {
        CI = 'true'
    }
     stages {
        stage('Build') {
            steps {
                sh 'ls -la'
                sh 'pwd'
                sh 'python3 --version'
            }
        }
        stage('Test') {
            steps {
                sh 'echo we could do something.'
                sh 'pip install --upgrade pip'
                sh 'pip install urllib3'
            }
        }
       stage('Deliver for development') {
            when {
                branch 'development' 
            }
            steps {
                sh 'python3 ./jenkins/scripts/deliver-in-development.py'
                //sh 'docker run --user $(id -u):$(id -g) -v $(pwd)./jenkins/scripts/deliver-in-development.py:./jenkins/scripts/deliver-in-development.py my-image /bin/bash -c "./jenkins/scripts/deliver-in-development.py"'               
                input message: 'Build Ended (Click "Proceed" to finish)'
            }
        }
    }
      
}
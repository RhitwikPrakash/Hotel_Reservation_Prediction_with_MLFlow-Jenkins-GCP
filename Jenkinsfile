pipeline {   
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "vocal-tracker-466814-q0"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
        //GOOGLE_APPLICATION_CREDENTIALS = 'vocal-tracker-466814-q0-7b2c4d1908f5.json'
    }

    stages {
        stage('Cloning Github Repository to Jenkins') {
            steps {
                script {
                    echo 'Cloning Github Repository to Jenkins....'
                    checkout scmGit(
                        branches: [[name: '*/main']], 
                        extensions: [], 
                        userRemoteConfigs: [[
                            credentialsId: 'github-token', 
                            url: 'https://github.com/RhitwikPrakash/Hotel_Reservation_Prediction_with_MLFlow-Jenkins-GCP.git'
                        ]]
                    )
                }
            }
        }

        stage('Setting up our virtual environment and installing dependencies') {
            steps {
                script {
                    echo 'Setting up our virtual environment and installing dependencies.......'
                    sh '''
                        python -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install -e .
                    '''
                }
            }
        }

        stage('Building and Pushing Docker Image to GCR'){
            steps{
                withCredentials([file(credentialsId: 'gcp-key' , variable : 'vocal-tracker-466814-q0-7b2c4d1908f5.json')]){
                    script{
                        echo 'Building and Pushing Docker Image to GCR.............'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet
                        docker build -t gcr.io/${GCP_PROJECT}/ds-mlops-project:latest .
                        docker push gcr.io/${GCP_PROJECT}/ds-mlops-project:latest 

                        '''
                    }
                }
            }
        }
    }
}

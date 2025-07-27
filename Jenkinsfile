pipeline {   
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "vocal-tracker-466814-q0"
        GCLOUD_PATH = "/c/Users/Rhitwik Prakash/Downloads/google-cloud-sdk/bin"
    }

    stages {
        
        // stage('Cloning Github Repository to Jenkins') {
        //     steps {
        //         script {
        //             echo 'Cloning Github Repository to Jenkins....'
        //             checkout scmGit(
        //                 branches: [[name: '*/main']], 
        //                 extensions: [], 
        //                 userRemoteConfigs: [[
        //                     credentialsId: 'github-token', 
        //                     url: 'https://github.com/RhitwikPrakash/Hotel_Reservation_Prediction_with_MLFlow-Jenkins-GCP.git'
        //                 ]]
        //             )
        //         }
        //     }
        // }
        
        // stage('Setting up our virtual environment and installing dependencies') {
        //     steps {
        //         script {
        //             echo 'Setting up our virtual environment and installing dependencies.......'
        //             sh '''
        //                 python -m venv ${VENV_DIR}
        //                 . ${VENV_DIR}/bin/activate
        //                 pip install --upgrade pip
        //                 pip install -e .
        //             '''
        //         }
        //     }
        // }

        // stage('Building and Pushing Docker Image to GCR'){
        //     steps {
        //         withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
        //             script {
        //                 echo 'Building and Pushing Docker Image to GCR.............'
        //                 sh '''
        //                     export PATH=$PATH:${GCLOUD_PATH}
        //                     gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
        //                     gcloud config set project ${GCP_PROJECT}
        //                     gcloud auth configure-docker --quiet

        //                     cp $GOOGLE_APPLICATION_CREDENTIALS ./gcp-key.json
        //                     docker build --build-arg GCP_CREDS=gcp-key.json -t gcr.io/${GCP_PROJECT}/ds-mlops-project:latest .
        //                     rm gcp-key.json

        //                     docker push gcr.io/${GCP_PROJECT}/ds-mlops-project:latest
        //                 '''
        //             }
        //         }
        //     }
        // }
        
        stage('Deploy to Google Cloud Run') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Deploying Docker Image to Google Cloud Run...'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                        gcloud config set project ${GCP_PROJECT}

                        gcloud run deploy ds-mlops-project \
                        --image=gcr.io/${GCP_PROJECT}/ds-mlops-project:latest \
                        --platform=managed \
                        --region=us-central1 \
                        --allow-unauthenticated
                        '''
                    }
                }
            }
        }



    }
}

pipeline{   
    agent any

    environment {
        VENV_DIR = 'venv'
    }
    stages{
        stage("Cloning Github Repository to Jenkins"){
            steps{
                script{
                    echo "Cloning the repository from GitHub to Jenkins...."
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/RhitwikPrakash/Hotel_Reservation_Prediction_with_MLFlow-Jenkins-GCP.git']])
                }
            }
        }

        stage("Setting up our Virtual Environment and installing dependencies"){
            steps{
                script{
                    echo "Setting up our Virtual Environment and installing dependencies"
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }
    }
}
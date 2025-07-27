pipeline{   
    agent any

    stages{
        stage('Cloning Github Repository to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github Repository to Jenkins....'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/RhitwikPrakash/Hotel_Reservation_Prediction_with_MLFlow-Jenkins-GCP.git']])
                }
            }
        }

    }
}

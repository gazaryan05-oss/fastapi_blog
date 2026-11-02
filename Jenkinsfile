pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Getting source code'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running Pytest'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image'
            }
        }
    }
}
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'fastapi-app'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'uv sync'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'uv run pytest'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:latest .'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished!'
        }
        success {
            echo 'Build succeeded!'
        }
        failure {
            echo 'Build failed! Check console logs.'
        }
    }
}
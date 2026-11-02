pipeline {
    agent any

    environment {
        IMAGE_NAME = 'fastapi-app'

        // Расширяем PATH для всех команд и дочерних процессов Docker/UV
        PATH = "/usr/local/bin:/Applications/Docker.app/Contents/Resources/bin:/opt/homebrew/bin:${env.PATH}"

        UV_BIN = '/Library/Frameworks/Python.framework/Versions/3.11/bin/uv'

        // Переменные окружения для Pydantic Settings
        SECRET_KEY = 'test_secret_key_for_jenkins_ci'
        S3_BUCKET_NAME = 'test-s3-bucket'
        DATABASE_URL = 'postgresql+psycopg://bloguser:password@localhost:5432/test_blog'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Source code fetched successfully'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Syncing all dependencies with UV...'
                sh '${UV_BIN} sync --all-groups'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running migrations and Pytest...'
                sh '${UV_BIN} run alembic upgrade head'
                sh '${UV_BIN} run pytest'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
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
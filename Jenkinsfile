pipeline {
    agent any

    environment {
        IMAGE_NAME = 'fastapi-app'
        // Прямой путь к бинарнику uv
        UV_BIN = '/Library/Frameworks/Python.framework/Versions/3.11/bin/uv'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Source code fetched successfully'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Syncing dependencies with UV...'
                sh '${UV_BIN} sync'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running migrations and pytest...'
                // Применяем миграции к тестовой базе данных
                sh '${UV_BIN} run alembic upgrade head'
                // Запускаем тесты
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
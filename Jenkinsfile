pipeline {
    agent any

    environment {
        // Название твоего Docker-образа
        IMAGE_NAME = 'fastapi-app'
    }

    stages {

        stage('Checkout') {
            steps {
                // Jenkins сам скачивает код из Git, но здесь можно выдать сообщение
                echo 'Source code fetched successfully'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Syncing dependencies with UV...'
                // Синхронизируем виртуальное окружение через uv
                sh 'uv sync'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running Pytest...'
                // Запускаем тесты с помощью pytest через виртуальное окружение uv
                sh 'uv run pytest'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                // Собираем Docker-образ вашего FastAPI приложения
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
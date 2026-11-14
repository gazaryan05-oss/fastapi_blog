pipeline {
    agent any

    environment {
        // Твой ник на Docker Hub
        IMAGE_NAME = 'victoriagazaryan/fastapi-blog'
        
        // Переменные для тестов (фейковые, чтобы тесты не стучались в реальную БД)
        SECRET_KEY = 'test_secret_key_for_jenkins'
        S3_BUCKET_NAME = 'test-s3-bucket'
        DATABASE_URL = 'postgresql+psycopg://bloguser:password@localhost:5432/test_blog'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                echo 'Installing uv and syncing dependencies...'
                sh 'curl -LsSf https://astral.sh/uv/install.sh | sh'
                sh 'export PATH="$HOME/.cargo/bin:$PATH" && uv sync --all-groups'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running Pytest...'
                sh 'export PATH="$HOME/.cargo/bin:$PATH" && uv run pytest'
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
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed! Check logs.'
        }
    }
}
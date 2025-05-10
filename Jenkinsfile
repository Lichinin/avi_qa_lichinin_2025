pipeline {
    agent any

    environment {
        SELENOID_URL = "http://selenoid:4444/wd/hub"
        DOCKER_COMPOSE_PROJECT_NAME = "ci_build_\${BUILD_NUMBER}"
    }

    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }

        stage('Setup Docker Compose Project Name') {
            steps {
                script {
                    // Установка переменной для уникальности проекта
                    env.DOCKER_COMPOSE_PROJECT_NAME = "ci_build_${currentBuild.number}"
                    echo "DOCKER_COMPOSE_PROJECT_NAME = ${env.DOCKER_COMPOSE_PROJECT_NAME}"
                }
            }
        }

        stage('Start Selenoid') {
            steps {
                sh '''
                    DOCKER_COMPOSE_PROJECT_NAME=${DOCKER_COMPOSE_PROJECT_NAME} docker-compose up -d selenoid
                    sleep 10  # Ждём, пока Selenoid полностью стартует
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    DOCKER_COMPOSE_PROJECT_NAME=${DOCKER_COMPOSE_PROJECT_NAME} docker-compose run --rm tests
                '''
            }
        }

        stage('Stop Containers') {
            steps {
                sh '''
                    DOCKER_COMPOSE_PROJECT_NAME=${DOCKER_COMPOSE_PROJECT_NAME} docker-compose down || true
                '''
            }
        }

        stage('Publish Allure Report') {
            steps {
                allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        failure {
            mail to: 'your@email.com',
                 subject: "Failed Pipeline: ${currentBuild.fullDisplayName}",
                 body: "See ${env.BUILD_URL}"
        }
    }
}
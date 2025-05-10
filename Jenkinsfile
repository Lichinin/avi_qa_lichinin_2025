pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_PROJECT_NAME = "ci_build_${currentBuild.number}"
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
                    echo "DOCKER_COMPOSE_PROJECT_NAME = ${env.DOCKER_COMPOSE_PROJECT_NAME}"
                }
            }
        }

        stage('Start Selenoid') {
            steps {
                bat """
                    docker-compose -p %DOCKER_COMPOSE_PROJECT_NAME% up -d selenoid
                """
            }
        }

        stage('Run Tests') {
            steps {
                bat """
                    docker-compose -p %DOCKER_COMPOSE_PROJECT_NAME% run --rm tests
                """
            }
        }

        stage('Stop Containers') {
            steps {
                bat """
                    docker-compose -p %DOCKER_COMPOSE_PROJECT_NAME% down
                """
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
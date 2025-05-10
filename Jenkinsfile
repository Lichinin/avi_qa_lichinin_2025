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

        stage('Start Selenoid and Run Tests') {
            steps {
                script {
                    try {
                        sh """
                            docker-compose -p \${DOCKER_COMPOSE_PROJECT_NAME} up -d selenoid
                            sleep 10
                        """

                        sh """
                            docker-compose -p \${DOCKER_COMPOSE_PROJECT_NAME} run --rm tests
                        """
                    } finally {
                        sh """
                            docker-compose -p \${DOCKER_COMPOSE_PROJECT_NAME} down || true
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            echo 'Pipeline finished.'
        }
        failure {
            mail to: 'your@email.com',
                 subject: "Failed Pipeline: ${currentBuild.fullDisplayName}",
                 body: "See ${env.BUILD_URL}"
        }
    }
}
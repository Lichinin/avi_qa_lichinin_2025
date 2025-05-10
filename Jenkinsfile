pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_PROJECT_NAME = "ci_build_${currentBuild.number}"
        SELENOID_NETWORK = "selenoid_net"
    }

    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }

        stage('Setup Project Name') {
            steps {
                script {
                    echo "DOCKER_COMPOSE_PROJECT_NAME = ${env.DOCKER_COMPOSE_PROJECT_NAME}"
                }
            }
        }

        stage('Cleanup old networks') {
            steps {
                sh 'docker network ls | grep selenoid_net && docker network rm selenoid_net || true'
            }
        }

        stage('Create shared network') {
            steps {
                sh 'docker network create selenoid_net || true'
            }
        }

        stage('Start Selenoid') {
            steps {
                sh """
                    docker-compose -p \${DOCKER_COMPOSE_PROJECT_NAME} up -d selenoid
                    sleep 10
                """
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    try {
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
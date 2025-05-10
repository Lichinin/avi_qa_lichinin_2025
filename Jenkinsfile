pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_PROJECT_NAME = "avi_qa_lichinin_2025"
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

        stage('Start Selenoid') {
            steps {
                script {
                    try {
                        // Удалить старые контейнеры и сеть, если есть
                        sh 'docker-compose -p $DOCKER_COMPOSE_PROJECT_NAME down || true'

                        // Запуск Selenoid
                        sh """
                            docker-compose -p \$DOCKER_COMPOSE_PROJECT_NAME up -d selenoid
                            sleep 10
                            until curl -s http://localhost:4444/status | grep '"total":'; do
                                echo "Ожидаем Selenoid..."
                                sleep 5
                            done
                        """
                        // Теперь сеть будет: avi_qa_lichinin_2025_selenoid_net
                    } catch (Exception e) {
                        echo "Ошибка при запуске Selenoid: ${e}"
                        currentBuild.result = 'FAILURE'
                        throw e
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                sh 'docker-compose -p $DOCKER_COMPOSE_PROJECT_NAME run --rm tests'
            }
        }

        stage('Stop Containers') {
            steps {
                sh 'docker-compose -p $DOCKER_COMPOSE_PROJECT_NAME down || true'
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
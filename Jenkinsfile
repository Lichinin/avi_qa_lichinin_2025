pipeline {
    agent any
    
    environment {
        DOCKER_HOST = "tcp://localhost:2375"
        SELENOID_IP = "localhost"
    }

    stages {
        stage('Prepare Environment') {
            steps {
                sh '''
                # Создаем сеть если не существует
                docker network create selenoid_net || true
                
                # Скачиваем образы (можно добавить --quiet для уменьшения логов)
                docker pull aerokube/selenoid:latest
                docker pull selenoid/chrome:125.0
                docker pull selenoid/video-recorder:latest
                '''
            }
        }

        stage('Start Selenoid') {
            steps {
                sh '''
                # Запускаем Selenoid с локальным конфигом
                docker-compose -f docker-compose.yml up -d selenoid
                
                # Проверяем доступность (добавляем таймаут)
                for i in {1..10}; do
                    if curl -s http://localhost:4444/status >/dev/null; then
                        echo "Selenoid ready"
                        break
                    fi
                    sleep 3
                done
                
                # Полная проверка статуса
                curl -v http://localhost:4444/status
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                # Собираем и запускаем тесты с привязкой к локальной сети
                docker-compose -f docker-compose.yml build tests
                docker-compose -f docker-compose.yml run --rm tests
                '''
            }
        }

        stage('Allure Report') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    properties: [],
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: 'allure-results']]
                ])
            }
        }
    }

    post {
        always {
            sh '''
            # Останавливаем контейнеры с таймаутом
            docker-compose -f docker-compose.yml down --timeout 30
            docker network rm selenoid_net || true
            '''
            archiveArtifacts artifacts: '**/logs/*.log', allowEmptyArchive: true
        }
    }
}
pipeline {
    agent any
    
    environment {
        // Настройки окружения
        DOCKER_HOST = "tcp://localhost:2375"
        SELENOID_IP = "185.105.91.135"
    }

    stages {
        stage('Prepare Environment') {
            steps {
                sh '''
                # Создаем сеть если не существует
                docker network create selenoid_net || true
                
                # Скачиваем необходимые образы
                docker pull aerokube/selenoid:latest
                docker pull selenoid/chrome:125.0
                docker pull selenoid/video-recorder:latest
                '''
            }
        }

        stage('Start Selenoid') {
            steps {
                sh '''
                # Запускаем Selenoid в фоновом режиме
                docker-compose -f docker-compose.yml up -d selenoid
                
                # Ждем инициализации
                sleep 15
                
                # Проверяем статус
                curl -v http://${SELENOID_IP}:4444/status
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                # Собираем образ с тестами
                docker-compose -f docker-compose.yml build tests
                
                # Запускаем тесты
                docker-compose -f docker-compose.yml run --rm tests
                '''
            }
        }

        stage('Allure Report') {
            steps {
                // Собираем отчеты Allure
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
            # Останавливаем контейнеры и чистим ресурсы
            docker-compose -f docker-compose.yml down
            docker network rm selenoid_net || true
            '''
            
            // Архивируем логи
            archiveArtifacts artifacts: '**/logs/*.log', allowEmptyArchive: true
        }
        
        success {
            // Уведомление об успешном выполнении
            slackSend(color: 'good', message: "Build ${BUILD_NUMBER} succeeded")
        }
        
        failure {
            // Уведомление о неудаче
            slackSend(color: 'danger', message: "Build ${BUILD_NUMBER} failed")
        }
    }
}
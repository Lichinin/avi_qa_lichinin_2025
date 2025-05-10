pipeline {
    agent any
    
    environment {
        DOCKER_HOST = "tcp://localhost:2375"
        SELENOID_IP = "localhost"
    }

    stages {
        stage('Prepare Environment') {
            steps {
                bat '''
                @echo off
                docker network create selenoid_net || echo Network already exists
                docker pull aerokube/selenoid:latest
                docker pull selenoid/chrome:125.0
                docker pull selenoid/video-recorder:latest
                '''
            }
        }

        stage('Start Selenoid') {
            steps {
                bat '''
                @echo off
                docker-compose -f docker-compose.yml up -d selenoid
                
                :: Проверка доступности с таймаутом
                for /l %%x in (1, 1, 10) do (
                  curl -s http://localhost:4444/status >nul && (
                    echo Selenoid ready
                    goto :ready
                  ) || (
                    timeout /t 3 >nul
                  )
                )
                :ready
                curl -v http://localhost:4444/status
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                @echo off
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
            bat '''
            @echo off
            docker-compose -f docker-compose.yml down --timeout 30
            docker network rm selenoid_net || echo Network removal failed
            '''
            archiveArtifacts artifacts: '**\\logs\\*.log', allowEmptyArchive: true
        }
    }
}
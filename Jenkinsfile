pipeline {
    agent any
    
    stages {
        stage('Build Test Image') {
            steps {
                script {
                    docker.build("python-web-tests", ".")
                }
            }
        }
        
        stage('Pull Selenoid & Browser') {
            steps {
                script {
                    docker.image('aerokube/selenoid:latest').pull()
                    docker.image('selenoid/chrome:125.0').pull()
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    // Запускаем Selenoid
                    def selenoid = docker.image('aerokube/selenoid:latest').run(
                        '-p 4444:4444 -v /var/run/docker.sock:/var/run/docker.sock --name selenoid'
                    )
                    
                    // Даем время на запуск
                    sleep 30
                    
                    try {
                        // Запускаем тесты, связывая контейнеры
                        docker.image('python-web-tests').inside(
                            "--link selenoid:selenoid -e SELENOID_URL='http://selenoid:4444/wd/hub'"
                        ) {
                            sh 'pytest'
                        }
                    } finally {
                        // Останавливаем Selenoid после тестов
                        selenoid.stop()
                    }
                }
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
            script {
                // Очистка контейнеров
                sh 'docker rm -f selenoid || true'
            }
            archiveArtifacts artifacts: 'allure-results/**/*', allowEmptyArchive: true
        }
    }
}
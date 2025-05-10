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
                    // 1. Запускаем Selenoid (Windows-формат для volume)
                    def selenoid = docker.image('aerokube/selenoid:latest').run(
                        '-p 4444:4444 -v //var/run/docker.sock:/var/run/docker.sock --name selenoid'
                    )
                    
                    // 2. Ожидание запуска (Windows-команда)
                    bat 'timeout /t 30 /nobreak'
                    
                    try {
                        // 3. Запуск тестов (sh остается, так как внутри Linux-контейнера)
                        docker.image('python-web-tests').inside(
                            "--link selenoid:selenoid -e SELENOID_URL=http://selenoid:4444/wd/hub"
                        ) {
                            sh 'pytest'
                        }
                    } finally {
                        // 4. Остановка Selenoid
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
                // Очистка (Windows-команда)
                bat 'docker rm -f selenoid || echo Container removal skipped'
                archiveArtifacts artifacts: 'allure-results/**/*', allowEmptyArchive: true
            }
        }
    }
}
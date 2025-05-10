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
                        bat """
                            docker-compose -p %DOCKER_COMPOSE_PROJECT_NAME% up -d selenoid
                            ping -n 10 127.0.0.1 > nul
                        """

                        bat """
                            docker-compose -p %DOCKER_COMPOSE_PROJECT_NAME% run --rm tests
                        """
                    } finally {
                        echo "Останавливаем контейнеры..."

                        bat """
                            docker-compose -p %DOCKER_COMPOSE_PROJECT_NAME% down || exit 0
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
            script {
                def passed = 0
                def failed = 0
                def skipped = 0

                // Подсчёт по allure-results
                def files = findFiles(glob: 'allure-results/test-result-*.json')
                files.each { file ->
                    def json = readJSON file: file
                    switch(json.status) {
                        case "passed":
                            passed++
                            break
                        case "failed":
                            failed++
                            break
                        case "skipped":
                            skipped++
                            break
                    }
                }

                def buildName = currentBuild.fullDisplayName
                def buildUrl = env.BUILD_URL

                def subject = "❌ Failed Pipeline: ${buildName}"
                def htmlBody = """\
                    <html>
                    <body>
                      <h3>Сборка: ${buildName} упала</h3>
                      <p><strong>Ссылка:</strong> <a href='${buildUrl}'>${buildUrl}</a></p>
                      <h4>Результаты тестов:</h4>
                      <ul>
                        <li>✅ Пройдено: ${passed}</li>
                        <li>❌ Упало: ${failed}</li>
                        <li>⚠️ Пропущено: ${skipped}</li>
                      </ul>
                      <p>Сгенерировано автоматически через Jenkins + Allure</p>
                    </body>
                    </html>
                """.stripIndent()

                emailext (
                    to: 'lichinin.v@yandex.ru',
                    subject: subject,
                    body: htmlBody,
                    mimeType: 'text/html'
                )
            }
        }
    }
}
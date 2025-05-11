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

        stage('Setup Project Name') {
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
                    ping -n 10 127.0.0.1 > nul
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

        // ✅ Добавленный этап: Ждём, чтобы allure-results точно были готовы
        stage('Wait for Allure Results') {
            steps {
                bat 'ping -n 10 127.0.0.1 > nul'
            }
        }

        stage('Stop Containers') {
            steps {
                bat """
                    docker-compose -p %DOCKER_COMPOSE_PROJECT_NAME% down || exit 0
                """
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

                // Ищем файлы test-result-*.json
                def files = findFiles(glob: 'allure-results/test-result-*.json')

                if (files == null || files.size() == 0) {
                    echo "❌ Файлы результатов не найдены в allure-results/"
                } else {
                    files.each { file ->
                        try {
                            def json = readJSON file: file.path
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
                                default:
                                    echo "Неизвестный статус: ${json.status}"
                            }
                        } catch (Exception e) {
                            echo "Ошибка при чтении файла ${file.name}: ${e}"
                        }
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
                        <li>✅ Пройдено: ${passed ?: 0}</li>
                        <li>❌ Упало: ${failed ?: 0}</li>
                        <li>⚠️ Пропущено: ${skipped ?: 0}</li>
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
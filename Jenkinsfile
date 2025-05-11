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

        // ✅ Новый этап: Очистка старых результатов
        stage('Clean Allure Results') {
            steps {
                script {
                    bat 'powershell -Command "if (Test-Path allure-results) { Remove-Item -Recurse -Force allure-results }"'
                    bat 'mkdir allure-results'
                }
            }
        }

        stage('Setup Project Name') {
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
                        // Запуск Selenoid
                        bat """
                            docker-compose -p %DOCKER_COMPOSE_PROJECT_NAME% up -d selenoid
                            ping -n 10 127.0.0.1 > nul
                        """

                        // Запуск тестов
                        bat """
                            docker-compose -p %DOCKER_COMPOSE_PROJECT_NAME% run --rm tests
                        """

                        // Ждём, чтобы allure-results точно были готовы
                        bat 'ping -n 5 127.0.0.1 > nul'

                    } finally {
                        // Этот блок выполнится всегда — даже если тесты упали
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

                // Ищем все JSON-файлы с результатами тестов
                def files = findFiles(glob: 'allure-results/*-result.json')

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

                // ✅ Новый этап: создаём ZIP-архив с отчётом
                bat """
                    cd allure-report && powershell Compress-Archive -Path * -DestinationPath ..\\allure-report.zip -Force
                """

                // Теперь отправляем письмо с прикреплённым архивом
                emailext (
                    to: 'lichinin.v@yandex.ru',
                    subject: subject,
                    body: htmlBody,
                    mimeType: 'text/html',
                    attachmentsPattern: 'allure-report.zip'  // ✅ Прикрепляем ZIP
                )
            }
        }
    }
}
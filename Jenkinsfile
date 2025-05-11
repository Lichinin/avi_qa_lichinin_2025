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

        stage('Clean Allure Results') {
            steps {
                bat 'powershell -Command "if (Test-Path allure-results) { Remove-Item -Recurse -Force allure-results }"'
                bat 'mkdir allure-results'
            }
        }

        stage('Start Selenoid and Run Tests') {
            steps {
                script {
                    try {
                        echo "Запускаю Selenoid..."
                        bat """
                            docker-compose -p %DOCKER_COMPOSE_PROJECT_NAME% up -d selenoid
                            ping -n 10 127.0.0.1 > nul
                        """
                        echo "Запускаю тесты..."
                        bat """
                            docker-compose -p %DOCKER_COMPOSE_PROJECT_NAME% run --rm tests
                        """

                        bat 'ping -n 5 127.0.0.1 > nul'

                    } finally {
                        echo "Останавливаю контейнеры..."
                        bat """
                            docker-compose -p %DOCKER_COMPOSE_PROJECT_NAME% down || exit 0
                        """
                    }
                }
            }
        }

        stage('Generate Allure Report Archive') {
            steps {
                bat 'powershell Compress-Archive -Path allure-report\\* -DestinationPath allure-report.zip -Force'
            }
        }
    }

    post {
        always {
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]

            script {
                def passed = 0
                def failed = 0
                def skipped = 0

                def files = findFiles(glob: 'allure-results/*-result.json')

                if (files == null || files.size() == 0) {
                    echo "❌ Файлы результатов не найдены"
                } else {
                    files.each { file ->
                        try {
                            def json = readJSON file: file.path
                            switch(json.status) {
                                case "passed": passed++; break
                                case "failed": failed++; break
                                case "skipped": skipped++; break
                                default: echo "Неизвестный статус: ${json.status}"
                            }
                        } catch (Exception e) {
                            echo "Ошибка при чтении файла ${file.name}: ${e}"
                        }
                    }
                }

                def buildName = currentBuild.fullDisplayName
                def buildUrl = env.BUILD_URL

                def subject = "📊 Результаты сборки: ${buildName}"
                def htmlBody = """\
                    <html>
                    <body>
                      <h3>Сборка: ${buildName}</h3>
                      <p><strong>Статус:</strong> ${currentBuild.currentResult}</p>
                      <p><strong>Ссылка:</strong> <a href='${buildUrl}'>${buildUrl}</a></p>

                      <h4>Результаты тестов</h4>
                      <ul>
                        <li>✅ Пройдено: ${passed ?: 0}</li>
                        <li>❌ Упало: ${failed ?: 0}</li>
                        <li>⚠️ Пропущено: ${skipped ?: 0}</li>
                      </ul>

                      <p>Сгенерировано автоматически через Jenkins + Allure</p>
                    </body>
                    </html>
                """.stripIndent()

                def hasAttachment = fileExists('allure-report.zip')
                def attachmentPath = hasAttachment ? 'allure-report.zip' : null

                if (!hasAttachment) {
                    echo "🚫 Архив не найден, отправляем без вложения"
                }

                emailext (
                    to: 'lichinin.v@yandex.ru',
                    subject: subject,
                    body: htmlBody,
                    mimeType: 'text/html',
                    attachLog: true,
                    attachmentsPattern: attachmentPath
                )
            }
        }
    }
}
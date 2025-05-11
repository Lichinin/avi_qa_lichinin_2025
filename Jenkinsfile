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
                        bat """
                            docker-compose -p %DOCKER_COMPOSE_PROJECT_NAME% up -d selenoid
                        """

                        bat """
                            docker-compose -p %DOCKER_COMPOSE_PROJECT_NAME% run --rm tests
                        """

                        bat 'ping -n 5 127.0.0.1 > nul'

                    } finally {
                        echo "Останавливаем контейнеры..."
                        bat """
                            docker-compose -p %DOCKER_COMPOSE_PROJECT_NAME% down || exit 0
                        """
                    }
                }
            }
        }

        // ✅ Новый этап: Создание и переименование ZIP-архива
        stage('Generate Renamed Report Archive') {
            steps {
                script {
                    try {
                        // Удаляем старые архивы, если есть
                        bat 'if exist allure-report.zip del /q allure-report.zip'
                        bat 'if exist allure-report.zip_renamed del /q allure-report.zip_renamed'

                        // Создаём новый архив
                        bat 'powershell Compress-Archive -Path allure-report\\* -DestinationPath allure-report.zip -Force'

                        // Переименовываем его в allure-report.zip_renamed
                        bat 'move allure-report.zip allure-report.zip_renamed'

                        echo "📦 Архив успешно создан и переименован: allure-report.zip_renamed"

                    } catch (Exception e) {
                        echo "⚠️ Не удалось создать архив: ${e}"
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

                def files = findFiles(glob: 'allure-results/*-result.json')

                if (files == null || files.size() == 0) {
                    echo "❌ Файлы результатов не найдены"
                } else {
                    files.each { file ->
                        try {
                            def json = readJSON(file: file.path)
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
                def buildStatus = currentBuild.currentResult

                def subject = "❌ Failed Pipeline: ${buildName} — ${buildStatus}"
                def htmlBody = """\
                    <html>
                    <body>
                      <h3>Сборка упала: ${buildName}</h3>
                      <p><strong>Ссылка:</strong> <a href='${buildUrl}'>${buildUrl}</a></p>

                      <h4>Результаты тестов:</h4>
                      <ul>
                        <li>✅ Пройдено: ${passed ?: 0}</li>
                        <li>❌ Упало: ${failed ?: 0}</li>
                        <li>⚠️ Пропущено: ${skipped ?: 0}</li>
                      </ul>

                      <p>Лог сборки и отчет приложены</p>
                    </body>
                    </html>
                """.stripIndent()

                emailext (
                    to: 'lichinin.v@yandex.ru',
                    subject: subject,
                    body: htmlBody,
                    mimeType: 'text/html',
                    attachLog: true,
                    attachmentsPattern: 'allure-report.zip_renamed'  // ✅ Используем новое имя
                )
            }
        }
    }
}
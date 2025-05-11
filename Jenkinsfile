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
        stage('Generate Password Protected Archive') {
            steps {
                script {
                    def zipPath = "${env.WORKSPACE}\\allure-report.zip"
                    def encryptedZipPath = "${env.WORKSPACE}\\allure-report-secure.zip"
                    def archivePassword = "12345"

                    // Удаляем старые архивы, если есть
                    bat 'if exist allure-report.zip del /q allure-report.zip'
                    bat 'if exist allure-report-secure.zip del /q allure-report-secure.zip'

                    // Используем 7z для создания зашифрованного архива
                    bat """
                        C:\\Program Files\\7-Zip\\7z.exe a -tzip -p${archivePassword} -mem=AES256 ${encryptedZipPath} allure-report\\*
                    """

                    echo "🔒 Зашифрованный архив создан: ${encryptedZipPath}"
                }
            }
        }
    }

    post {
        always {
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            echo 'Pipeline finished.'

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
                def buldStatus = currentBuild.currentResult

                def subject = "Pipeline status ${buildName}: ${buldStatus}"
                def htmlBody = """\
                    <html>
                    <body>
                    <h3>Результаты сборки ${buildName}: ${buldStatus}</h3>
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

                // ✅ Защита: проверяем, существует ли архив
                def hasAttachment = fileExists('allure-report.zip')
                def attachmentPath = hasAttachment ? 'allure-report.zip' : null

                if (hasAttachment) {
                    echo "📎 Архив найден: allure-report.zip"
                } else {
                    echo "🚫 Архив не найден: allure-report.zip"
                }

                emailext (
                    to: 'lichinin.v@yandex.ru',
                    subject: subject,
                    body: htmlBody,
                    mimeType: 'text/html',
                    attachLog: true,
                    attachmentsPattern: 'allure-report-secure.zip'
                )
            }
        }
    }
}
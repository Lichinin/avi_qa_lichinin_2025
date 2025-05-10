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
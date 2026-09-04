pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t restful-booker-automation .'
            }
        }

        stage('Run API Tests') {
            steps {
                bat '''
                docker run --rm -v "%CD%:/app" restful-booker-automation ^
                pytest tests/api -v -s ^
                --html=report.html ^
                --self-contained-html
                '''
            }
        }
    }

    post {

        always {
            publishHTML([
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: '.',
                reportFiles: 'report.html',
                reportName: 'API Automation Report'
            ])
        }

        success {
            echo 'API automation tests completed successfully.'
        }

        failure {
            echo 'API automation tests failed.'
        }
    }
}
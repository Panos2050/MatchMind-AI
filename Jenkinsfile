pipeline {
    agent any

    environment {
        PYTHON = 'python3'
        VENV_DIR = 'venv'
        MONGO_URI = 'mongodb://localhost:27017/'
    }

    triggers {
        cron('H 0 * * *') // ⏰ Run automatically every night at midnight
    }

    stages {

        stage('Checkout') {
            steps {
                echo '📦 Checking out code...'
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo '🐍 Setting up virtual environment...'
                sh '''
                    ${PYTHON} -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo '🧪 Running Pytest...'
                sh '''
                    . ${VENV_DIR}/bin/activate
                    pytest -v --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('Run Match Pipeline') {
            steps {
                echo '⚽ Running MatchMind-AI main script...'
                sh '''
                    . ${VENV_DIR}/bin/activate
                    ${PYTHON} main.py
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed — check Jenkins console logs or test results.'
        }
    }
}

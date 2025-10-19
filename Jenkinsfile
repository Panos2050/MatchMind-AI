pipeline {
    agent any

    triggers {
        cron('0 0 * * *')   // every midnight
        githubPush()        // whenever you push to GitHub
    }

    environment {
        PYTHONPATH = "${WORKSPACE}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo '📦 Checking out code...'
                git branch: 'main', url: 'https://github.com/panos2050MatchMind-AI.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo '🐍 Setting up virtual environment...'
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo '🧪 Running tests with pytest...'
                sh '''
                . venv/bin/activate
                pytest --maxfail=1 --disable-warnings -q --junitxml=test-results.xml
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
                echo '⚽ Running main.py (fetch + summarize)...'
                sh '''
                . venv/bin/activate
                python3 main.py
                '''
            }
        }
    }

    post {
        success {
            echo '✅ All tests passed and pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed — check Jenkins console logs or test results.'
        }
    }
}

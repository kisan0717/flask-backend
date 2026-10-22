
pipeline {
    agent any

    options {
        disableConcurrentBuilds()
        timestamps()
    }

    environment {
        DEPLOY_DIR = '/opt/apps/flask-backend'
        VENV = '/opt/apps/flask-backend/venv'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                sh '''
                    set -eu
                    python3 -m venv test-venv
                    test-venv/bin/pip install -r requirements.txt
                    test-venv/bin/pip install pytest
                    test-venv/bin/python -m pytest
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    set -eu

                    test -f app.py
                    test -f requirements.txt

                    rsync -av --delete \
                        --exclude='venv/' \
                        --exclude='test-venv/' \
                        --exclude='.git/' \
                        ./ "$DEPLOY_DIR/"

                    "$VENV/bin/pip" install \
                        -r "$DEPLOY_DIR/requirements.txt"

                    sudo /usr/bin/systemctl restart flask
                    sudo /usr/bin/systemctl is-active flask

                    curl --fail --silent --show-error \
                        http://127.0.0.1:5000/
                '''
            }
        }
    }

    post {
        success {
            echo 'Flask deployment successful!'
        }
        failure {
            echo 'Flask deployment failed. Check the console output.'
        }
        always {
            sh 'rm -rf test-venv'
        }
    }
}
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

                    rsync -r --delete \
                        --no-perms \
                        --no-owner \
                        --no-group \
                        --exclude='venv/' \
                        --exclude='test-venv/' \
                        --exclude='.git/' \
                        --exclude='__pycache__/' \
                        --exclude='.pytest_cache/' \
                        ./ "$DEPLOY_DIR/"

                    "$VENV/bin/pip" install \
                        -r "$DEPLOY_DIR/requirements.txt"

                    sudo /usr/bin/systemctl restart flask

                    for i in $(seq 1 10); do
                        if curl --fail --silent --show-error \
                            http://127.0.0.1:5000/; then
                            echo "Flask deployment successful!"
                            exit 0
                        fi
                        sleep 2
                    done

                    echo "Flask failed to respond after restart."
                    sudo /usr/bin/systemctl status flask --no-pager || true
                    sudo /usr/bin/journalctl -u flask -n 50 --no-pager || true
                    exit 1
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

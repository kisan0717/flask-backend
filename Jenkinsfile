
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

                    echo "Creating test environment..."

                    python3 -m venv test-venv

                    echo "Installing dependencies..."

                    test-venv/bin/pip install -r requirements.txt
                    test-venv/bin/pip install pytest

                    echo "Running Flask tests..."

                    test-venv/bin/python -m pytest -v
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    set -eu

                    echo "Validating Flask application files..."

                    test -f app.py
                    test -f config.py
                    test -f requirements.txt

                    echo "Copying application files to EC2..."

                    rsync -r \
                        --no-perms \
                        --no-owner \
                        --no-group \
                        --exclude='venv/' \
                        --exclude='test-venv/' \
                        --exclude='.git/' \
                        --exclude='__pycache__/' \
                        --exclude='.pytest_cache/' \
                        --exclude='.env' \
                        ./ "$DEPLOY_DIR/"

                    echo "Installing production dependencies..."

                    "$VENV/bin/pip" install \
                        -r "$DEPLOY_DIR/requirements.txt"

                    echo "Restarting Flask service..."

                    sudo /usr/bin/systemctl restart flask

                    echo "Waiting for Flask to become healthy..."

                    for i in $(seq 1 15); do

                        if curl --fail --silent \
                            http://127.0.0.1:5000/health >/dev/null; then

                            echo "Flask health check passed."
                            break
                        fi

                        if [ "$i" -eq 15 ]; then
                            echo "ERROR: Flask failed to start."

                            sudo /usr/bin/systemctl status flask --no-pager || true

                            exit 1
                        fi

                        echo "Waiting for Flask... attempt $i"
                        sleep 2
                    done

                    echo "Checking Flask homepage..."

                    curl --fail --silent --show-error \
                        http://127.0.0.1:5000/ \
                        | grep -q '"status":"success"'

                    echo "Checking Flask through Nginx..."

                    curl --fail --silent --show-error \
                        http://127.0.0.1/api/health \
                        | grep -q '"status":"healthy"'

                    echo "Flask deployment completed successfully."
                '''
            }
        }
    }

    post {

        success {
            echo 'SUCCESS: Flask backend deployed successfully.'
        }

        failure {
            echo 'FAILURE: Flask deployment failed. Check Console Output.'
        }

        always {
            sh 'rm -rf test-venv'
            echo 'Flask CI/CD pipeline execution completed.'
        }
    }
}

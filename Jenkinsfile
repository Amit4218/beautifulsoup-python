pipeline {
    agent any

    stages {
        stage('Setup Environment') {
            steps {
                script {
                    echo 'Setting up Python environment...'
                    sh '''
                        #!/bin/bash
                        set -e  # stop on first error

                        sudo apt update -y
                        sudo apt install -y python3 python3.12-venv

                        # Create virtual environment
                        python3 -m venv .venv

                        # Activate venv
                        . .venv/bin/activate

                        # Upgrade pip inside venv
                        pip install --upgrade pip

                        # Install dependencies
                        pip install -r requirements.txt
                        pip install requests
                    '''
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    echo 'Building the application...'
                    sh '''
                        #!/bin/bash
                        set -e
                        . .venv/bin/activate
                        pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    echo 'Running tests...'
                    sh '''
                        #!/bin/bash
                        set -e
                        . .venv/bin/activate
                        pytest main.test.py   
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo 'Deploying the application...'
                    sh '''
                        #!/bin/bash
                        set -e
                        . .venv/bin/activate
                        python main.py
                    '''
                    // Add deployment steps (e.g., rsync, docker, kubectl, etc.)
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}

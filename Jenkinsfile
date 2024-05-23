pipeline {
    agent { 
        dockerfile true
      }
    // triggers {
    //     pollSCM 'H * * * *'
    // }
    stages {
        // stage('Install Python Packages') {
        //     steps {
        //         sh 'echo "KURWAAAAAAA"'
        //     }
        // }

        stage('Run Application') {
            steps {
                sh 'python3 --version'
                sh 'ls'
                sh 'python -m pytest -s tests/interface_test.py'
            }
        }
    }
}
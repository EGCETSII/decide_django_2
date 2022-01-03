pipeline {
    agent { docker { image 'python:3.7.2' } }

    stages {
        stage('Build Master') {
            when {
                branch 'master' 
            }
            steps {
                sh '''
                pip install -r requirements.txt

                cd decide
                ./manage.py test -v 2
                '''
            }
        }

        stage('Deploy Master') {
            when {
                branch 'master' 
            }
            steps {
                /* Llamamos a Heroku y a darle caña */
            }
        }

        stage('Build Develop') {
            when {
                branch 'develop' 
            }
            steps {
                sh '''
                pip install -r requirements.txt

                cd decide
                ./manage.py test -v 2
                '''
            }
        }

        stage('Build G1') {
            when {
                branch 'G1' 
            }
            steps {
                sh '''
                pip install -r requirements.txt

                cd decide
                ./manage.py test authentication -v 2
                '''
            }
        }

        stage('Build G2') {
            when {
                branch 'G2' 
            }
            steps {
                sh '''
                pip install -r requirements.txt

                cd decide
                ./manage.py test booth -v 2
                '''
            }
        }

        stage('Build G3') {
            when {
                branch 'G3' 
            }
            steps {
                sh '''
                pip install -r requirements.txt

                cd decide
                ./manage.py test voting -v 2
                '''
            }
        }
    }
}

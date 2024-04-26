pipeline { 
    environment {
        IMAGE = "srishiva20/myrepo1"
    }
    agent any 
    stages {
        stage('checkout') {
            steps {
                git branch: 'main',
                url: 'https://github.com/srishiva3/project0.git'
            }
        }
        stage('Building the image and pushing to dockerhub') {
            steps {
                echo "building the docker image..."
                withCredentials([usernamePassword(credentialsId: 'dockerhub', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    sh "echo $PASS | docker login -u $USER --password-stdin"
                    sh "docker build -t ${IMAGE}:lts ."
                    sh "docker push ${IMAGE}:lts"
                }
            }
        }
    } 
}
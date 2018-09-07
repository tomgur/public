#!groovy
pipeline {
    agent { label 'slave' }

    environment {
        HEAD_BUILD_NUMBER = "${BUILD_NUMBER}"
        REGISTRY = "ec2-18-130-226-162.eu-west-2.compute.amazonaws.com"
    }

    options { timestamps() }

    stages {
        stage('Compile') {
            steps {
                withEnv(["JAVA_HOME=${tool 'jdk1.8'}", "PATH+MAVEN=${tool 'm2'}/bin:${env.JAVA_HOME}/bin"]) {
                    sh "mvn --batch-mode -V -U -e clean compile"
                }
            }
        }
        stage('Test') {
            steps {
                withEnv(["JAVA_HOME=${tool 'jdk1.8'}", "PATH+MAVEN=${tool 'm2'}/bin:${env.JAVA_HOME}/bin"]) {
                    sh "mvn --batch-mode -V -U -e clean test"
                }
            }
            post {
                always {
                    junit "**/target/surefire-reports/*.xml"
                }
            }
        }
        stage('Build WAR') {
            steps {
                withEnv(["JAVA_HOME=${tool 'jdk1.8'}", "PATH+MAVEN=${tool 'm2'}/bin:${env.JAVA_HOME}/bin"]) {
                    sh "mvn --batch-mode -V -U -e clean package -DskipTests"
                }
            }
        }
        stage('Deploy Snapshots') {
            steps {
                echo '------------ Deploying the WAR to nexus ------------'
                withEnv(["JAVA_HOME=${tool 'jdk1.8'}", "PATH+MAVEN=${tool 'm2'}/bin:${env.JAVA_HOME}/bin"]) {
                    sh "mvn -V -U -e clean deploy -DskipTests"
                }
            }
        }
        stage('Build and Deploy Docker') {
            steps {
                build job: 'Build-Docker-Image', parameters: [string(name: 'PARENT_BUILD_NUM', value: "${HEAD_BUILD_NUMBER}")]
            }
        }
        stage('Integration tests') {
            steps {
                echo "Running shopize:${BUILD_NUMBER} docker image"
                build job: 'Run-Docker-Image', parameters: [string(name: 'IMAGE_VERSION', value: "${HEAD_BUILD_NUMBER}"),
                                                            string(name: 'IMAGE_NAME', value: "${REGISTRY}/shopizer")]
                echo 'This is where we would setup integration tests - selnium etc...'
            }
        }
        stage('Prepare release') {
            steps {
                echo "Run the release plugin, tag the git revision, change the POM versions to new dev version"
            }
        }
        stage('Upload to production repositories') {
            steps {
                echo "Deploying new Version to production repositories"
            }
        }
        stage('Start Deploy to production procedures') {
            steps {
                echo "PRODUCTION!!!!"
            }
        }

    }
}

pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo '--- ETAPA 1: BUILD (Verificando entorno Python, Flask y Doxygen) ---'
                sh 'python3 --version'
                sh 'doxygen --version'
                sh 'python3 -m pip install --break-system-packages flask || true'
            }
        }
        stage('Test') {
            steps {
                echo '--- ETAPA 2: TEST (Ejecutando pruebas unitarias) ---'
                sh 'python3 -c "import app; client = app.app.test_client(); resp = client.get(\'/hello?name=Jenkins\'); assert resp.status_code == 200 and b\'Hello, Jenkins!\' in resp.data; print(\'TEST UNITARIO APROBADO:\', resp.data.decode())"'
            }
        }
        stage('Generate Documentation') {
            steps {
                echo '--- ETAPA 3: GENERATE DOCUMENTATION (Generando docs con Doxygen) ---'
                sh 'doxygen Doxyfile'
                sh 'ls -la docs/html/index.html'
            }
        }
        stage('Version Control') {
            steps {
                echo '--- ETAPA 4: VERSION CONTROL (Subiendo documentación generada a GitHub) ---'
                withCredentials([usernamePassword(credentialsId: 'github-token', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_PASS')]) {
                    sh '''
                        git config user.name "Jenkins CI"
                        git config user.email "jenkins@duocuc.cl"
                        git checkout -B main
                        git add docs/
                        if ! git diff --cached --quiet; then
                            git commit -m "Docs: Actualiza documentacion Doxygen desde Jenkins [Build #${BUILD_NUMBER}]"
                            git push https://${GIT_USER}:${GIT_PASS}@github.com/Abisai77/actividad-3-4-2-documentacion.git main
                        else
                            echo "Sin cambios nuevos en la documentacion."
                        fi
                    '''
                }
            }
        }
        stage('Deploy') {
            steps {
                echo '--- ETAPA 5: DEPLOY (Desplegando aplicación en entorno de prueba) ---'
                sh 'pkill -f "python3.*app.py" || true'
                sh 'JENKINS_NODE_COOKIE=dontKillMe nohup python3 app.py > app.log 2>&1 &'
                sh 'sleep 3'
                sh 'curl -s "http://127.0.0.1:5000/hello?name=David"'
            }
        }
    }
    post {
        success {
            echo 'ALERTA OK: Pipeline ejecutado con éxito. Documentación y despliegue actualizados.'
        }
        failure {
            echo 'ALERTA CRITICA: Fallo detectado en el pipeline de documentación o despliegue.'
        }
    }
}

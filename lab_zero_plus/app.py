import os
import subprocess
from flask import Flask, render_template, request, redirect, session
import db

app = Flask(__name__)
app.secret_key = "clave_insegura_para_cookies"

# Inicializar DB al arrancar
db.init_db()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        user = db.check_login(u, p)
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect('/dashboard')
        else:
            return render_template('login.html', error="Credenciales inválidas")
            
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session: return redirect('/')
    
    ping_result = ""
    # VULN: XSS Reflejado en el mensaje de bienvenida o búsqueda
    search_term = request.args.get('q', '')
    
    # VULN: RCE (Ping Tool)
    if request.method == 'POST':
        ip = request.form.get('ip')
        if ";" in ip:
            ping_result = "Caracter prohibido detectado"
        else:
            try:
                ping_result = subprocess.check_output(f"ping -c 1 {ip}", shell=True).decode()
            except Exception as e:
                ping_result = str(e)

    return render_template('dashboard.html', user=session['username'], result=ping_result, search=search_term)

@app.route('/profile')
def profile():
    if 'user_id' not in session: return redirect('/')
    
    # VULN: IDOR (Insecure Direct Object Reference)
    # El ID viene por la URL (?id=1) en lugar de la sesión.
    # Si no ponen ID, usamos el suyo.
    target_id = request.args.get('id', session['user_id'])
    
    user_data = db.get_user_by_id(target_id)
    return render_template('profile.html', data=user_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

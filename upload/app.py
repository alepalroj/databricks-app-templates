from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from werkzeug.utils import secure_filename
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.secret_key = 'super-alepalroj'

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

USERS = {'admin': 'admin'}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in USERS and USERS[username] == password:
            session['user'] = username
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('upload_file'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')

    return render_template('login.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'user' not in session:
        flash('Debes iniciar sesión para acceder', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        file = request.files.get('file')

        if not file or file.filename == '':
            flash('No se seleccionó ningún archivo', 'danger')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Archivo subido exitosamente', 'success')

    return render_template('upload.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Sesión cerrada', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

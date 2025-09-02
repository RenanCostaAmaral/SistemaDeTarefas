from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import threading
import webbrowser
import time
import os

app = Flask(__name__)

# 🔧 Inicializa o banco de dados SQLite
def inicializar_banco():
    conexao = sqlite3.connect('tarefas.db')
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT
        )
    ''')
    conexao.commit()
    conexao.close()

# 🏠 Página principal - Lista de tarefas
@app.route('/')
def listar_tarefas():
    conexao = sqlite3.connect('tarefas.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM tarefas')
    tarefas = cursor.fetchall()
    conexao.close()
    return render_template('lista.html', tarefas=tarefas)

# ➕ Criar nova tarefa
@app.route('/nova', methods=['GET', 'POST'])
def nova_tarefa():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        conexao = sqlite3.connect('tarefas.db')
        cursor = conexao.cursor()
        cursor.execute('INSERT INTO tarefas (titulo, descricao) VALUES (?, ?)', (titulo, descricao))
        conexao.commit()
        conexao.close()
        return redirect(url_for('listar_tarefas'))
    return render_template('nova_tarefa.html')

# ✏️ Editar uma tarefa
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_tarefa(id):
    conexao = sqlite3.connect('tarefas.db')
    cursor = conexao.cursor()

    if request.method == 'POST':
        novo_titulo = request.form['titulo']
        nova_descricao = request.form['descricao']
        cursor.execute(
            'UPDATE tarefas SET titulo = ?, descricao = ? WHERE id = ?',
            (novo_titulo, nova_descricao, id)
        )
        conexao.commit()
        conexao.close()
        return redirect(url_for('listar_tarefas'))

    cursor.execute('SELECT * FROM tarefas WHERE id = ?', (id,))
    tarefa = cursor.fetchone()
    conexao.close()
    return render_template('editar_tarefa.html', tarefa=tarefa)

# 🗑️ Excluir uma tarefa
@app.route('/excluir/<int:id>')
def excluir_tarefa(id):
    conexao = sqlite3.connect('tarefas.db')
    cursor = conexao.cursor()
    cursor.execute('DELETE FROM tarefas WHERE id = ?', (id,))
    conexao.commit()
    conexao.close()
    return redirect(url_for('listar_tarefas'))


if __name__ == '__main__':
    def abrir_navegador():
        time.sleep(1)
        webbrowser.open('http://localhost:5000')

    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Thread(target=abrir_navegador).start()

    inicializar_banco()
    app.run(debug=True)


from flask import Flask, render_template, redirect, url_for, flash, request
from models import Tarefa, db_session
from datetime import datetime
from sqlalchemy import select, func, extract
import os
import locale

app = Flask(__name__)
app.secret_key = os.urandom(24)
# Configurar idioma para português
# app.config['BABEL_DEFAULT_LOCALE'] = 'pt'
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')  # Configura o idioma para português


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/cadastrar', methods=["POST", "GET"])
def cadastrar():
    if request.method == "POST":
        # Captura os valores dos campos do formulário
        nome_tarefa = request.form["form_nome"]
        status = request.form["form_status"]
        data = request.form["form_data"]
        horario = request.form["form_horario"]
        descricao = request.form["form_descricao"]

        # Lista para armazenar mensagens de erro
        erros = []

        # Validação de cada campo
        if not nome_tarefa:
            erros.append("O campo 'Nome' é obrigatório.")
        if not status:
            erros.append("O campo 'Status' é obrigatório.")
        if not data:
            erros.append("O campo 'Data' é obrigatório.")
        if not horario:
            erros.append("O campo 'Horário' é obrigatório.")
        if not descricao:
            erros.append("O campo 'Descrição' é obrigatório.")

        # Se houver erros, exibe todas as mensagens
        if erros:
            for erro in erros:
                flash(erro, "error")
        else:
            # Se todos os campos estiverem preenchidos, cria o veterinário
            form_evento = Tarefa(
                nome_tarefa=nome_tarefa,
                status=status,
                data=data,
                horario=horario,
                descricao=descricao
            )
            form_evento.save()
            flash("Veterinário criado com sucesso!", "success")
            return redirect(url_for('tarefa'))

    return render_template('cadastro.html')

@app.route('/tarefa', methods=['GET'])
def tarefa():
    lista = db_session.execute(select(Tarefa)).scalars().all()

    return render_template('lista.html',
                           lista=lista,
                           )

def editar(id_tarefa):
    tarefa = db_session.execute(select(Tarefa).where(Tarefa.id_tarefa == id_tarefa)).scalar()

    if request.method == "POST":
        if not request.form.get("form_nome"):
            flash("O campo 'Nome' é obrigatório.")
        else:
            tarefa.nome_tarefa = request.form["form_nome"]
            tarefa.data = request.form["form_data"]
            tarefa.horario = request.form["form_horario"]
            tarefa.status = request.form["form_status"]
            tarefa.descricao = request.form["form_descricao"]
            tarefa.save()
            return redirect(url_for("tarefa"))

    return render_template('editar.html', tarefa=tarefa)


if __name__ == '__main__':
    app.run(debug=True)

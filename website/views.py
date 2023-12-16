from flask import Blueprint, render_template, request, flash, redirect
from flask_login import login_required, current_user
from datetime import datetime, date
from .models import Todo
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        # Se for uma busca, processar a pesquisa
        search_query = request.form.get('search_query')
        if search_query:
            results = Todo.query.filter(Todo.content.ilike(f"%{search_query}%")).all()
            return render_template('index.html', tasks=results, user=current_user, search_query=search_query)
       
    if request.method == 'POST':
        
        # Se não for uma busca, processar adição de tarefa
        input_content = request.form.get('input_content')
        input_due_date = request.form.get('input_due_date')

        if input_content is not None:
            if input_content and input_due_date:
                due_date = datetime.strptime(input_due_date, '%Y-%m-%d')
                new_task = Todo(content=input_content, due_date=due_date, user_id=current_user.id)
                db.session.add(new_task)
                db.session.commit()
                flash('Task added!', category='success')
            else:
                flash('Must add a task and a due date!', category='error')
        
    # Lógica para exibir tarefas de hoje
    today = date.today()
    tasks = Todo.query.filter(db.func.date(Todo.due_date) == today).order_by(Todo.due_date).all()

    current_date = datetime.now()
    formatted_date = current_date.strftime("%B, %d %Y")
    return render_template("index.html", user=current_user, formatted_date=formatted_date, tasks=tasks)



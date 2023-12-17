from flask import Blueprint, render_template, request, flash, redirect, url_for
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


@views.route('/delete/<int:id>')
@login_required
def delete(id):
    task_delete = Todo.query.get_or_404(id)

    db.session.delete(task_delete)
    db.session.commit()
    return redirect(url_for('views.home'))

@views.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    task = Todo.query.get_or_404(id)
   
    due_date_formatted = task.due_date.strftime('%Y-%m-%d')
   
    #task.due_date = datetime.strptime(due_date_formatted, '%Y-%m-%d').date()

    current_date = datetime.now()
    formatted_date = current_date.strftime("%B, %d %Y")

    if request.method == 'POST':
        task.content = request.form['input_content']
        input_due_date = request.form['input_due_date']
        task.due_date = datetime.strptime(input_due_date, '%Y-%m-%d')
        db.session.commit()
        flash('Task added!', category='success')
        return redirect(url_for('views.home'))

    else:
        return render_template("update.html", task=task, user=current_user, formatted_date=formatted_date, due_date_formatted=due_date_formatted)

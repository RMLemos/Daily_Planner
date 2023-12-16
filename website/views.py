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
        input_content = request.form.get('input_content')
        input_due_date = request.form.get('input_due_date')
        due_date = datetime.strptime(input_due_date, '%Y-%m-%d')
        if len(input_content) < 3:
            flash('Task is to short!', category='error')
        else:
            new_task = Todo(content=input_content, due_date=due_date, user_id=current_user.id)
            db.session.add(new_task) #adding the note to the database 
            db.session.commit()
            #return redirect('/')
    else:
        today = date.today()
        tasks = Todo.query.filter(db.func.date(Todo.due_date) == today).order_by(Todo.due_date).all()
    current_date = datetime.now()
    formatted_date = current_date.strftime("%B, %d %Y")
    return render_template("index.html", user=current_user, formatted_date=formatted_date, tasks=tasks)


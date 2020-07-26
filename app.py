from flask import Flask, request
from flask import render_template
from flask import redirect
import urllib.parse 
from flask_sqlalchemy import SQLAlchemy

params = urllib.parse.quote_plus("DRIVER={SQL Server};Server=tcp:db2-2387.database.windows.net,1433;Database=crud;Uid=dbadmin;Pwd=inti@lDrift#1;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    done = db.Column(db.Boolean, default=0)

    def __init__(self, content):
        self.content = content
        self.done = 0

    def __repr__(self):
        return '<Content %s>' % self.content


# db.create_all()


@app.route('/')
def tasks_list():
    tasks = Task.query.all()
    return render_template('list.html', tasks=tasks)


@app.route('/task', methods=['POST'])
def add_task():
    content = request.form['content']
    if not content:
        return 'Error'

    task = Task(content)
    db.session.add(task)
    db.session.commit()
    return redirect('/')


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return redirect('/')

    db.session.delete(task)
    db.session.commit()
    return redirect('/')


@app.route('/done/<int:task_id>')
def resolve_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return redirect('/')
    if task.done:
        task.done = 0
    else:
        task.done = 1

    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
     app.run()

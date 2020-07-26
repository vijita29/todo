from flask import Flask, request
from flask import render_template
from flask import redirect
import urllib.parse 

app = Flask(__name__)
tasks = [{'id': 1, 'content': 'Read', 'done': 0}, {'id': 2, 'content': 'Shopping', 'done': 0}, {'id': 3, 'content': 'Cleaning', 'done': 0}]


@app.route('/')
def tasks_list():
    return render_template('list.html', tasks=tasks)


@app.route('/task', methods=['POST'])
def add_task():
    content = request.form['content']
    if not content:
        return 'Error'

    if len(tasks)  < 1:
        task = {'id': 1, 'content': content, 'done': 0}
    else:
        task = {'id': tasks[-1]['id']+1, 'content': content, 'done': 0}
    tasks.append(task)
    return redirect('/')


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    
    i = 0
    for task in tasks:
        if task['id'] == task_id:
            tasks.pop(i)
        i = i + 1
    return redirect('/')


@app.route('/done/<int:task_id>')
def resolve_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            if task['done'] == 0:
                task['done'] = 1
            else:
                task['done'] = 0

    return redirect('/')


# if __name__ == '__main__':
#     app.run()





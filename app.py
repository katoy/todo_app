from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

def load_todos():
    try:
        with open('todos.json', 'r') as f:
            todos = json.load(f)
    except FileNotFoundError:
        todos = []
    return todos

def save_todos(todos):
    with open('todos.json', 'w') as f:
        json.dump(todos, f, indent=4)

@app.route('/')
def index():
    todos = load_todos()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    todos = load_todos()
    todo = request.form['todo']
    todos.append({'task': todo, 'completed': False})
    save_todos(todos)
    return redirect(url_for('index'))

@app.route('/update/<string:task>/<string:completed>', methods=['POST'])
def update_todo(task, completed):
    todos = load_todos()
    for todo in todos:
        if todo['task'] == task:
            todo['completed'] = completed == 'true'
            break
    save_todos(todos)
    return 'OK'

@app.route('/delete/<int:index>')
def delete_todo(index):
    todos = load_todos()
    del todos[index]
    save_todos(todos)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

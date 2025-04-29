from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

def load_todos():
    todos_file = os.environ.get('TODOS_FILE', 'todos.json')
    try:
        with open(todos_file, 'r') as f:
            todos = json.load(f)
    except FileNotFoundError:
        todos = []
    return todos

def load_translations(lang='en'):
    try:
        with open(f'translations/{lang}.json', 'r') as f:
            translations = json.load(f)
    except FileNotFoundError:
        translations = {}
    return translations

def save_todos(todos):
    todos_file = os.environ.get('TODOS_FILE', 'todos.json')
    with open(todos_file, 'w') as f:
        json.dump(todos, f, indent=4)

@app.route('/')
def index():
    todos = load_todos()
    lang = request.args.get('lang', 'en')
    translations = {}
    try:
        translations = load_translations(lang)
    except FileNotFoundError:
        pass
    return render_template('index.html', todos=todos, translations=translations, lang=lang)


@app.route('/add', methods=['POST'])
def add_todo():
    todos = load_todos()
    todo = request.form['todo']
    lang = request.form.get('lang', 'en')
    print(f"lang: {lang}")
    if todo.strip() == "":
        try:
            translations = load_translations(lang)
        except FileNotFoundError:
            translations = {}
        return render_template('index.html', todos=todos, error=translations.get('errorMessage', "Please enter a task name"), translations=translations, lang=lang)
    todos.append({'task': todo, 'completed': False})
    save_todos(todos)
    return redirect(url_for('index', lang=lang))

@app.route('/update/<string:task>/<string:completed>')
def update_todo(task, completed):
    todos = load_todos()
    found = False
    for todo in todos:
        if todo['task'] == task:
            todo['completed'] = completed.lower() == 'true'
            found = True
            break
    save_todos(todos)
    if not found:
        return 'Task not found', 404
    return redirect(url_for('index'))

@app.route('/delete/<int:index>')
def delete_todo(index):
    todos = load_todos()
    if 0 <= index < len(todos):
        del todos[index]
        save_todos(todos)
    else:
        return "Invalid index", 400
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

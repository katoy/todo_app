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

def load_translations(lang='en'):
    try:
        with open(f'translations/{lang}.json', 'r') as f:
            translations = json.load(f)
    except FileNotFoundError:
        translations = {}
    return translations

def save_todos(todos):
    with open('todos.json', 'w') as f:
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

@app.route('/update/<string:task>/<string:completed>', methods=['POST'])
def update_todo(task, completed):
    todos = load_todos()
    found = False
    for todo in todos:
        if todo['task'] == task:
            todo['completed'] = completed == 'true'
            found = True
            break
    save_todos(todos)
    if not found:
        return 'Task not found', 404
    return 'OK'

@app.route('/delete/<int:index>')
def delete_todo(index):
    todos = load_todos()
    try:
        del todos[index]
    except IndexError:
        return "Invalid index", 400
    save_todos(todos)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

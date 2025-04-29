from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

import logging

logging.basicConfig(level=logging.INFO)

import uuid

def load_todos():
    todos_file = os.environ.get('TODOS_FILE', 'todos.json')
    try:
        with open(todos_file, 'r') as f:
            todos = json.load(f)
            for todo in todos:
                if 'id' not in todo:
                    todo['id'] = str(uuid.uuid4())
    except FileNotFoundError:
        logging.info(f"Todos file not found: {todos_file}")
        todos = []
    return todos

def load_translations(lang='en'):
    try:
        with open(f'translations/{lang}.json', 'r') as f:
            translations = json.load(f)
    except FileNotFoundError:
        logging.info(f"Translations file not found: translations/{lang}.json")
        translations = {}
    return translations

def save_todos(todos):
    todos_file = os.environ.get('TODOS_FILE', 'todos.json')
    with open(todos_file, 'w') as f:
        json.dump(todos, f, indent=4, ensure_ascii=False)

import uuid

@app.route('/')
def index():
    todos = load_todos()
    lang = request.args.get('lang', 'en')
    translations = load_translations(lang)
    return render_template('index.html', todos=todos, translations=translations, lang=lang)

@app.route('/add', methods=['POST'])
def add_todo():
    todos = load_todos()
    todo = request.form['todo']
    lang = request.form['lang']
    print(f"lang: {lang}")
    if todo.strip() == "":
        translations = load_translations(lang)
        return render_template('index.html', todos=todos, error=translations.get('errorMessage', "Please enter a task name"), translations=translations, lang=lang)
    todos.append({'id': str(uuid.uuid4()), 'task': todo, 'completed': False})
    save_todos(todos)
    return redirect(url_for('index', lang=lang))

@app.route('/update/<string:task>/<string:completed>')
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
        return f'Task \'{task}\' not found', 404
    return redirect(url_for('index'))

@app.route('/delete/<string:id>')
def delete_todo(id):
    todos = load_todos()
    for i, todo in enumerate(todos):
        if todo['id'] == id:
            del todos[i]
            save_todos(todos)
            return redirect(url_for('index'))
    return f"Invalid id: {id}", 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

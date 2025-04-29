import unittest
import json
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, load_todos, load_translations, save_todos
from bs4 import BeautifulSoup
from flask import Flask

class TestApp(unittest.TestCase):

    def setUp(self):
        os.environ['TODOS_FILE'] = 'test_todos.json'
        self.app = app.test_client()
        self.app.testing = True
        self.test_task = "Test Task"
        self.test_lang = "en"

    def test_index_route(self):
        response = self.app.get('/?lang=' + self.test_lang)
        self.assertEqual(response.status_code, 200)

    def test_add_route(self):
        response = self.app.post('/add', data=dict(todo=self.test_task, lang=self.test_lang), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        todos = load_todos()
        self.assertTrue(any(d['task'] == self.test_task for d in todos))
        # Clean up: remove the added task
        todos = load_todos()
        todos = [item for item in todos if item['task'] != self.test_task]
        save_todos(todos)

    def test_update_route(self):
        # Add a test task
        todos = load_todos()
        todos.append({'task': self.test_task, 'completed': False, 'id': 'test_id'})
        save_todos(todos)
        # Update the test task
        response = self.app.get(f'/update/{self.test_task}/true', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        todos = load_todos()
        self.assertTrue(any(d['task'] == self.test_task and d['completed'] for d in todos))
        # Clean up: revert the changes
        todos = load_todos()
        for todo in todos:
            if todo['task'] == self.test_task:
                todo['completed'] = False
        save_todos(todos)
        todos = load_todos()
        todos = [item for item in todos if item['task'] != self.test_task]
        save_todos(todos)

    def test_delete_route(self):
        # Add a test task
        todos = load_todos()
        todos.append({'task': self.test_task, 'completed': False, 'id': 'test_id'})
        save_todos(todos)
         # Delete the test task
        with self.app:
            todos = load_todos()
            todo_id = None
            for todo in todos:
                if todo['task'] == self.test_task:
                    todo_id = todo['id']
                    break
            response = self.app.get(f'/delete/{todo_id}', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            todos = load_todos()
            self.assertFalse(any(d['task'] == self.test_task for d in todos))

if __name__ == '__main__':
    unittest.main()

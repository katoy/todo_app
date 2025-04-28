import unittest
import json
from flask import Flask
from app import app, load_todos, load_translations, save_todos
from bs4 import BeautifulSoup

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_load_todos(self):
        todos = load_todos()
        self.assertIsInstance(todos, list)

    def test_load_translations(self):
        translations = load_translations('en')
        self.assertIsInstance(translations, dict)
        self.assertEqual(translations['title'], 'Todo List')

    def test_add_todo(self):
        with self.app:
            response = self.app.post('/add', data=dict(todo='Test Todo', lang='en'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            todos = load_todos()
            self.assertIn({'task': 'Test Todo', 'completed': False}, todos)
            # Clean up
            todos.remove({'task': 'Test Todo', 'completed': False})
            save_todos(todos)

    def test_add_todo_empty(self):
        with self.app:
            response = self.app.post('/add', data=dict(todo='', lang='en'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Please enter a task name', response.data)

    def test_update_todo(self):
        # Add a todo first
        todos = load_todos()
        todos.append({'task': 'Test Update', 'completed': False})
        save_todos(todos)
        with self.app:
            response = self.app.post('/update/Test Update/true')
            self.assertEqual(response.status_code, 200)
            todos = load_todos()
            for todo in todos:
                if todo['task'] == 'Test Update':
                    self.assertEqual(todo['completed'], True)
                    break
        # Clean up
        todos.remove({'task': 'Test Update', 'completed': True})
        save_todos(todos)

    def test_update_todo_not_found(self):
        with self.app:
            response = self.app.post('/update/NonExistentTask/true')
            self.assertEqual(response.status_code, 404)
            self.assertIn(b'Task not found', response.data)

    def test_delete_todo(self):
        # Add a todo first
        todos = load_todos()
        todos.append({'task': 'Test Delete', 'completed': False})
        save_todos(todos)
        index = len(todos) - 1
        with self.app:
            response = self.app.get(f'/delete/{index}', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            todos = load_todos()
            self.assertNotIn({'task': 'Test Delete', 'completed': False}, todos)

    def test_delete_todo_invalid_index(self):
        with self.app:
            response = self.app.get('/delete/999', follow_redirects=True)
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Invalid index', response.data)

    def test_load_translations_not_found(self):
        translations = load_translations('nonexistent')
        self.assertIsInstance(translations, dict)
        self.assertEqual(translations, {})

    def test_index_translation_not_found(self):
        with self.app:
            response = self.app.get('/?lang=nonexistent')
            self.assertEqual(response.status_code, 200)

        # Check if the translations variable is an empty dictionary
        response = self.app.get('/?lang=nonexistent')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        title = soup.find('h1').text
        self.assertEqual(title, 'Todo List')

    def test_add_todo_translation_not_found(self):
        with self.app:
            response = self.app.post('/add', data=dict(todo='Test Todo', lang='nonexistent'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            soup = BeautifulSoup(response.data, 'html.parser')
            error_message = soup.find('p', {'style': 'color: red;'}).text
            self.assertEqual(error_message, '')

    def test_add_todo_no_error(self):
        with self.app:
            response = self.app.post('/add', data=dict(todo='Test Todo', lang='en'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            soup = BeautifulSoup(response.data, 'html.parser')
            error_message = soup.find('p', {'style': 'color: red;'}).text
            self.assertEqual(error_message, '')

    def test_placeholder_translation(self):
        with self.app:
            response = self.app.get('/?lang=en')
            self.assertEqual(response.status_code, 200)
            soup = BeautifulSoup(response.data, 'html.parser')
            placeholder = soup.find('input', {'name': 'todo'})['placeholder']
            self.assertEqual(placeholder, 'Enter todo')

    def test_index_translation_not_found_empty_dict(self):
        with self.app:
            response = self.app.get('/?lang=nonexistent')
            self.assertEqual(response.status_code, 200)

    def test_load_translations_not_found_in_index(self):
        translations = load_translations('nonexistent')
        self.assertIsInstance(translations, dict)
        self.assertEqual(translations, {})

    def test_index_translation_not_found_empty_dict_2(self):
        with self.app:
            response = self.app.get('/?lang=nonexistent')
            self.assertEqual(response.status_code, 200)
            soup = BeautifulSoup(response.data, 'html.parser')
            self.assertEqual(soup.find('h1').text, 'Todo List')
            self.assertEqual(soup.find('p', {'style': 'color: red;'}).text, '')

if __name__ == '__main__':
    unittest.main()

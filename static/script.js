const languageSelect = document.getElementById('language-select');
languageSelect.addEventListener('change', function() {
    const lang = this.value;
    window.location.href = '/?lang=' + lang;
});

function updateTodoStatus(id, completed) {
  fetch('/update/' + id + '/' + completed, {
    method: 'GET',
  }).then(response => {
    if (!response.ok) {
      console.error('Failed to update todo status');
    }
  }).catch(error => {
    console.error('Error:', error);
  });
}

const todoTable = document.getElementById('todo-table');

function changeLanguage(lang) {
    window.location.href = '/?lang=' + lang;
}

todoTable.addEventListener('change', function(event) {
    if (event.target.type === 'checkbox') {
        const id = event.target.dataset.task;
        const taskNameSpan = document.getElementById('task-name-' + id);
        if (event.target.checked) {
            taskNameSpan.classList.remove('pending');
            taskNameSpan.classList.add('completed');
        } else {
            taskNameSpan.classList.remove('completed');
            taskNameSpan.classList.add('pending');
        }
    }
});

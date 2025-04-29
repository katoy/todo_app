const languageSelect = document.getElementById('language-select');
languageSelect.addEventListener('change', function() {
    const lang = this.value;
    window.location.href = '/?lang=' + lang;
});

function getLanguage() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('lang') || 'en';
}

function updateTodoStatus(id, completed) {
  fetch('/update/' + id + '/' + completed + '?lang=' + getLanguage(), {
    method: 'GET',
  }).then(response => {
    if (!response.ok) {
      console.error('Failed to update todo status');
    } else {
      const taskName = document.getElementById(`task-name-${id}`);
      if (completed === true) {
        taskName.classList.add('completed');
        taskName.classList.remove('pending');
      } else {
        taskName.classList.add('pending');
        taskName.classList.remove('completed');
      }
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
        const completed = event.target.checked;
        updateTodoStatus(id, completed);
    }
});

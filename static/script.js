const languageSelect = document.getElementById('language-select');
languageSelect.addEventListener('change', function() {
    const lang = this.value;
    window.location.href = '/?lang=' + lang;
});

function updateTodoStatus(task, completed) {
  fetch('/update/' + task, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ completed })
  }).then(response => {
    if (!response.ok) {
      console.error('Failed to update todo status');
    }
  }).catch(error => {
    console.error('Error:', error);
  });
}

const todoTable = document.getElementById('todo-table');
todoTable.addEventListener('change', function(event) {
    if (event.target.type === 'checkbox') {
        const task = event.target.dataset.task;
        const listItem = event.target.parentNode.parentNode;
        if (event.target.checked) {
            listItem.classList.add('completed');
            listItem.classList.remove('pending');
        } else {
            listItem.classList.add('pending');
            listItem.classList.remove('completed');
        }
    }
});

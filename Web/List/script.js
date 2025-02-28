// Get DOM elements
const taskInput = document.getElementById('taskInput');
const addTaskButton = document.getElementById('addTaskButton');
const taskList = document.getElementById('taskList');

// Function to add a task
function addTask() {
    const taskText = taskInput.value.trim();
    if (taskText === '') return;

    // Create a new list item
    const listItem = document.createElement('li');
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    const taskSpan = document.createElement('span');
    taskSpan.textContent = taskText;
    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Delete';
    deleteButton.classList.add('delete-button');

    // Add elements to the list item
    listItem.appendChild(checkbox);
    listItem.appendChild(taskSpan);
    listItem.appendChild(deleteButton);

    // Add the list item to the task list
    taskList.appendChild(listItem);

    // Clear the input box
    taskInput.value = '';

    // Add an event listener to the checkbox
    checkbox.addEventListener('change', function () {
        if (this.checked) {
            listItem.classList.add('completed');
        } else {
            listItem.classList.remove('completed');
        }
    });

    // Add an event listener to the delete button
    deleteButton.addEventListener('click', function () {
        taskList.removeChild(listItem);
    });
}

// Add a click event listener to the add button
addTaskButton.addEventListener('click', addTask);

// Add a keydown event listener to the input box, add a task when the Enter key is pressed
taskInput.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        addTask();
    }
});
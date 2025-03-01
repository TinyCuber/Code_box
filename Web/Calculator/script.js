const display = document.getElementById('display');
let memory = 0;
let history = [];
let expressionHistory = [];
const historyTable = document.getElementById('history-table').getElementsByTagName('tbody')[0];
const historyModal = document.getElementById('history-modal');

function appendToDisplay(value) {
    if (value === 'π') {
        display.value += Math.PI;
    } else {
        display.value += value;
    }
}

function clearDisplay() {
    display.value = '';
}

function deleteLast() {
    display.value = display.value.slice(0, -1);
}

function calculate() {
    const currentExpression = display.value;
    try {
        let expression = currentExpression;
        // Handle brackets, replace square brackets and curly brackets with parentheses
        expression = expression.replace(/\[/g, '(').replace(/]/g, ')').replace(/{/g, '(').replace(/}/g, ')');
        // Handle percentage
        expression = expression.replace(/%/g, '/100');
        // Handle power operation
        expression = expression.replace(/\^/g, '**');

        // Handle x√y operation
        while (expression.includes('x√y')) {
            const parts = expression.split('x√y');
            const base = parseFloat(parts[0].match(/\d+(\.\d+)?$/)[0]);
            const exponent = parseFloat(parts[1].match(/^\d+(\.\d+)?/)[0]);
            const result = Math.pow(exponent, 1 / base);
            const newExpression = parts[0].replace(/\d+(\.\d+)?$/, '') + result + parts[1].replace(/^\d+(\.\d+)?/, '');
            expression = newExpression;
        }

        const result = eval(expression);
        display.value = result;
        history.push(result);
        expressionHistory.push(currentExpression);
        updateHistoryTable();
    } catch (error) {
        display.value = 'Error';
    }
}

function showHistory() {
    historyModal.style.display = 'block';
    updateHistoryTable();
}

function closeHistory() {
    historyModal.style.display = 'none';
}

function updateHistoryTable() {
    historyTable.innerHTML = '';
    for (let i = 0; i < history.length; i++) {
        const row = historyTable.insertRow();
        const cell1 = row.insertCell(0);
        const cell2 = row.insertCell(1);
        cell1.textContent = i + 1;
        cell2.textContent = expressionHistory[i] + ' = ' + history[i];
        row.addEventListener('click', function (event) {
            if (event.ctrlKey) {
                this.classList.toggle('selected');
            }
        });
    }
}

function deleteAllHistory() {
    if (confirm('Are you sure you want to delete all history records?')) {
        history = [];
        expressionHistory = [];
        updateHistoryTable();
    }
}

function deleteSelectedHistory() {
    const selectedRows = Array.from(historyTable.rows).filter(row => row.classList.contains('selected'));
    if (selectedRows.length > 0) {
        if (confirm('Are you sure you want to delete the selected history records?')) {
            const selectedIndices = selectedRows.map(row => Array.from(historyTable.rows).indexOf(row));
            selectedIndices.sort((a, b) => b - a);
            selectedIndices.forEach(index => {
                history.splice(index, 1);
                expressionHistory.splice(index, 1);
            });
            updateHistoryTable();
        }
    }
}

function historyRecord() {
    showHistory();
}

function memoryAdd() {
    memory += parseFloat(display.value) || 0;
}

function memorySubtract() {
    memory -= parseFloat(display.value) || 0;
}

function memoryRecallClear() {
    if (memory) {
        display.value = memory;
    } else {
        memory = 0;
        clearDisplay();
    }
}

function factorial() {
    let num = parseInt(display.value);
    if (isNaN(num)) {
        display.value = 'Error';
        return;
    }
    let result = 1;
    for (let i = 1; i <= num; i++) {
        result *= i;
    }
    display.value = result;
}

function rootXY() {
    appendToDisplay('x√y');
}

function squareRoot() {
    let num = parseFloat(display.value);
    if (isNaN(num)) {
        display.value = 'Error';
        return;
    }
    display.value = Math.sqrt(num);
}

function reciprocal() {
    let num = parseFloat(display.value);
    if (isNaN(num) || num === 0) {
        display.value = 'Error';
        return;
    }
    display.value = 1 / num;
}

function changeSign() {
    let num = parseFloat(display.value);
    if (!isNaN(num)) {
        display.value = -num;
    }
}
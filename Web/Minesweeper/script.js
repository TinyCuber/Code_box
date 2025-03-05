const boardElement = document.getElementById('board');
const difficultySelect = document.getElementById('difficulty');
const timerElement = document.getElementById('timer');
const customSettings = document.getElementById('custom-settings');
const customRowsInput = document.getElementById('custom-rows');
const customColsInput = document.getElementById('custom-cols');
const customMinesInput = document.getElementById('custom-mines');
const gameStatusElement = document.getElementById('game-status');
const historyButton = document.getElementById('historyButton');
const historyModal = document.getElementById('history-modal');
const historyTable = document.getElementById('history-table').getElementsByTagName('tbody')[0];

let rows, cols, mines;
let board;
let gameStarted = false;
let timer;
let timeElapsed = 0;
let gameHistory = [];

difficultySelect.addEventListener('change', function () {
    if (this.value === 'custom') {
        customSettings.style.display = 'inline';
    } else {
        customSettings.style.display = 'none';
    }
    startGame();
});

function startGame() {
    clearInterval(timer);
    timeElapsed = 0;
    timerElement.textContent = `Time: ${timeElapsed} seconds`;
    gameStarted = false;
    gameStatusElement.textContent = '😀';

    const difficulty = difficultySelect.value;
    if (difficulty === 'custom') {
        rows = parseInt(customRowsInput.value);
        cols = parseInt(customColsInput.value);
        mines = parseInt(customMinesInput.value);

        if (rows < 1 || rows > 24 || cols < 1 || cols > 30 || mines < 1 || mines > 667 || mines >= rows * cols) {
            alert('Invalid input parameters. Please ensure the number of rows is between 1 - 24, the number of columns is between 1 - 30, and the number of mines is between 1 - 667 and less than the total number of board cells!');
            return;
        }
    } else {
        switch (difficulty) {
            case 'easy':
                rows = 9;
                cols = 9;
                mines = 10;
                break;
            case 'medium':
                rows = 16;
                cols = 16;
                mines = 40;
                break;
            case 'hard':
                rows = 16;
                cols = 30;
                mines = 99;
                break;
        }
    }

    board = createBoard(rows, cols);
    renderBoard();
}

function createBoard(rows, cols) {
    const board = [];
    for (let i = 0; i < rows; i++) {
        const row = [];
        for (let j = 0; j < cols; j++) {
            row.push({
                isMine: false,
                isRevealed: false,
                isFlagged: false,
                adjacentMines: 0
            });
        }
        board.push(row);
    }
    return board;
}

function renderBoard() {
    boardElement.innerHTML = '';
    boardElement.style.gridTemplateColumns = `repeat(${cols}, 30px)`;

    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < cols; j++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.dataset.row = i;
            cell.dataset.col = j;

            cell.addEventListener('click', () => handleClick(i, j));
            cell.addEventListener('contextmenu', (e) => {
                e.preventDefault();
                handleRightClick(i, j);
            });

            boardElement.appendChild(cell);
        }
    }
}

function handleClick(row, col) {
    if (!gameStarted) {
        gameStarted = true;
        placeMines(row, col);
        calculateAdjacentMines();
        timer = setInterval(() => {
            timeElapsed++;
            timerElement.textContent = `Time: ${timeElapsed} seconds`;
        }, 1000);
    }

    if (board[row][col].isFlagged) return;
    if (board[row][col].isMine) {
        endGame(false);
    } else {
        revealCell(row, col);
        checkWin();
    }
}

function handleRightClick(row, col) {
    if (!gameStarted) return;
    if (!board[row][col].isRevealed) {
        board[row][col].isFlagged = !board[row][col].isFlagged;
        const cell = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
        if (board[row][col].isFlagged) {
            cell.textContent = '🚩';
            cell.classList.add('flagged');
        } else {
            cell.textContent = '';
            cell.classList.remove('flagged');
        }
    }
}

function placeMines(safeRow, safeCol) {
    let placedMines = 0;
    const safeZone = getSafeZone(safeRow, safeCol);

    while (placedMines < mines) {
        const row = Math.floor(Math.random() * rows);
        const col = Math.floor(Math.random() * cols);
        const isInSafeZone = safeZone.some(([r, c]) => r === row && c === col);
        if (!board[row][col].isMine &&!isInSafeZone) {
            board[row][col].isMine = true;
            placedMines++;
        }
    }
}

function getSafeZone(row, col) {
    const safeZone = [];
    for (let x = Math.max(row - 1, 0); x <= Math.min(row + 1, rows - 1); x++) {
        for (let y = Math.max(col - 1, 0); y <= Math.min(col + 1, cols - 1); y++) {
            safeZone.push([x, y]);
        }
    }
    return safeZone;
}

function calculateAdjacentMines() {
    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < cols; j++) {
            if (!board[i][j].isMine) {
                let count = 0;
                for (let x = Math.max(i - 1, 0); x <= Math.min(i + 1, rows - 1); x++) {
                    for (let y = Math.max(j - 1, 0); y <= Math.min(j + 1, cols - 1); y++) {
                        if (board[x][y].isMine) {
                            count++;
                        }
                    }
                }
                board[i][j].adjacentMines = count;
            }
        }
    }
}

function revealCell(row, col) {
    if (row < 0 || row >= rows || col < 0 || col >= cols) return;
    if (board[row][col].isRevealed || board[row][col].isFlagged) return;

    board[row][col].isRevealed = true;
    const cell = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
    cell.classList.add('revealed');

    if (board[row][col].adjacentMines > 0) {
        cell.textContent = board[row][col].adjacentMines;
        cell.dataset.number = board[row][col].adjacentMines;
    } else {
        for (let x = Math.max(row - 1, 0); x <= Math.min(row + 1, rows - 1); x++) {
            for (let y = Math.max(col - 1, 0); y <= Math.min(col + 1, cols - 1); y++) {
                revealCell(x, y);
            }
        }
    }
}

function checkWin() {
    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < cols; j++) {
            if (!board[i][j].isMine &&!board[i][j].isRevealed) {
                return;
            }
        }
    }
    endGame(true);
}

function endGame(isWin) {
    clearInterval(timer);
    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < cols; j++) {
            const cell = document.querySelector(`[data-row="${i}"][data-col="${j}"]`);
            if (board[i][j].isMine) {
                cell.textContent = '💣';
                cell.classList.add('mine');
            } else if (board[i][j].isFlagged) {
                cell.textContent = '❌';
                cell.classList.add('wrong-flag');
            }
        }
    }
    gameStatusElement.textContent = isWin ? '😎' : '😵';
    alert(isWin ? 'Congratulations, you won the game!' : 'Game over, you stepped on a mine!');

    const difficulty = difficultySelect.value;
    let mode;
    if (difficulty === 'custom') {
        mode = `Custom (Width: ${cols}, Height: ${rows}, Mines: ${mines})`;
    } else {
        switch (difficulty) {
            case 'easy':
                mode = 'Easy';
                break;
            case 'medium':
                mode = 'Medium';
                break;
            case 'hard':
                mode = 'Hard';
                break;
        }
    }
    const result = isWin ? 'Win' : 'Lose';
    const record = {
        mode: mode,
        time: `${timeElapsed} seconds`,
        result: result
    };
    gameHistory.push(record);
    updateHistoryTable();
}

function updateHistoryTable() {
    historyTable.innerHTML = '';
    gameHistory.forEach(record => {
        const row = historyTable.insertRow();
        const modeCell = row.insertCell(0);
        const timeCell = row.insertCell(1);
        const resultCell = row.insertCell(2);
        modeCell.textContent = record.mode;
        timeCell.textContent = record.time;
        resultCell.textContent = record.result;
    });
}

function openHistoryModal() {
    historyModal.style.display = 'block';
}

function closeHistoryModal() {
    historyModal.style.display = 'none';
}

historyButton.addEventListener('click', openHistoryModal);

// Call startGame once during initialization
startGame();
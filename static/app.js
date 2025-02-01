// DOM Elements
const loginSection = document.getElementById('login-section');
const registerSection = document.getElementById('register-section');
const buttonMenu = document.getElementById('button-menu');
const gameSection = document.getElementById('game-section');
const studyModeSection = document.getElementById('study-mode-section');
const leaderboardSection = document.getElementById('leaderboard-section');
const leaderboardList = document.getElementById('leaderboard');
const cyberProgressBar = document.getElementById('cyber-progress'); // (Not used directly now)
const hackerProgressBar = document.getElementById('hacker-progress'); // (Not used directly now)
const flashcardInner = document.querySelector('.flashcard-inner');
const flashcardTitle = document.getElementById('flashcard-question');
const flashcardContent = document.getElementById('flashcard-answer');
const endGameButtons = document.getElementById('end-game-buttons');
const viewScoreBtn = document.getElementById('view-score-btn');
const exitGameBtn = document.getElementById('exit-game-btn');
const exitMainBtn = document.getElementById('exit-main-btn'); // Exit button from main menu
const mainMenuBtn = document.getElementById('main-menu-btn');   // Main Menu button in game screen

// New elements for animations are assumed to be present:
// <div id="fireworks"></div> and <div id="error-msg"></div>

let username = '';
let currentStage = 1;
let questionIndex = 0;
let questions = [];
let flashcards = [];
let currentFlashcardIndex = 0;
let cyberProgress = 0; // In %
let hackerProgress = 0;  // In %
let correctAnswers = 0;
let questionTimer;
let gameFinished = false; // Flag to prevent further processing after game over

// Study Cards Array (Static Educational Content)
const studyCards = [
  {
    title: "Phishing",
    content: "Phishing is a type of social engineering attack where attackers disguise themselves as trustworthy entities in electronic communications. Always verify the sender and avoid clicking on suspicious links."
  },
  {
    title: "Password Strength",
    content: "A strong password is key to protecting your accounts. Use a mix of uppercase and lowercase letters, numbers, and special characters, and avoid using easily guessable information."
  },
  {
    title: "Vulnerability Detection",
    content: "Vulnerability detection involves identifying and mitigating security weaknesses in systems. Regular updates and security scans help protect against exploits."
  },
  {
    title: "Incident Response",
    content: "Incident response is the process of handling a cyber attack or security breach. It involves immediate actions to contain the breach and remediate the vulnerabilities exploited."
  },
  {
    title: "Cyber Puzzles",
    content: "Cyber puzzles test your cybersecurity knowledge in a fun and engaging way. They challenge your problem-solving skills and help reinforce best practices in digital security."
  }
];

// -------------------- Authentication Functions --------------------

// Login
document.getElementById('login-btn').addEventListener('click', async () => {
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  const response = await fetch('/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  const result = await response.json();
  if (response.ok) {
    username = result.username;
    loginSection.style.display = 'none';
    buttonMenu.style.display = 'block';
  } else {
    alert(result.error);
  }
});

// Registration
document.getElementById('register-btn').addEventListener('click', async () => {
  const regUsername = document.getElementById('register-username').value;
  const regEmail = document.getElementById('register-email').value;
  const regPassword = document.getElementById('register-password').value;
  const response = await fetch('/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: regUsername, email: regEmail, password: regPassword }),
  });
  const result = await response.json();
  if (response.ok) {
    alert(result.message);
    registerSection.style.display = 'none';
    loginSection.style.display = 'block';
  } else {
    alert(result.error);
  }
});

// Toggle between Login and Registration
document.getElementById('show-register').addEventListener('click', (e) => {
  e.preventDefault();
  loginSection.style.display = 'none';
  registerSection.style.display = 'block';
});
document.getElementById('show-login').addEventListener('click', (e) => {
  e.preventDefault();
  registerSection.style.display = 'none';
  loginSection.style.display = 'block';
});

// -------------------- Main Menu and Navigation --------------------

// Main Menu Exit Button: Go back to login screen
exitMainBtn.addEventListener('click', () => {
  resetGame();
});

// Main Menu Button in Game: Return to the main menu (button menu)
mainMenuBtn.addEventListener('click', () => {
  resetToMenu();
});

// Start Game
document.getElementById('start-game-btn').addEventListener('click', () => {
  gameFinished = false;
  buttonMenu.style.display = 'none';
  gameSection.style.display = 'block';
  // Ensure the custom progress section is visible
  document.getElementById('progress-section').style.display = 'block';
  loadQuestions(currentStage);
});

// Study Mode: Use static study cards
document.getElementById('study-mode-btn').addEventListener('click', () => {
  flashcards = studyCards;
  currentFlashcardIndex = 0;
  displayStudyCard(currentFlashcardIndex);
  flashcardInner.classList.remove('flipped');
  buttonMenu.style.display = 'none';
  studyModeSection.style.display = 'block';
});

// Toggle flashcard flip on click
flashcardInner.addEventListener('click', function() {
  this.classList.toggle('flipped');
});

// Function to display a study card
function displayStudyCard(index) {
  const card = flashcards[index];
  flashcardTitle.textContent = card.title;
  flashcardContent.textContent = card.content;
  flashcardInner.classList.remove('flipped');
}

// Study Mode Navigation
document.getElementById('prev-flashcard-btn').addEventListener('click', () => {
  if (currentFlashcardIndex > 0) {
    currentFlashcardIndex--;
    displayStudyCard(currentFlashcardIndex);
  } else {
    alert('This is the first flashcard.');
  }
});
document.getElementById('next-flashcard-btn').addEventListener('click', () => {
  if (currentFlashcardIndex < flashcards.length - 1) {
    currentFlashcardIndex++;
    displayStudyCard(currentFlashcardIndex);
  } else {
    alert('This is the last flashcard.');
  }
});
document.getElementById('exit-study-mode-btn').addEventListener('click', () => {
  studyModeSection.style.display = 'none';
  buttonMenu.style.display = 'block';
});

// Leaderboard Functionality
document.getElementById('leaderboard-btn').addEventListener('click', async () => {
  buttonMenu.style.display = 'none';
  gameSection.style.display = 'none';
  studyModeSection.style.display = 'none';
  leaderboardSection.style.display = 'block';
  const response = await fetch('/leaderboard');
  if (response.ok) {
    const data = await response.json();
    const leaderboardUl = document.getElementById('leaderboard');
    leaderboardUl.innerHTML = '';
    data.forEach(entry => {
      const li = document.createElement('li');
      li.textContent = `${entry.username} - ${entry.score} (${entry.date})`;
      leaderboardUl.appendChild(li);
    });
  } else {
    alert("Failed to load leaderboard.");
  }
});
document.getElementById('back-to-login-btn').addEventListener('click', () => {
  leaderboardSection.style.display = 'none';
  buttonMenu.style.display = 'block';
});

// -------------------- Game Mode Functions --------------------

// Load Questions (Game Mode)
async function loadQuestions(stage) {
  const response = await fetch(`/questions/${stage}`);
  questions = await response.json();
  if (questions.length > 0) {
    questionIndex = 0;
    displayQuestion(questions[questionIndex]);
  } else {
    alert('No questions available.');
  }
}

// Display Question (Game Mode)
function displayQuestion(question) {
  document.getElementById('stage-number').textContent = `Stage ${currentStage}`;
  document.getElementById('question-text').textContent = question.question;
  const optionsDiv = document.getElementById('options');
  optionsDiv.innerHTML = '';
  for (const [key, value] of Object.entries(question.options)) {
    const button = document.createElement('button');
    button.textContent = `${key}: ${value}`;
    button.addEventListener('click', () => {
      clearInterval(questionTimer);
      submitAnswer(question.id, key);
    });
    optionsDiv.appendChild(button);
  }
  startTimer(30);
}

// Timer Function
function startTimer(duration) {
  let timeRemaining = duration;
  const timerElement = document.getElementById('timer');
  timerElement.textContent = `Time Left: ${timeRemaining}s`;
  questionTimer = setInterval(() => {
    timeRemaining--;
    timerElement.textContent = `Time Left: ${timeRemaining}s`;
    if (timeRemaining <= 0) {
      clearInterval(questionTimer);
      alert('Time is up!');
      submitAnswer(questions[questionIndex].id, null);
    }
  }, 1000);
}

// Save Score Function (POST to /save_score)
async function saveScore(score) {
  const response = await fetch('/save_score', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, score }),
  });
  if (!response.ok) {
    alert('Error saving score.');
  }
}

// Finish Game Helper Function (accepts isWin flag)
function finishGame(finalMessage, isWin) {
  gameFinished = true;
  saveScore(cyberProgress);
  if (isWin) {
    showFireworks();
  } else {
    showErrorAnimation(finalMessage);
  }
  setTimeout(() => {
    resetToMenu();
  }, 3000);
}

// Reset Game State and Show Main Menu (for Game Mode)
function resetToMenu() {
  clearInterval(questionTimer);
  gameSection.style.display = 'none';
  studyModeSection.style.display = 'none';
  leaderboardSection.style.display = 'none';
  endGameButtons.style.display = 'none';
  cyberProgress = 0;
  hackerProgress = 0;
  correctAnswers = 0;
  currentStage = 1;
  questionIndex = 0;
  questions = [];
  updateProgressBars();
  buttonMenu.style.display = 'block';
  gameFinished = false;
}

// Submit Answer (Game Mode)
async function submitAnswer(questionId, selectedAnswer) {
  if (gameFinished) return;
  const response = await fetch('/submit_answer', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question_id: questionId, selected_answer: selectedAnswer }),
  });
  const result = await response.json();
  if (result.correct) {
    correctAnswers++;
    cyberProgress += 2.5;
    alert('Correct! Great job!');
  } else {
    hackerProgress += 2.5;
    alert(`Incorrect! The correct answer was ${result.correctAnswer}.`);
  }
  updateProgressBars();
  if (cyberProgress >= 100) {
    finishGame(`Congratz ${username}..... you defeted hacker team.`, true);
    return;
  }
  if (hackerProgress >= 100) {
    finishGame('You loose, hackers attacked us', false);
    return;
  }
  questionIndex++;
  if (questionIndex >= questions.length) {
    if (currentStage === 5) {
      if (correctAnswers >= 40) {
        finishGame(`Congratz ${username}..... you defeted hacker team.`, true);
      } else if (correctAnswers > 25) {
        finishGame('You are good, but not much to win', true);
      } else {
        finishGame('You can not protect, learn and come.', false);
      }
    } else {
      currentStage++;
      loadQuestions(currentStage);
    }
  } else {
    displayQuestion(questions[questionIndex]);
  }
}

// Update Custom Progress Bars (Fill and Indicator positions)
function updateProgressBars() {
  // Update text percentages
  document.getElementById('cyber-progress-text').innerText = cyberProgress + '%';
  document.getElementById('hacker-progress-text').innerText = hackerProgress + '%';
  // Update custom fill widths
  document.getElementById('cyber-fill').style.width = cyberProgress + '%';
  document.getElementById('hk-fill').style.width = hackerProgress + '%';
  // Update indicator positions: move the image to the right edge of the fill
  document.getElementById('cs-indicator').style.left = cyberProgress + '%';
  document.getElementById('hk-indicator').style.left = hackerProgress + '%';
}

// -------------------- Animation Functions --------------------

// Fireworks Animation for Win
function showFireworks() {
  const fireworksContainer = document.getElementById('fireworks');
  fireworksContainer.innerHTML = '';
  fireworksContainer.style.display = 'block';
  for (let i = 0; i < 30; i++) {
    const firework = document.createElement('span');
    firework.classList.add('firework');
    firework.style.left = Math.random() * 100 + '%';
    firework.style.top = Math.random() * 100 + '%';
    firework.style.animationDelay = Math.random() * 0.5 + 's';
    fireworksContainer.appendChild(firework);
  }
  setTimeout(() => {
    fireworksContainer.style.display = 'none';
  }, 3000);
}

// Error Animation for Loss
function showErrorAnimation(message) {
  const errorMsg = document.getElementById('error-msg');
  errorMsg.textContent = message;
  errorMsg.style.display = 'block';
  errorMsg.classList.add('shake');
  setTimeout(() => {
    errorMsg.style.display = 'none';
    errorMsg.classList.remove('shake');
  }, 3000);
}

// -------------------- Other Navigation --------------------

viewScoreBtn.addEventListener('click', async () => {
  document.getElementById('leaderboard-btn').click();
});
exitGameBtn.addEventListener('click', () => {
  alert('Exiting the game. Thank you for playing!');
  resetGame();
});
function resetGame() {
  gameSection.style.display = 'none';
  const progressSection = document.getElementById('progress-section');
  progressSection.style.display = 'none';
  leaderboardSection.style.display = 'none';
  buttonMenu.style.display = 'none';
  loginSection.style.display = 'block';
  cyberProgress = 0;
  hackerProgress = 0;
  correctAnswers = 0;
  currentStage = 1;
  questionIndex = 0;
  questions = [];
  updateProgressBars();
  gameFinished = false;
}


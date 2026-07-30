// AmtAssist frontend — handles user input, calls the /ask API, displays results

// Get references to DOM elements
const questionInput = document.getElementById('question');
const askButton = document.getElementById('ask-button');
const responseSection = document.getElementById('response-section');
const loadingDiv = document.getElementById('loading');
const answerContainer = document.getElementById('answer-container');
const answerText = document.getElementById('answer');
const sourcesList = document.getElementById('sources');
const errorDiv = document.getElementById('error');
const errorMessage = errorDiv.querySelector('.error-message');


// Helper: show one section, hide the others
function showSection(section) {
    loadingDiv.classList.add('hidden');
    answerContainer.classList.add('hidden');
    errorDiv.classList.add('hidden');
    
    if (section) {
        section.classList.remove('hidden');
    }
}


// Helper: clean up source filenames for display
// e.g. "how_to_find_an_apartment_in_berlin.txt" -> "How To Find An Apartment In Berlin"
function formatSourceName(filename) {
    return filename
        .replace('.txt', '')
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}


// The main function: send question to backend, display response
async function askQuestion() {
    const question = questionInput.value.trim();
    
    // Validate: don't send empty questions
    if (!question) {
        showError('Please enter a question first.');
        return;
    }
    
    // Show loading state
    responseSection.classList.remove('hidden');
    showSection(loadingDiv);
    askButton.disabled = true;
    
    try {
        // Call the /ask endpoint
        const url = `/ask?question=${encodeURIComponent(question)}`;
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Display the answer
        answerText.textContent = data.answer;
        
        // Display sources (deduplicated)
        sourcesList.innerHTML = '';
        const seenSources = new Set();
        data.sources.forEach(source => {
            if (!seenSources.has(source.source)) {
                seenSources.add(source.source);
                const li = document.createElement('li');
                li.textContent = formatSourceName(source.source);
                sourcesList.appendChild(li);
            }
        });
        
        showSection(answerContainer);
        
    } catch (error) {
        console.error('Error fetching answer:', error);
        showError(`Something went wrong: ${error.message}. Make sure the server is running.`);
    } finally {
        askButton.disabled = false;
    }
}


// Helper: display an error message
function showError(message) {
    errorMessage.textContent = message;
    responseSection.classList.remove('hidden');
    showSection(errorDiv);
}


// Attach event listeners
askButton.addEventListener('click', askQuestion);

// Also submit on Ctrl+Enter or Cmd+Enter inside the textarea
questionInput.addEventListener('keydown', (event) => {
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
        event.preventDefault();
        askQuestion();
    }
});
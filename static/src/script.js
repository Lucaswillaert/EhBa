document.addEventListener('DOMContentLoaded', function() {
    let form = document.getElementById('chat-form');
    let questionInput = document.getElementById('question');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        let question = questionInput.value;
        questionInput.value = ''; // Clear the input field

        // Create and append user message
        let userMessageDiv = document.createElement('div');
        userMessageDiv.className = 'message user-message flex justify-end items-start mb-4';
        userMessageDiv.innerHTML = '<div class="bg-blue-500 text-white rounded-tl-lg rounded-bl-lg rounded-br-lg px-4 py-2 max-w-full break-words ml-[20%]">' + question.replace(/\n/g, '<br>') + '</div>';
        document.getElementById('chat-box').appendChild(userMessageDiv);

        // Show loading dots and disable input and button
        let loadingBubbleDiv = createBubbleWithLoadingDots();
        document.getElementById('chat-box').appendChild(loadingBubbleDiv);
        questionInput.disabled = true;
        form.querySelector('button').disabled = true;

        // Create JSON payload
        let payload = JSON.stringify({question: question});

        let xhr = new XMLHttpRequest();
        xhr.open('POST', '/chat', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = function() {
            if (this.status >= 200 && this.status < 400) {
                console.log(this.response);
                let response = JSON.parse(this.response);
                console.log(response);

                // Hide loading dots and type out response
                loadingBubbleDiv.remove();
                typeResponse(response.message.replace(/\n/g, '<br>'));

                // Re-enable input and button after response is typed out
                questionInput.disabled = false;
                form.querySelector('button').disabled = false;
            } else {
                console.error('Error reaching the server.' + this.status);
            }
        };
        xhr.onerror = function() {
            console.error('Connection error.');

            // Re-enable input and button in case of error
            questionInput.disabled = false;
            form.querySelector('button').disabled = false;
        };
        xhr.send(payload);
    });
});

function createBubbleWithLoadingDots() {
    let bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'message bot-message flex justify-start items-start mb-4 max-w-4/5';

    let loadingDotsDiv = document.createElement('div');
    loadingDotsDiv.className = 'flex space-x-1 justify-center items-center';
    loadingDotsDiv.innerHTML = `
    <span class='sr-only'>Loading...</span>
    <div class='h-2 w-2 bg-gray-700 rounded-full animate-bounce' style='animation-delay: -0.3s'></div>
    <div class='h-2 w-2 bg-gray-700 rounded-full animate-bounce' style='animation-delay: -0.15s'></div>
    <div class='h-2 w-2 bg-gray-700 rounded-full animate-bounce'></div>
    `;

    bubbleDiv.appendChild(loadingDotsDiv);
    return bubbleDiv;
}

function typeResponse(message) {
    // Create and append bot response bubble
    let botResponseDiv = document.createElement('div');
    botResponseDiv.className = 'message bot-message flex justify-start items-start mb-4 max-w-4/5';
    let bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'bg-gray-300 text-black rounded-tr-lg rounded-br-lg rounded-bl-lg px-4 max-w-full py-2 break-words';
    botResponseDiv.appendChild(bubbleDiv);
    document.getElementById('chat-box').appendChild(botResponseDiv);

    // Re-enable input and button after response is typed out
    let questionInput = document.getElementById('question');
    if (questionInput) {
        questionInput.disabled = false;
        let form = document.getElementById('chat-form');
        form.querySelector('button').disabled = false;
    }

    // Typing animation
    let currentIndex = 0;
    let typingInterval = setInterval(function() {
        if (currentIndex < message.length) {
            if (message[currentIndex] === '<' && message.substr(currentIndex, 4) === '<br>') {
                bubbleDiv.innerHTML += '<br>';
                currentIndex += 4;
            } else {
                bubbleDiv.appendChild(document.createTextNode(message[currentIndex]));
                currentIndex++;
            }
        } else {
            // Stop typing animation
            clearInterval(typingInterval);
        }
    }, 10); // Adjust typing speed as needed (in milliseconds)
}


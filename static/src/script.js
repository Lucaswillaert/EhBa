document.addEventListener('DOMContentLoaded', function() {
    let form = document.getElementById('chat-form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        let question = document.getElementById('question').value;

        // Create and append user message
        let userMessageDiv = document.createElement('div');
        userMessageDiv.className = 'message user-message flex justify-end items-start mb-4';
        userMessageDiv.innerHTML = '<div class="bg-blue-500 text-white rounded-tl-lg rounded-bl-lg rounded-br-lg px-4 py-2 max-w-4/5">' + question + '</div>';
        document.getElementById('chat-box').appendChild(userMessageDiv);

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
                let botResponseDiv = document.createElement('div');
                botResponseDiv.className = 'message bot-message flex justify-start items-start mb-4';
                botResponseDiv.innerHTML = '<div class="bg-gray-300 text-black rounded-tr-lg rounded-br-lg rounded-bl-lg px-4 py-2 max-w-4/5">' + response.message + '</div>';
                document.getElementById('chat-box').appendChild(botResponseDiv);
            } else {
                console.error('Error reaching the server.' + this.status);
            }
        };
        xhr.onerror = function() {
            console.error('Connection error.');
        };
        xhr.send(payload);
    });
});

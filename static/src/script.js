document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('chat-form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        var question = document.getElementById('question').value;

        // Create and append user message
        var userMessageDiv = document.createElement('div');
        userMessageDiv.className = 'message user-message flex justify-end items-start mb-4 max-w-4/5';
        userMessageDiv.innerHTML = '<div class="bg-blue-500 text-white rounded-tl-lg rounded-bl-lg rounded-br-lg px-4 py-2 max-w-4/5">' + question + '</div>';
        document.getElementById('chat-history').appendChild(userMessageDiv);

        var xhr = new XMLHttpRequest();
        var proxyUrl = 'http://localhost:8080/';
        var targetUrl = 'https://ehb-chatbot.azurewebsites.net/api/openai_request_function?code=8CyjNc52VM-4ays5jYzl3gxNYYx9ZesCyPIxJ56bNM8qAzFu6Zl7tA==';
        xhr.open('POST', proxyUrl + targetUrl, true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = function() {
            if (this.status >= 200 && this.status < 400) {
                // Success!
                var response = JSON.parse(this.response);

                // Create and append bot response
                var botResponseDiv = document.createElement('div');
                botResponseDiv.className = 'message bot-message flex justify-start items-start mb-4 max-w-4/5';
                botResponseDiv.innerHTML = '<div class="bg-gray-300 text-black rounded-tr-lg rounded-br-lg rounded-bl-lg px-4 py-2 max-w-4/5">' + response + '</div>';
                document.getElementById('chat-history').appendChild(botResponseDiv);
            } else {
                // We reached our target server, but it returned an error
            }
        };
        xhr.onerror = function() {
            // There was a connection error of some sort
        };
        xhr.send(JSON.stringify({ question: question }));
    });
});
document.addEventListener('DOMContentLoaded', function() {
    const streamForm = document.getElementById('streamForm');
    const generateButton = document.getElementById('generatePlaylist');
    const messageContainer = document.getElementById('messageContainer');

    // Get the base URL dynamically
    const baseURL = window.location.origin;

    streamForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const streamData = {
            name: document.getElementById('streamName').value,
            url: document.getElementById('streamUrl').value,
            duration: parseInt(document.getElementById('duration').value)
        };

        try {
            const response = await fetch(`${baseURL}/api/add-stream`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(streamData)
            });

            const data = await response.json();
            
            if (response.ok) {
                showMessage(data.message, 'success');
                streamForm.reset();
            } else {
                showMessage(data.message, 'error');
            }
        } catch (error) {
            showMessage('Error connecting to server', 'error');
        }
    });

    generateButton.addEventListener('click', async function() {
        try {
            window.location.href = `${baseURL}/api/generate`;
        } catch (error) {
            showMessage('Error generating playlist', 'error');
        }
    });

    function showMessage(message, type) {
        messageContainer.textContent = message;
        messageContainer.className = 'message-container ' + type;
        
        setTimeout(() => {
            messageContainer.textContent = '';
            messageContainer.className = 'message-container';
        }, 3000);
    }
}); 
// When receiving messages
socketio.on('message', (data) => {
  console.log('Received message:', data);
  // Add message to your messages div
  const messagesDiv = document.getElementById('messages');
  messagesDiv.innerHTML += `
      <div class="message">
          <strong>${data.user}</strong>: ${data.message}
          <small>${data.timestamp}</small>
      </div>
  `;
});

// When user joins/leaves
socketio.on('status', (data) => {
  console.log('Status update:', data);
});

// Improved sendMessage function
const sendMessage = () => {
const messageInput = document.getElementById('message');
const message = messageInput.value;

console.log('Sending message:', message);

socketio.emit('message', {
  room: "{{room.id}}", // Make sure to pass the correct room ID
  message: message
});

messageInput.value = ''; // Clear input after sending
};

// When joining room
socketio.emit('join', {
room: "{{room.id}}",
user: "{{user.first_name}}"
});
const socket = io();

// Function to toggle visibility of ciphertext and plaintext
function toggleVisibility(index) {
    const plaintextElement = document.getElementById(`plaintext-${index}`);
    const ciphertextElement = document.getElementById(`ciphertext-${index}`);
    if (plaintextElement.style.display === 'none') {
        plaintextElement.style.display = 'block';
        ciphertextElement.style.display = 'none';
    } else {
        plaintextElement.style.display = 'none';
        ciphertextElement.style.display = 'block';
    }
}

socket.on('receive_message', function(data) {
    const messageBox = document.getElementById('message_box');
    // Create a new div for the incoming message
    const messageElement = document.createElement('div');
    messageElement.className = 'message';

    // Create elements for plaintext and ciphertext
    const plaintextElement = document.createElement('p');
    plaintextElement.id = `plaintext-${data.index}`;
    plaintextElement.textContent = data.plaintext; // Display plaintext
    plaintextElement.style.display = 'none'; // Hide plaintext by default

    const ciphertextElement = document.createElement('p');
    ciphertextElement.id = `ciphertext-${data.index}`;
    ciphertextElement.textContent = `Ciphertext: ${data.ciphertext}`; // Display ciphertext

    // Create a checkbox to toggle visibility
    const toggleCheckbox = document.createElement('input');
    toggleCheckbox.type = 'checkbox';
    toggleCheckbox.onclick = () => toggleVisibility(data.index);
    const toggleLabel = document.createElement('label');
    toggleLabel.textContent = 'Show Plaintext';
    toggleLabel.style.marginLeft = '5px';

    // Append elements to messageElement
    messageElement.appendChild(ciphertextElement);
    messageElement.appendChild(plaintextElement);
    messageElement.appendChild(toggleCheckbox);
    messageElement.appendChild(toggleLabel);

    messageBox.appendChild(messageElement);
    messageBox.scrollTop = messageBox.scrollHeight; // Scroll to the bottom
});
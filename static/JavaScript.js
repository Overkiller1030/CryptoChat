document.addEventListener("DOMContentLoaded", () => {
  const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  socket.on('receive_message', function(data) {
      addMessage(data);
  });

  function addMessage(data) {
      const messageBox = document.getElementById('message_box');
      const messageElement = document.createElement('p');
      messageElement.innerHTML = data.plaintext;
      messageElement.setAttribute("data-plaintext", data.plaintext);
      messageElement.setAttribute("data-ciphertext", JSON.stringify(data.ciphertext));
      messageElement.onclick = toggleCiphertext;
      messageBox.appendChild(messageElement);
  }

  window.toggleCiphertext = function(event) {
      const messageElement = event.target;
      if (messageElement.innerHTML === messageElement.dataset.plaintext) {
          messageElement.innerHTML = messageElement.dataset.ciphertext;
      } else {
          messageElement.innerHTML = messageElement.dataset.plaintext;
      }
  };
});
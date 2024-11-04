function sendMessage() {
  let userInput = document.getElementById("chat-input").value;
  let chatContainer = document.getElementById("chatlogs");

  if (userInput.trim() === "") return; 

  
  let userDiv = document.createElement("div");
  userDiv.className = "chat self";
  let userText = document.createElement("p");
  let userImage = document.createElement("div");
  userText.textContent = userInput;
  userText.className = "chat-message";
  userImage.className = "user-photo";
  userDiv.appendChild(userText);
  userDiv.appendChild(userImage);
  chatContainer.appendChild(userDiv);

  document.getElementById("chat-input").value = "";


  chatContainer.scrollTop = chatContainer.scrollHeight;

  fetch("/ask", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
      },
      body: JSON.stringify({ question: userInput }),
  })
  .then((response) => {
      console.log("Risposta dal server ricevuta:", response);
      return response.json();
  })
  .then((data) => {
      console.log("Dati effettivi ricevuti:", data);

      
      let botDiv = document.createElement("div");
      botDiv.className = "chat robot";
      let botText = document.createElement("p");
      let botImage = document.createElement("div");
      botText.textContent = data.answer;
      botText.className = "chat-message";
      botImage.className = "user-photo";
      botDiv.appendChild(botText);
      botDiv.appendChild(botImage);
      chatContainer.appendChild(botDiv);

      
      chatContainer.scrollTop = chatContainer.scrollHeight;
  })
  .catch((error) => {
      console.error("Errore nella richiesta:", error);
  });
}
/*
window.onload = function() {
  let chatContainer = document.getElementById("chatlogs");

  let welcomeDiv = `
    <div class="chat robot">
      <div class="user-photo"></div>
      <p class="chat-message">Ciao! Come posso aiutarti?</p>
    </div>
  `;
  chatContainer.insertAdjacentHTML('beforeend', welcomeDiv);

  chatContainer.scrollTop = chatContainer.scrollHeight;
};*/

document.getElementById("send").addEventListener("click", function () {
  sendMessage();
});


document.getElementById("chat-input").addEventListener("keypress", function (event) {
  if (event.key === "Enter") {
      event.preventDefault();  
      sendMessage();
  }
});

const chatContainer = document.getElementById("chat-container");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

const API_KEY = "your-openai-api-key"; // Replace with your OpenAI API key

sendBtn.addEventListener("click", () => {
  const message = userInput.value.trim();
  if (message) {
    addMessage("user", message);
    fetchAIResponse(message);
    userInput.value = "";
  }
});

function addMessage(sender, message) {
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${sender}`;
  messageDiv.textContent = message;
  chatContainer.appendChild(messageDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

async function fetchAIResponse(prompt) {
  addMessage("ai", "Thinking...");
  const apiResponse = await fetch("https://api.openai.com/v1/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${API_KEY}`,
    },
    body: JSON.stringify({
      model: "text-davinci-003",
      prompt: `You are a helpful game AI. ${prompt}`,
      max_tokens: 100,
      temperature: 0.7,
    }),
  });

  if (apiResponse.ok) {
    const data = await apiResponse.json();
    const aiMessage = data.choices[0].text.trim();
    updateLastMessage(aiMessage);
  } else {
    updateLastMessage("Something went wrong. Please try again!");
  }
}

function updateLastMessage(message) {
  const aiMessages = chatContainer.querySelectorAll(".ai");
  const lastAiMessage = aiMessages[aiMessages.length - 1];
  lastAiMessage.textContent = message;
}
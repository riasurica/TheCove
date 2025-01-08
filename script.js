document.getElementById("send").addEventListener("click", async () => {
  const userInput = document.getElementById("userInput").value.trim();
  if (!userInput) return;

  const chatbox = document.getElementById("chatbox");

  // Display user input
  const userMessage = document.createElement("p");
  userMessage.textContent = `You: ${userInput}`;
  chatbox.appendChild(userMessage);

  document.getElementById("userInput").value = "";

  try {
    const response = await fetch("http://localhost:5000/api/conversation", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userInput }),
    });

    const data = await response.json();

    // Display AI response
    const aiMessage = document.createElement("p");
    aiMessage.textContent = `AI: ${data.reply}`;
    chatbox.appendChild(aiMessage);

    chatbox.scrollTop = chatbox.scrollHeight;
  } catch (error) {
    console.error("Error:", error);
    const errorMessage = document.createElement("p");
    errorMessage.textContent = "AI: Sorry, there was an error.";
    chatbox.appendChild(errorMessage);
  }
});

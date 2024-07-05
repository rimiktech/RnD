async function sendMessage() {
    const chatArea = document.getElementById('chatArea');
    const prompt = document.getElementById('prompt');
    const userMessage = prompt.value.trim();
                  
    if (userMessage) {
        const userDiv = document.createElement('div');
        userDiv.classList.add('query');
        userDiv.innerHTML = `<p>${userMessage}</p>`;
        chatArea.appendChild(userDiv);

        // Simulate a response
        const botResponse = await fetchData(userMessage);


        const botDiv = document.createElement('div');
        botDiv.classList.add('output');
        botDiv.innerHTML = `<p>${botResponse}</p>`;
        chatArea.appendChild(botDiv);

        // Clear the prompt
        prompt.value = '';

        // Scroll to the bottom of the chat area
        chatArea.scrollTop = chatArea.scrollHeight;
    }
}

const fetchData = async (query) => {
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    
    const raw = JSON.stringify({ query });
    
    const requestOptions = {
      method: "POST",
      headers: myHeaders,
      body: raw,
      redirect: "follow"
    };
    
    const response = await fetch("http://127.0.0.1:5000/api/chat", requestOptions);
    const result = await response.text(); // Receive response as text
    return result; // Return the text response
};

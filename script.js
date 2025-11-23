// script.js

function analyzeEmail() {
    // 1. Get the text input and result area
    const emailText = document.getElementById('email-text').value;
    const resultDiv = document.getElementById('result');
    
    if (emailText.length === 0) {
        resultDiv.textContent = "Please enter some text to analyze.";
        resultDiv.className = "spam"; // Use red style for error
        resultDiv.style.display = 'block'; // Make sure the result box is visible
        return;
    }

    // Show processing status
    resultDiv.textContent = "Analyzing...";
    resultDiv.className = "";
    resultDiv.style.display = 'block';

    // 2. The Connection: Fetch API sends the data to the Flask backend
    // This connects to the /predict endpoint on your running server
    fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        // Send the user's text as a JSON object
        body: JSON.stringify({ text: emailText })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // 3. The Output: Process the result received from Flask
        const prediction = data.prediction;
        const confidence = (prediction === 'SPAM' ? data.spam_confidence : data.ham_confidence) * 100;
        
        resultDiv.textContent = `Prediction: ${prediction} | Confidence: ${confidence.toFixed(2)}%`;
        
        // 4. Style the output based on the prediction
        if (prediction === 'SPAM') {
            resultDiv.className = 'spam';
        } else {
            resultDiv.className = 'ham';
        }
    })
    .catch(error => {
        console.error('Connection Error:', error);
        resultDiv.textContent = "Error connecting to the server. Please check the terminal running app.py.";
        resultDiv.className = "spam";
    });
}
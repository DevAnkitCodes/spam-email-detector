// script.js

function analyzeEmail() {

    const emailText = document.getElementById('email-text').value;
    const resultDiv = document.getElementById('result');

    if (emailText.length === 0) {
        resultDiv.textContent = "Please enter some text to analyze.";
        resultDiv.className = "spam";
        resultDiv.style.display = 'block';
        return;
    }

    resultDiv.textContent = "Analyzing...";
    resultDiv.className = "";
    resultDiv.style.display = 'block';

    // Auto-detect URL (Localhost or Render)
    const apiURL = window.location.origin + "/predict";

    fetch(apiURL, {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: emailText })
    })
    .then(response => response.json())
    .then(data => {
        const prediction = data.prediction;
        const confidence = (prediction === 'SPAM' ? data.spam_confidence : data.ham_confidence) * 100;

        resultDiv.textContent = `Prediction: ${prediction} | Confidence: ${confidence.toFixed(2)}%`;
        resultDiv.className = prediction === 'SPAM' ? "spam" : "ham";
    })
    .catch(error => {
        console.error("Error:", error);
        resultDiv.textContent = "Server error. Please check if app.py is running.";
        resultDiv.className = "spam";
    });
}

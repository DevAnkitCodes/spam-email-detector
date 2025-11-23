// This function runs when you click "Analyze Email"
function analyzeEmail() {

    // Get the text the user wrote
    const emailText = document.getElementById('email-text').value;

    // The div where the result will appear
    const resultDiv = document.getElementById('result');

    // If no text is entered
    if (emailText.length === 0) {
        resultDiv.textContent = "Please enter some text to analyze.";
        resultDiv.className = "spam";   // red warning style
        resultDiv.style.display = 'block';
        return;
    }

    // Show loading message
    resultDiv.textContent = "Analyzing...";
    resultDiv.className = "";
    resultDiv.style.display = 'block';

    /**
     * VERY IMPORTANT:
     * window.location.origin works automatically for both:
     *   ✔ Localhost: http://127.0.0.1:5000
     *   ✔ Render deployment: https://yourappname.onrender.com
     * 
     * So you don't need to change anything when deploying.
     */
    const apiUrl = window.location.origin + "/predict";

    // Send POST request to Flask API
    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        // Send email text as JSON
        body: JSON.stringify({ text: emailText })
    })

    // Convert response → JSON
    .then(res => res.json())

    // Handle prediction response
    .then(data => {

        const prediction = data.prediction; // "SPAM" or "HAM"

        // Choose correct confidence score
        const confidence =
            (prediction === "SPAM" ? data.spam_confidence : data.ham_confidence) * 100;

        // Show result on screen
        resultDiv.textContent =
            `Prediction: ${prediction} | Confidence: ${confidence.toFixed(2)}%`;

        // Apply color (spam → red, ham → green)
        resultDiv.className = (prediction === "SPAM") ? "spam" : "ham";
    })

    // If server is not running or error occurs
    .catch(err => {
        console.error(err);
        resultDiv.textContent = "Server error. Check Render logs.";
        resultDiv.className = "spam";
    });
}

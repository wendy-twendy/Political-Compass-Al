function displayResults(result) {
    console.log('Displaying results:', result);
    window.quizResult = result; // Store the result globally
    const plotlyChart = document.getElementById('plotly-chart');
    const resultDescription = document.getElementById('result-description');
    
    if (!plotlyChart) {
        console.error('Plotly chart container not found');
        return;
    }
    
    // Parse the plot JSON and render it using Plotly
    const plotData = JSON.parse(result.plot_json);
    Plotly.newPlot('plotly-chart', plotData.data, plotData.layout, {
        displayModeBar: false,
        responsive: true,
        staticPlot: true
    });
    
    let economicLabel = result.economic < 0 ? 'Left' : 'Right';
    let libertarianAuthoritarianLabel = result.libertarian_authoritarian < 0 ? 'Libertarian' : 'Authoritarian';
    
    resultDescription.textContent = `Your political compass position is: Economic: ${result.economic.toFixed(2)} (${economicLabel}), Social: ${result.libertarian_authoritarian.toFixed(2)} (${libertarianAuthoritarianLabel})`;

    // Add social media sharing buttons
    const shareContainer = document.createElement('div');
    shareContainer.className = 'flex justify-center mt-4 space-x-4';
    shareContainer.innerHTML = `
        <button onclick="shareOnTwitter()" class="bg-blue-400 text-white px-4 py-2 rounded hover:bg-blue-500 transition duration-200">Share on Twitter</button>
        <button onclick="shareOnLinkedIn()" class="bg-blue-800 text-white px-4 py-2 rounded hover:bg-blue-900 transition duration-200">Share on LinkedIn</button>
    `;
    resultDescription.parentNode.insertBefore(shareContainer, resultDescription.nextSibling);
}

function downloadImage() {
    Plotly.toImage('plotly-chart', {format: 'png', width: 800, height: 800}).then(function(dataUrl) {
        var link = document.createElement('a');
        link.download = 'political_compass.png';
        link.href = dataUrl;
        link.click();
    });
}

function encodeAnswers() {
    return window.userAnswers ? window.userAnswers.join(',') : '';
}

function shareOnTwitter() {
    const answers = encodeAnswers();
    const url = encodeURIComponent(window.location.origin + '/shared_result?economic=' + window.quizResult.economic.toFixed(2) + '&libertarian_authoritarian=' + window.quizResult.libertarian_authoritarian.toFixed(2) + '&answers=' + answers);
    const text = encodeURIComponent("Check out my Political Compass Quiz result!");
    const shareUrl = `https://twitter.com/intent/tweet?url=${url}&text=${text}`;
    window.open(shareUrl, '_blank');
}

function shareOnLinkedIn() {
    const answers = encodeAnswers();
    const url = encodeURIComponent(window.location.origin + '/shared_result?economic=' + window.quizResult.economic.toFixed(2) + '&libertarian_authoritarian=' + window.quizResult.libertarian_authoritarian.toFixed(2) + '&answers=' + answers);
    const shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${url}`;
    window.open(shareUrl, '_blank');
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('download-button').addEventListener('click', downloadImage);
});

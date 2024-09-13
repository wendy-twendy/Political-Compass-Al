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
    
    resultDescription.innerHTML = `
        <p class="text-lg font-semibold mb-2">Your political compass position:</p>
        <p>Economic: ${result.economic.toFixed(2)} (${economicLabel})</p>
        <p>Social: ${result.libertarian_authoritarian.toFixed(2)} (${libertarianAuthoritarianLabel})</p>
        <h3 class="text-xl font-semibold mt-4">Your Quadrant: ${result.quadrant}</h3>
        <p class="mt-2 whitespace-pre-line">${result.explanation}</p>
        <h3 class="text-xl font-semibold mt-4">Comparisons:</h3>
        <p>Average Position: Economic: ${result.average_economic.toFixed(2)}, Social: ${result.average_libertarian_authoritarian.toFixed(2)}</p>
        <h4 class="text-lg font-semibold mt-2">Famous Political Figures:</h4>
        <ul class="list-disc list-inside">
            ${Object.entries(result.famous_figures).map(([name, position]) => 
                `<li>${name}: Economic: ${position[0].toFixed(2)}, Social: ${position[1].toFixed(2)}</li>`
            ).join('')}
        </ul>
    `;

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

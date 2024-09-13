function displayResults(result) {
    console.log('Displaying results:', result);
    try {
        const plotlyChart = document.getElementById('plotly-chart');
        const resultDescription = document.getElementById('result-description');
        
        if (!plotlyChart || !resultDescription) {
            console.error('Required DOM elements not found');
            return;
        }
        
        if (result && result.plot_json) {
            const plotData = JSON.parse(result.plot_json);
            Plotly.newPlot('plotly-chart', plotData.data, plotData.layout, {
                displayModeBar: false,
                responsive: true,
                staticPlot: true
            });
        } else {
            console.error('Invalid plot data');
        }
        
        let economicLabel = result.economic < 0 ? 'Left' : 'Right';
        let libertarianAuthoritarianLabel = result.libertarian_authoritarian < 0 ? 'Libertarian' : 'Authoritarian';
        
        resultDescription.innerHTML = `
            <h3 class="text-xl font-semibold mb-2">Your Results:</h3>
            <p>Economic: ${result.economic.toFixed(2)} (${economicLabel})</p>
            <p>Social: ${result.libertarian_authoritarian.toFixed(2)} (${libertarianAuthoritarianLabel})</p>
            <h3 class="text-xl font-semibold mt-4 mb-2">Your Quadrant: ${result.quadrant}</h3>
            <p class="mb-4">${result.explanation}</p>
            <h3 class="text-xl font-semibold mt-4 mb-2">Comparisons:</h3>
            <p>Average Position: Economic: ${result.average_economic.toFixed(2)}, Social: ${result.average_social.toFixed(2)}</p>
            <p>Closest Political Figure: ${result.closest_figure}</p>
            <h4 class="text-lg font-semibold mt-2 mb-1">Top 3 Closest Figures:</h4>
            <ul class="list-disc list-inside mb-4">
                ${result.comparisons.map(comp => `<li>${comp.name} (Distance: ${comp.distance.toFixed(2)})</li>`).join('')}
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
    } catch (error) {
        console.error('Error displaying results:', error);
        alert('An error occurred while displaying the results. Please try again.');
    }
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

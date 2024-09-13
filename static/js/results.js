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
    `;

    // Add comparisons if they exist
    if (result.comparisons && result.comparisons.average_scores && result.comparisons.famous_figures) {
        const comparisonsContainer = document.createElement('div');
        comparisonsContainer.className = 'mt-6';
        comparisonsContainer.innerHTML = `
            <h3 class="text-xl font-semibold mb-2">Comparisons</h3>
            <h4 class="text-lg font-semibold mt-4">Average Scores</h4>
            <ul class="list-disc list-inside">
                <li>Overall: Economic ${result.comparisons.average_scores.overall.economic.toFixed(2)}, Social ${result.comparisons.average_scores.overall.social.toFixed(2)}</li>
                <li>Your Age Group: Economic ${result.comparisons.average_scores.age_group.economic.toFixed(2)}, Social ${result.comparisons.average_scores.age_group.social.toFixed(2)}</li>
                <li>Your Sex: Economic ${result.comparisons.average_scores.sex.economic.toFixed(2)}, Social ${result.comparisons.average_scores.sex.social.toFixed(2)}</li>
                <li>Your Country: Economic ${result.comparisons.average_scores.country.economic.toFixed(2)}, Social ${result.comparisons.average_scores.country.social.toFixed(2)}</li>
            </ul>
            <h4 class="text-lg font-semibold mt-4">Famous Political Figures</h4>
            <ul class="list-disc list-inside">
                ${Object.entries(result.comparisons.famous_figures).map(([name, scores]) => `
                    <li>${name}: Economic ${scores.economic.toFixed(2)}, Social ${scores.social.toFixed(2)}</li>
                `).join('')}
            </ul>
        `;
        resultDescription.appendChild(comparisonsContainer);
    }

    // Add social media sharing buttons
    const shareContainer = document.createElement('div');
    shareContainer.className = 'flex justify-center mt-4 space-x-4';
    shareContainer.innerHTML = `
        <button onclick="shareOnTwitter()" class="bg-blue-400 text-white px-4 py-2 rounded hover:bg-blue-500 transition duration-200">Share on Twitter</button>
        <button onclick="shareOnLinkedIn()" class="bg-blue-800 text-white px-4 py-2 rounded hover:bg-blue-900 transition duration-200">Share on LinkedIn</button>
    `;
    resultDescription.parentNode.insertBefore(shareContainer, resultDescription.nextSibling);
}

function shareOnTwitter() {
    const url = encodeURIComponent(window.location.origin);
    const text = encodeURIComponent("Check out my Political Compass Quiz result!");
    const shareUrl = `https://twitter.com/intent/tweet?url=${url}&text=${text}`;
    window.open(shareUrl, '_blank');
}

function shareOnLinkedIn() {
    const url = encodeURIComponent(window.location.origin);
    const shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${url}`;
    window.open(shareUrl, '_blank');
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('download-button').addEventListener('click', downloadImage);
});

function downloadImage() {
    Plotly.toImage('plotly-chart', {format: 'png', width: 800, height: 800}).then(function(dataUrl) {
        var link = document.createElement('a');
        link.download = 'political_compass.png';
        link.href = dataUrl;
        link.click();
    });
}
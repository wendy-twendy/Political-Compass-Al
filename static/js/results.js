function displayResults(result) {
    console.log('Displaying results:', result);
    window.quizResult = result; // Store the result globally
    const plotlyChart = document.getElementById('plotly-chart');
    const resultDescription = document.getElementById('result-description');
    const averageScoresChart = document.getElementById('average-scores-chart');
    const famousFiguresChart = document.getElementById('famous-figures-chart');

    if (!plotlyChart || !averageScoresChart || !famousFiguresChart) {
        console.error('One or more chart containers not found');
        return;
    }

    // Parse the plot JSON and render it using Plotly
    const plotData = JSON.parse(result.plot_json);
    Plotly.newPlot('plotly-chart', plotData.data, plotData.layout, {
        displayModeBar: false,
        responsive: true,
        staticPlot: true
    });

    // Render Average Scores plot
    const averageScoresData = JSON.parse(result.average_scores_plot);
    Plotly.newPlot('average-scores-chart', averageScoresData.data, averageScoresData.layout, {
        displayModeBar: false,
        responsive: true,
        staticPlot: true
    });

    // Render Famous Figures plot
    const famousFiguresData = JSON.parse(result.famous_figures_plot);
    Plotly.newPlot('famous-figures-chart', famousFiguresData.data, famousFiguresData.layout, {
        displayModeBar: false,
        responsive: true,
        staticPlot: true
    });

    // Add back the user's score description
    let economicLabel = result.economic < 0 ? 'Left' : 'Right';
    let libertarianAuthoritarianLabel = result.libertarian_authoritarian < 0 ? 'Libertarian' : 'Authoritarian';
    resultDescription.innerHTML = `
        <p class="text-lg font-semibold mb-2">Your political compass position:</p>
        <p>Economic: ${result.economic.toFixed(2)} (${economicLabel})</p>
        <p>Social: ${result.libertarian_authoritarian.toFixed(2)} (${libertarianAuthoritarianLabel})</p>
    `;

    const quadrantName = document.getElementById('quadrant-name');
    const quadrantDescription = document.getElementById('quadrant-description');
    
    quadrantName.textContent = result.quadrant;
    quadrantDescription.textContent = result.explanation;

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
    const economic = window.quizResult.economic.toFixed(2);
    const libertarianAuthoritarian = window.quizResult.libertarian_authoritarian.toFixed(2);
    const answers = encodeURIComponent(window.userAnswers.join(','));
    const url = encodeURIComponent(`${window.location.origin}/shared_result?economic=${economic}&libertarian_authoritarian=${libertarianAuthoritarian}&answers=${answers}`);
    const text = encodeURIComponent("Check out my Political Compass Quiz result!");
    const shareUrl = `https://twitter.com/intent/tweet?url=${url}&text=${text}`;
    window.open(shareUrl, '_blank');
}

function shareOnLinkedIn() {
    const economic = window.quizResult.economic.toFixed(2);
    const libertarianAuthoritarian = window.quizResult.libertarian_authoritarian.toFixed(2);
    const answers = encodeURIComponent(window.userAnswers.join(','));
    const url = encodeURIComponent(`${window.location.origin}/shared_result?economic=${economic}&libertarian_authoritarian=${libertarianAuthoritarian}&answers=${answers}`);
    const shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${url}`;
    window.open(shareUrl, '_blank');
}

// Comment out the downloadImage function and its event listener
/*
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
*/
